import re
import sys
import asyncio
from src.abstractions.dependencies import get_use_case
from langsmith import traceable

URL_PATTERN = r'https?://\S+|www\.\S+'

@traceable
async def main() -> None:    
    input_text = input("Enter URL(s) (with whitespace in between) or query to find related articles: ").strip()
    if input_text.lower() in ('exit', 'quit'):        
        sys.exit(1)

    urls = re.findall(URL_PATTERN, input_text)    
    is_url_input = len(urls) >= 1

    use_case = get_use_case(is_url_input)
    await use_case.process_async(input_text)
    
if __name__ == "__main__":    
    try:
        asyncio.run(main())
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)