import asyncio
import aiohttp
import pytest
from company_analyzer import CompanyAnalyzer

async def main():
    # Initialize the CompanyAnalyzer
    analyzer = CompanyAnalyzer()
    
    # Create aiohttp session
    async with aiohttp.ClientSession() as session:
        analyzer.session = session
        
        # Test company name
        test_company = "Tesla"
    
        try:
            # Call the search_basic_company_info method
            result = await analyzer.search_basic_company_info(test_company)
            
            # Print the results in a formatted way
            print(f"\nResults for {test_company}:")
            print("-" * 50)
            for key, value in result.items():
                print(f"{key}: {value}")
                
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            # Close the WebsiteExtractor session
            await analyzer.extractor.close()
            # Close the main session
            if analyzer.session and not analyzer.session.closed:
                await analyzer.session.close()

@pytest.mark.asyncio
async def test_search_competitor_company_info():
    # Initialize the analyzer
    analyzer = CompanyAnalyzer()
    
    # Create aiohttp session
    async with aiohttp.ClientSession() as session:
        analyzer.session = session
        
        # Test company name
        test_company = "Tesla"
        
        try:
            # Call the method
            result = await analyzer.search_competitor_company_info(test_company)
            
            # Assert the result is a dictionary
            assert isinstance(result, dict), "Result should be a dictionary"
            
            # Assert the dictionary has two competitors
            assert "first competitor" in result, "Result should have 'first competitor' key"
            assert "second competitor" in result, "Result should have 'second competitor' key"
            
            # Expected keys for each competitor
            expected_keys = {
                "pricing_strategy",
                "after_sales_service",
                "customer_base",
                "market_share",
                "competitive_landscape",
                "data_security_compliance",
                "channel_strategy"
            }
            
            # Check first competitor
            first_competitor = result["first competitor"]
            assert isinstance(first_competitor, dict), "First competitor should be a dictionary"
            assert set(first_competitor.keys()) == expected_keys, "First competitor should have all expected keys"
            assert all(isinstance(value, str) for value in first_competitor.values()), "All values should be strings"
            
            # Check second competitor
            second_competitor = result["second competitor"]
            assert isinstance(second_competitor, dict), "Second competitor should be a dictionary"
            assert set(second_competitor.keys()) == expected_keys, "Second competitor should have all expected keys"
            assert all(isinstance(value, str) for value in second_competitor.values()), "All values should be strings"
                
        finally:
            # Close the WebsiteExtractor session
            await analyzer.extractor.close()
            # Close the main session
            if analyzer.session and not analyzer.session.closed:
                await analyzer.session.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])