from google import genai
from google.genai import types
import time

# Configure the client
client = genai.Client(api_key='AIzaSyDcfB0FgMo1_gKo-_-GRnofKd7timm9W_4')

def get_gemini_response(query: str) -> str:
    """Get a response from Gemini model with Google Search grounding.
    
    Args:
        query: The question to ask the model.
        
    Returns:
        The model's response text.
    """
    # Define the grounding tool
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    # Configure generation settings
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    # Make the request with retry
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
                config=config,
            )
            return clean_markdown_code_block(response.text)
        except Exception as e:
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                print(f"All attempts failed. Last error: {str(e)}")
                raise  # Re-raise the last exception 

def clean_markdown_code_block(text: str) -> str:
    # Strip Markdown-style ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        # Remove the first line (e.g., ```json)
        lines = text.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return text.strip()

if __name__ == "__main__":
    # Example usag
    company_name = "Tesla"
    query = f"""
    Give me the following information about "{company_name}":
    - Website
    - Headquarters
    - Industry
    - LinkedIn page
    - Parent company (if any)
    - Description

    Respond only in the following JSON format:
    {{
      "company_name": "",
      "website": "",
      "headquarters": "",
      "industry": "",
      "linkedin_page": "",
      "parent_company": "",
      "description": ""
    }}
    """
    response = get_gemini_response(query)
    print(response)