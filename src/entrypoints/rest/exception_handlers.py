from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

from application.exceptions.token_limit_exceeded import TokenLimitExceeded

def exception_container(app: FastAPI) -> None:
    
    @app.exception_handler(TokenLimitExceeded)
    async def token_limit_exception_handler(request: Request, exc: TokenLimitExceeded):
        """
        Exception handler for TokenLimitExceeded exceptions.
        Args:
            request (Request): The request object.
            exc (TokenLimitExceeded): The exception that was raised.
        Returns:
            JSONResponse: A JSON response with a 422 Unprocessable Entity status code and an error message.
        """
        
        logging.warning(f"Token limit exceeded: {exc}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)},
        )
        
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        General exception handler catches all unhandled exceptions and returns a JSON response
        with a 500 Internal Server Error status code.
        Args:
            request (Request): The request object.
            exc (Exception): The exception that was raised.
        Returns:
            JSONResponse: A JSON response with a 500 status code and an error message.
        """
        
        logging.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."},
        )