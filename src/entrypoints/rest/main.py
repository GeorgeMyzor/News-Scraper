import logging.config

from fastapi import FastAPI

from entrypoints.rest.exception_handlers import exception_container
from entrypoints.rest.routers import articles
from config.logging import LOGGING_CONFIG
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

logging.config.dictConfig(LOGGING_CONFIG)

set_llm_cache(InMemoryCache())

app = FastAPI()

app.include_router(articles.router)

exception_container(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("entrypoints.rest.main:app", host="127.0.0.1", port=8001, reload=False)
