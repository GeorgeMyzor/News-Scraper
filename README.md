# News Scraper

News Scraper is a Python tool that scrapes news articles from URLs, enriches them with AI-generated summaries and topic tags, and stores the processed data in a vector database (Chroma). It also supports user queries for similarity-based search to find relevant articles.

## Features

- **News Article Scraping**  
  Automatically extracts full-text content from user-provided URLs.

- **AI-Powered Summarization**  
  Leverages ChatGPT-4o mini to generate high-quality, structured summaries of articles.

- **Semantic Embedding Generation**  
  Uses Hugging Face models to convert content into vector embeddings for semantic search.

- **Query Enhancement**  
  Improves and refines user queries to increase the accuracy and relevance of search results.

- **LangChain LangGraph LangSmith**  
  LLM helper libraries used for creating reusable chains, robust executable graphs and LLM related metrics.

- **Vector Storage with Chroma**  
  Stores embeddings in a Chroma vector database to enable efficient similarity-based retrieval.

- **Clean Architecture Design**  
  Implements a modular and maintainable codebase inspired by Clean Architecture principles.

- **Scalable Summarization with Splitter + Map-Reduce**  
  Handles large or lengthy articles by splitting and summarizing content in parallel, then aggregating results.


## Project Structure

This project follows a Clean Architecture-inspired structure for maintainability, scalability, and clear separation of concerns.

```text
src/
├── abstractions/         # Interfaces, abstract base classes, and dependency injection
├── application/          # Business logic: services, use-cases, and custom exceptions
├── config/               # Configuration files: logging, prompts, and application settings
├── domain/               # Core domain models (e.g., Article)
├── entrypoints/          # REST API routers and external interfaces
├── repositories/         # Implementation of data access and persistence layers
```
The main entry point of the application is:
```
src/entrypoints/rest/main.py
```

## Requirements
- Python 3.13

- API keys for Azure OpenAI (see .env.example)

- Dependencies listed in requirements.txt
  
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GeorgeMyzor/News-Scraper.git
   cd News-Scraper
   ```
   
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Linux: source venv/bin/activate
   ```
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Configure environment variables:

   Copy .env.example to .env:
   ```bash
   cp .env.example .env
   ```
   Populate the .env file with required keys (see the Configuration section).

## Usage
   Run the CLI script:

  ```bash
  uvicorn entrypoints.rest.main:app --reload --app-dir src --port 8000 # Change port if already in use
  ```

  Go to http://127.0.0.1:8000/docs and use POST /articles/summary or GET /articles/query

## Configuration
The .env file must include the following variables:
```env
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-3-large"
AZURE_OPENAI_EMBEDDING_API_VERSION="2024-02-01"

LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

ARTICLES_COLLECTION_NAME="articles"
CHROMA_PERSIST_DIRECTORY="./chroma_db"

HUGGINGFACE_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"

USE_CHROMA_DB=true
USE_DETERMINISTIC_QUERY=false

QUERY_TOKEN_LIMIT=1000
# too low, for showcase
CHUNK_TOKEN_LIMIT=1000 
MAX_TOKEN_LIMIT=50000

PYTHONPATH=src
```
