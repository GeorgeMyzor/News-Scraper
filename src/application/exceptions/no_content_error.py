class NoContentError(Exception):
    """
    Exception raised when an article has no content or the HTML page is malformed.
    This can occur when the URL provided does not lead to a valid article or the content
    cannot be extracted due to missing or malformed HTML elements.
    Attributes:
        invalid_url (str): The URL that caused the error.
    """
    def __init__(self, invalid_url: str):
        message = f"The following URL has no content or should fix their HTML page: {invalid_url}"
        super().__init__(message)
        self.invalid_url = invalid_url
