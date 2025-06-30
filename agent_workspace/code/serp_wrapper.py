import requests
from openai import OpenAI

# 配置你的 API Key
SERPAPI_KEY = "30656a79e3a1abbe7cf871aaafb472a96d14aa73f472e949a5103744e659f201"
OPENAI_API_KEY = "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"
client = OpenAI(
    api_key=OPENAI_API_KEY
)

def search_serpapi(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def extract_snippets(serp_data):
    results = serp_data.get("organic_results", [])
    return "\n\n".join([f"{r['title']}:\n{r.get('snippet', '')}" for r in results if 'snippet' in r])

def ask_openai(company_name, snippets):
    prompt = f"""
You are a professional business analyst. Based on the following search results about "{company_name}", extract key company information and return it in this exact JSON format:

{{
    "company_name": "",
    "website": "",
    "headquarters": "",
    "industry": "",
    "linkedin_page": "",
    "parent_company": "",
    "description": ""
}}

Search Results:
{snippets}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You return only structured JSON company info."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def get_company_info(company_name):
    print(f"🔎 Searching Google for: {company_name}")
    serp_data = search_serpapi(f"{company_name} site:linkedin.com OR site:crunchbase.com OR site:{company_name.lower()}.com")
    snippets = extract_snippets(serp_data)
    print("🧠 Generating JSON via OpenAI...")
    return ask_openai(company_name, snippets)

# 示例调用
if __name__ == "__main__":
    company_name = "Tiktok"
    company_json = get_company_info(company_name)
    print("📦 Company Info JSON:\n")
    print(company_json)
