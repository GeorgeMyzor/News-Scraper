from langchain.prompts import ChatPromptTemplate

SYSTEM_SUMMARY_TEMPLATE = """
You are a precise and concise assistant that summarizes news articles into structured data.
Your task is to extract key information such as headline, summary, key topics, people mentioned, locations, and publication date.
If any information is missing or cannot be inferred, return null for that field.
Always return your answer in JSON format with clear, concise values.
"""

USER_SUMMARY_TEMPLATE = """
Summarize the following news article in 2-4 concise sentences, highlighting the main event, key people, and any outcomes or implications.

Headline: {headline}
Content: {content}
"""

def build_summary_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_SUMMARY_TEMPLATE),
        ("user", USER_SUMMARY_TEMPLATE),
    ])

SYSTEM_QUERY_TEMPLATE = """
You are a helpful assistant that rewrites user queries to improve their effectiveness for semantic search in a vector database.

Your goal is to:
- Expand or rephrase vague queries into more specific and semantically rich ones
- Include synonyms, named entities, or relevant contextual terms where appropriate
- Avoid changing the original intent of the query
- Ensure the result is natural, concise, and well-formed for embedding

Do not answer the query or provide results — only rewrite it to enhance its semantic embedding quality.
"""
USER_QUERY_TEMPLATE = """
Rewrite this query to make it semantically rich and specific for searching articles. Query: {userQuery}
"""
def build_query_enhancement_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_QUERY_TEMPLATE),
        ("user", USER_QUERY_TEMPLATE),
    ])