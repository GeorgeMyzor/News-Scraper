from pydantic import HttpUrl, ValidationError, TypeAdapter

from application.exceptions.url_validation_error import UrlValidationError

def validate_urls(urls: list[str]) -> None:
    """
    Validates the provided URLs.
    Args:
        urls (list[str]): List of URLs to validate.
    Raises:
        ValueError: If any URL is invalid.
    """
    invalid_urls = []
    
    for url in urls:
        try:
            TypeAdapter(HttpUrl).validate_python(url)
        except ValidationError:
            invalid_urls.append(url)

    if invalid_urls:
        raise UrlValidationError(invalid_urls)