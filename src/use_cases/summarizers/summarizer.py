import os
from openai import OpenAI

def generate_summary(article):
    """
    Generates a summary for an article using OpenAI's GPT-4 API.
    """
    content = truncate_content(article.content, max_tokens=100)
    prompt = (
        f"Summarize the following news article in key points:\n\n"
        f"Title: {article.title}\n\n"
        f"Content: {content}\n\n"
        f"Summary:"
    )
    
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        response = client.responses.create(
            model="gpt-3.5-turbo", 
            instructions= "You are a helpful assistant that summarizes news articles.",
            input=prompt,
            temperature=0.7,  
        )

        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None
    
def truncate_content(content, max_tokens=2048):
    """
    Truncate content to fit GPT token limits, ensuring the model can process it.
    """
    words = content.split()
    if len(words) > max_tokens:
        return " ".join(words[:max_tokens]) + "..."
    return content