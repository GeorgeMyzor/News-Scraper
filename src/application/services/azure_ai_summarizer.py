import asyncio
from typing import List, Dict, TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from domain.article_enriched import ArticleEnriched
from abstractions.summarizer import Summarizer

from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    headline: str
    content: str
    chunks: List[str]
    chunk_summaries: List[str]
    article_enriched: str


class AzureAISummarizer(Summarizer):
    def __init__(
        self, 
        llm: BaseChatModel,
        summary_prompt: ChatPromptTemplate,
        chunk_summary_prompt: ChatPromptTemplate,
        token_text_splitter: TokenTextSplitter
    ):        
        self.text_splitter = token_text_splitter
        
        self.summary_chain = self._build_chain(summary_prompt, llm.with_structured_output(schema=ArticleEnriched))
        self.chunk_chain = self._build_chain(chunk_summary_prompt, llm)
        
        self.graph = self._build_graph()

    def _build_chain(self, prompt, llm):
        return prompt | llm | StrOutputParser()
    
    def _build_graph(self):
        graph = StateGraph(GraphState)

        def splitter_node(state: GraphState) -> GraphState:
            chunks = self.text_splitter.split_text(state["content"])
            return {**state, "chunks": chunks}

        async def summarize_chunks_node(state: GraphState) -> GraphState:
            summaries = await self.chunk_chain.abatch(
                [{"headline": state["headline"], "content": chunk} for chunk in state["chunks"]],
                config={"max_concurrency": 5}
            )
            return {**state, "chunk_summaries": summaries}

        async def article_enriched_node(state: GraphState) -> GraphState:
            joined = "\n".join(state["chunk_summaries"])
            final = await self.summary_chain.ainvoke({"headline": state["headline"], "content": joined})
            final.content = state["content"]  # Ensure original content and headline is preserved
            final.headline = state["headline"]
            return {**state, "article_enriched": final}

        graph.add_node("split", splitter_node)
        graph.add_node("summarize_chunks", summarize_chunks_node)
        graph.add_node("summarize_final", article_enriched_node)

        graph.set_entry_point("split")
        graph.add_edge("split", "summarize_chunks")
        graph.add_edge("summarize_chunks", "summarize_final")
        graph.add_edge("summarize_final", END)

        return graph.compile()

    async def summarize_async(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        tasks = [
            self.graph.ainvoke(article)
            for article in articles
        ]
        results = await asyncio.gather(*tasks)
        
        return [
            result["article_enriched"]
            for result in results
        ]
