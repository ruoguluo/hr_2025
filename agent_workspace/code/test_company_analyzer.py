import asyncio
import aiohttp
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

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())