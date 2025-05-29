import asyncio
import logging
from typing import TypedDict
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, END
from langsmith import traceable
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_not_exception_type

from domain.article_enriched import ArticleEnriched
from abstractions.summarizer import Summarizer
from application.utils.token_limit_validator import TokenLimitValidator
from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError

class GraphState(TypedDict):
    """State for the summarization graph."""
    headline: str
    content: str
    chunks: list[str]
    chunk_summaries: list[str]
    article_enriched: str


@traceable
class AzureAISummarizer(Summarizer):
    """
    Summarizer implementation using Azure AI.
    This class provides methods to summarize articles by splitting them into chunks,
    summarizing each chunk, and then combining the summaries into a final enriched article.
    Aslo knowsn as Map-Reduce summarization pattern.
    """
    def __init__(
        self, 
        llm: BaseChatModel,
        summary_prompt: ChatPromptTemplate,
        chunk_summary_prompt: ChatPromptTemplate,
        token_text_splitter: TokenTextSplitter,
        token_limit_validator: TokenLimitValidator,
    ):        
        self.text_splitter = token_text_splitter
        
        self.summary_chain = self._build_chain(summary_prompt, token_limit_validator, llm.with_structured_output(schema=ArticleEnriched))
        self.chunk_chain = self._build_chain(chunk_summary_prompt, token_limit_validator, llm)
        
        self.graph = self._build_graph()

    def _build_chain(self, prompt, token_limit_validator, llm):
        """
        Builds a chain for summarization using the provided prompt, token limit validator, and LLM.
        Args:
            prompt (ChatPromptTemplate): The prompt template for summarization.
            token_limit_validator (TokenLimitValidator): Validator to check token limits.
            llm (BaseChatModel): The language model to use for summarization.
        Returns:
            Chain: A chain that processes the summarization task.
        """
        return prompt | token_limit_validator | llm | StrOutputParser()
    
    def _build_graph(self):
        """Builds the state graph for summarization."""
        graph = StateGraph(GraphState)

        def splitter_node(state: GraphState) -> GraphState:
            """Splits the content into chunks using the text splitter."""
            chunks = self.text_splitter.split_text(state["content"])
            
            logging.debug(f"Split content into {len(chunks)} chunks.")
            
            return {**state, "chunks": chunks}

        @retry(
            wait=wait_exponential(multiplier=1, min=1, max=5), 
            stop=stop_after_attempt(2),
            retry=retry_if_not_exception_type(TokenLimitExceededError)
        )
        async def summarize_chunks_node(state: GraphState) -> GraphState:
            """Summarizes chunks of the article in batch."""
            summaries = await self.chunk_chain.abatch(
                [{"headline": state["headline"], "content": contet_chunk} for contet_chunk in state["chunks"]]
            )
            return {**state, "chunk_summaries": summaries}
        
        @retry(
            wait=wait_exponential(multiplier=1, min=1, max=5), 
            stop=stop_after_attempt(2),
            retry=retry_if_not_exception_type(TokenLimitExceededError)
        )
        async def summarize_all_node(state: GraphState) -> GraphState:
            """Combines chunk summaries into a final enriched article."""            
            if "chunk_summaries" in state and state["chunk_summaries"]:
                summaries = "\n".join(state["chunk_summaries"])
            else:
                summaries = state["content"]
                
            enriched_article = await self.summary_chain.ainvoke({"headline": state["headline"], "content": summaries})
            enriched_article.content = state["content"]  # Ensure original content and headline is preserved
            enriched_article.headline = state["headline"]
            
            return {**state, "article_enriched": enriched_article}

        graph.add_node("split", splitter_node)
        graph.add_node("summarize_chunks", summarize_chunks_node)
        graph.add_node("summarize_final", summarize_all_node)

        graph.set_entry_point("split")
        graph.add_conditional_edges(
            "split",
            lambda state: "summarize_chunks" if len(state["chunks"]) > 1 else "summarize_final"
        )
        graph.add_edge("summarize_chunks", "summarize_final")
        graph.add_edge("summarize_final", END)

        return graph.compile()

    async def summarize_async(self, articles: list[dict[str, str]]) -> list[dict[str, str]]:
        """
        Asynchronously summarizes a list of articles.
        Args:
            articles (List[Dict[str, str]]): List of articles with 'headline' and 'content'.
        Returns:
            List[Dict[str, str]]: List of enriched articles with summaries.
        """
        tasks = [
            self.graph.ainvoke(article)
            for article in articles
        ]
        results = await asyncio.gather(*tasks)
        
        # Extract the enriched articles from the results
        return [
            result["article_enriched"]
            for result in results
        ]
