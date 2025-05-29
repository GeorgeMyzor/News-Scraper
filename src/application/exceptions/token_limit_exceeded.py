class TokenLimitExceeded(Exception):
    def __init__(self, actual_tokens, max_tokens):
        message = f"Input has {actual_tokens} tokens, which exceeds the limit of {max_tokens}."
        super().__init__(message)
