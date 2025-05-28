from fastapi import FastAPI

from src.entrypoints.rest.exception_handlers import exception_container
from src.entrypoints.rest.routers import articles

app = FastAPI()

app.include_router(articles.router)

#exception_container(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.entrypoints.rest.main:app", host="127.0.0.1", port=8001, reload=False)
