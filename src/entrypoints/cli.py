import re
import sys
import asyncio
from src.abstractions.dependencies import get_use_case

URL_PATTERN = r'https?://\S+|www\.\S+'

async def main(get_use_case_func) -> None:        
    print("Welcome to the Article Scrapper App!")
    print("Enter one or more URLs (space-separated) to summarize the articles.")
    print("Or enter a query to find related articles in the database.")
    print("Type 'exit' or 'quit' to close the program.\n")

    while True:
        try:
            input_text = input("Enter URL(s) or query: ").strip()

            if input_text.lower() in ('exit', 'quit'):
                print("Exiting the application. Goodbye!")
                break  

            is_url_input = contains_only_urls(input_text)

            use_case = get_use_case_func(is_url_input)
            await use_case.process_async(input_text)

        except Exception as error:
            print(f"An error occurred: {error}")
            print("Please try again.")
        print() 

def contains_only_urls(input_text: str) -> bool:
    urls = re.findall(URL_PATTERN, input_text)
    return len(urls) > 0 and len(urls) == len(input_text.split())
  
if __name__ == "__main__":    
    try:
        asyncio.run(main(get_use_case))
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)