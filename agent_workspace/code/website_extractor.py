import aiohttp
from bs4 import BeautifulSoup
import re

class WebsiteExtractor:
    def __init__(self):
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def extract_from_url(self, url):
        try:
            session = await self._get_session()
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, "html.parser")
                    return soup
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def find_contact_info(self, soup):
        # Try to find contact page
        contact_links = soup.find_all("a", href=re.compile(r"contact", re.IGNORECASE))
        if contact_links:
            # For simplicity, we'll just parse the current page for now.
            # A more robust solution would follow the contact link.
            pass

        # Look for address patterns
        address_pattern = re.compile(r"\d+\s+([A-Z][a-z]+\s+)+([A-Z][a-z]+,)\s+[A-Z]{2}\s+\d{5}")
        addresses = soup.find_all(text=address_pattern)
        if addresses:
            return addresses[0]
        return None

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
