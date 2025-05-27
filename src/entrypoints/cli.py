import re
import sys
from src.abstrations.dependencies import get_use_case

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python app.py <URL>")
        sys.exit(1)
    
    input = sys.argv[1]
    pattern = r'https?://\S+|www\.\S+'
    are_urls = re.match(pattern, input)

    use_case = get_use_case(are_urls)
    use_case.process(input)
    
if __name__ == "__main__":
    main()