# News Scrapper

News Scrapper is a Python tool that scrapes news articles from URLs, enriches them with AI-generated summaries and topic tags, and stores the processed data in a vector database (Chroma). It also supports user queries for similarity-based search to find relevant articles.

## Features

- Scrapes news articles from provided URLs  
- Uses ChatGPT 4o for AI-powered summarization with structured output  
- Generates embeddings via Hugging Face models  
- Stores data in Chroma vector database for efficient similarity search  
- Clean Architecture-inspired code structure for maintainability  

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
   
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
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
  python src/entrypoints/cli.py
  ```

  The script will prompt you to enter a URL to scrape or a query to search relevant news.

## Requirements
- Python 3.13

- API keys for Azure OpenAI and LangSmith (see .env.example)

- Dependencies listed in requirements.txt

## Configuration
The .env file must include the following variables:
```env
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
```