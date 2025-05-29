class TokenLimitExceededError(Exception):
    """
    Exception raised when the number of tokens in the input exceeds the allowed limit.
    Attributes:
        actual_tokens (int): The actual number of tokens in the input.
        max_tokens (int): The maximum allowed number of tokens.
    """
    def __init__(self, actual_tokens, max_tokens):
        message = f"Input has {actual_tokens} tokens, which exceeds the limit of {max_tokens}."
        super().__init__(message)
