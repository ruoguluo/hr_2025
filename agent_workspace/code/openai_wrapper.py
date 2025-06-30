# new
from openai import OpenAI
import os

# Set your OpenAI API key
#openai.api_key = os.getenv("OPENAI_API_KEY")  # Or just set it directly here
api_key = "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"

client = OpenAI(
    api_key=api_key
)


def get_company_info(company_name):
    # Build the prompt
    user_prompt = f"""
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

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a business data assistant. Return all company data in a structured JSON format."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2  # lower temperature for more factual, consistent output
    )

    # Extract the content from the response
    return response.choices[0].message.content


def main():
    # Example usage
    company_name = "Ark Wealth Management"
    company_info = get_company_info(company_name)
    print(company_info)


if __name__ == "__main__":
    main()
