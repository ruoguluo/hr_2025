import requests
from openai import OpenAI

# 你的 API Keys
SERPAPI_KEY = "30656a79e3a1abbe7cf871aaafb472a96d14aa73f472e949a5103744e659f201"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

def filter_company_results(results):
    #company_keywords = ["linkedin.com/company", "crunchbase.com/organization", "zoominfo.com/c/"]
    company_keywords = ["crunchbase.com/organization"]
    company_results = []
    #print(results);
    for r in results.get("organic_results", []):
        link = r.get("link", "")
        if any(kw in link for kw in company_keywords):
            company_results.append({
                "title": r["title"],
                "link": link,
                "snippet": r.get("snippet", "")
            })
    return company_results


def search_company_candidates(company_name, max_results=5):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{company_name} company site:linkedin.com OR site:crunchbase.com",
        #"q": f"{company_name} company site:crunchbase.com",
        "api_key": SERPAPI_KEY,
        "num": max_results
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    company_results = filter_company_results(data)

    print(f"🎯 Found {len(company_results)} likely company pages:")
    for idx, c in enumerate(company_results):
        print(f"{idx + 1}. {c['title']} — {c['link']}")

    return company_results

def extract_candidates(serp_data):
    print(serp_data);
    candidates = []
    #results = serp_data.get("organic_results", [])
    for r in serp_data:
        title = r.get("title")
        link = r.get("link")
        snippet = r.get("snippet", "")
        if title and link:
            candidates.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })
    return candidates

def display_candidates(candidates):
    print("\n🔍 Multiple companies found. Please select one:")
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c['title']}")
        print(f"   {c['snippet']}")
        print(f"   [Link] {c['link']}\n")

def ask_openai(company_name, selected_snippet):
    prompt = f"""
You are a business analyst assistant. Based on the following search result about "{company_name}", extract the company information and return it in this exact JSON format:

{{
    "company_name": "",
    "website": "",
    "headquarters": "",
    "industry": "",
    "linkedin_page": "",
    "parent_company": "",
    "description": ""
}}

Search Snippet:
{selected_snippet}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You return structured JSON about companies."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def get_company_info(company_name):
    serp_data = search_company_candidates(company_name)
    candidates = extract_candidates(serp_data)

    if not candidates:
        print("❌ No candidates found.")
        return

    display_candidates(candidates)

    try:
        choice = int(input("👉 Enter the number of the company you mean: ")) - 1
        selected = candidates[choice]
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    print(f"\n🧠 Extracting company info from: {selected['title']}")
    print(f"\n{selected['snippet']}")
    json_info = ask_openai(company_name, selected['snippet'])
    print("\n📦 Company Info JSON:\n")
    print(json_info)

# ==== 示例 ====
if __name__ == "__main__":
    user_input = input("🔎 Enter a company name: ")
    get_company_info(user_input)
