from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError
from application.exceptions.url_validation_error import UrlValidationError
from application.exceptions.no_content_error import NoContentError

def exception_container(app: FastAPI) -> None:
        
    @app.exception_handler(NoContentError)
    async def no_content_exception_handler(request: Request, exc: NoContentError):
        """
        Exception handler for NoContentError exceptions.
        Args:
            request (Request): The request object.
            exc (NoContentError): The exception that was raised.
        Returns:
            JSONResponse: A JSON response with a 422 Unprocessable Entity status code and an error message.
        """
        logging.warning(f"No content extracted from URL: {exc.invalid_url}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": str(exc),
                "url": exc.invalid_url,
            },
        )
        
    @app.exception_handler(UrlValidationError)
    async def invalid_urls_exception_handler(request: Request, exc: UrlValidationError):
        """
        Exception handler for UrlValidationError exceptions.
        Args:
            request (Request): The request object.
            exc (UrlValidationError): The exception that was raised.
        Returns:
            JSONResponse: A JSON response with a 400 Bad Request status code and an error message.
        """
        logging.warning(f"Invalid URLs provided: {exc.invalid_urls}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc),
                "invalid_urls": exc.invalid_urls,
            },
        )
        
    @app.exception_handler(TokenLimitExceededError)
    async def token_limit_exception_handler(request: Request, exc: TokenLimitExceededError):
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