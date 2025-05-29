class UrlValidationError(Exception):
    """
    Exception raised when one or more URLs are invalid.
    Attributes:
        invalid_urls (list[str]): List of invalid URLs.
    """
    def __init__(self, invalid_urls: list[str]):
        message = f"One or more URLs are invalid."
        super().__init__(message)
        self.invalid_urls = invalid_urls
