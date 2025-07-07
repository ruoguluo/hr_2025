"""
Company Analysis System
Comprehensive company research and analysis tool
"""

import json
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any, Optional
import re
from googlesearch import search
from bs4 import BeautifulSoup
from website_extractor import WebsiteExtractor
from gemini_wrapper import get_gemini_response
from db_handler import DatabaseHandler

class CompanyAnalyzer:
    def __init__(self):
        self.website_extractor = WebsiteExtractor()

    async def analyze_company(self, company_name: str) -> Dict[str, Any]:
        try:
            # Check database first
            db_handler = DatabaseHandler()
            cached_data = db_handler.get_research_data(company_name)
            analysis_result = {
                "company_name": company_name,
                "company_info": {
                    "Company Group / Parent (if any)": "待补充 🔘",
                    "Company Website": "待补充 🔘", 
                    "LinkedIn Company Page": "待补充 🔘",
                    "Location (HQ)": "待补充 🔘",
                    "Location (Job Site)": "待补充 🔘",
                    "Market Region": "待补充 🔘",
                    "Industry": "待补充 🔘",
                    "Sub-Industry": "待补充 🔘",
                    "Company Stage": "待补充 🔘",
                    "Company Size (Global Headcount)": "待补充 🔘",
                    "Funding Stage (if startup)": "待补充 🔘",
                    "Listed / Private / PE-Owned": "待补充 🔘",
                    "Group Structure Notes": "待补充 🔘"
                },
                "products_services": {
                    "Key Products / Services": "待补充 🔘",
                    "Product / Service Differentiation": "待补充 🔘",
                    "Target Customers": "待补充 🔘",
                    "Technology Focus": "待补充 🔘",
                    "Main Revenue Source": "待补充 🔘",
                    "GTM Strategy": "待补充 🔘"
                },
                "market_comparison": {
                    "技术能力": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "产品定价": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "客户群体": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "市场份额": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "售后服务": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "渠道策略": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    },
                    "数据安全 / 合规": {
                        "行业常规标准": "待补充 🔘",
                        "target_company": "待补充 🔘",
                        "competitor_a": "待补充 🔘",
                        "competitor_b": "待补充 🔘"
                    }
                },
                "research_sources": [],
                "analysis_timestamp": "2025-06-27 15:25:08"
            }
            if cached_data:
                print(f"Found cached data for {company_name}")
                db_handler.close()
                analysis_result = await self.process_research_data(cached_data, analysis_result) 
                return analysis_result
            else:
            
                # If not in database, perform research
                research_data = await self.perform_research(company_name)
                
                # Store the new research data
                stored = db_handler.store_research_data(company_name, research_data)
                if not stored:
                    print(f"Failed to store research data for {company_name} in database")
                
                db_handler.close()
                analysis_result = await self.process_research_data(research_data, analysis_result)  
                return analysis_result
            
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return {}

    async def perform_research(self, company_name: str) -> Dict[str, Any]:
        """
        Perform multi-source research on the company
        """
        research_tasks = []
        
        try:
            # Web search for basic company information
            # Get basic company information
            try:
                basic_info = await self.search_basic_company_info(company_name)
            except Exception as e:
                print(f"Error getting basic info: {str(e)}")
                basic_info = {}
            
            # Search for financial and business information  
            try:
                financial_info = await self.search_financial_info(company_name)
            except Exception as e:
                print(f"Error getting financial info: {str(e)}")
                financial_info = {}
            
            # Get product and service information
            try:
                product_service_info = await self.search_product_service_info(company_name)
            except Exception as e:
                print(f"Error getting product/service info: {str(e)}")
                product_service_info = {}
            
            # Search for industry information
            try:
                industry_info = await self.search_industry_info(company_name)
            except Exception as e:
                print(f"Error getting industry info: {str(e)}")
                industry_info = {}
            
            # Get industry company information
            try:
                industry_company_info = await self.search_industry_company_info(company_name)
            except Exception as e:
                print(f"Error getting industry company info: {str(e)}")
                industry_company_info = {}
            
            # Get competitor information
            try:
                competitor_company_info = await self.search_competitor_company_info(company_name)
            except Exception as e:
                print(f"Error getting competitor info: {str(e)}")
                competitor_company_info = {}
            
            # Combine all research data
            research_data = {
                "basic_info": basic_info,
                "financial_info": financial_info, 
                "industry_info": industry_info,
                "product_service_info": product_service_info,
                "industry_company_info": industry_company_info,
                "competitor_company_info": competitor_company_info
            }

            # Store research data in database
            db_handler = DatabaseHandler()
            stored = db_handler.store_research_data(company_name, research_data)
            if not stored:
                print(f"Failed to store research data for {company_name} in database")
            db_handler.close()
            
            return research_data
            
        except Exception as e:
            print(f"Research error: {str(e)}")
            return {}

    async def search_basic_company_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for basic company information
        """ 
        query = f"""
        Give me the following information about "{company_name}":
        - Website
        - Headquarters
        - Industry
        - LinkedIn page
        - Parent company (if any)
        - Description
        - Market region

        Respond only in the following JSON format, without any extra text:
        {{
        "company_name": "",
        "website": "",
        "headquarters": "",
        "industry": "",
        "linkedin_page": "",
        "parent_company": "",
        "description": "",
        "market_region": ""
        }}
        """
        response = get_gemini_response(query)
        print("basic info:" + response)
        return json.loads(response)

    async def search_financial_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for financial and business information
        """
        query = f"""
        Give me the following information about "{company_name}":
        - Company Size 
        - Funding Stage 
        - Listing Status
        - Revenue

        Respond only in the following JSON format, without any extra text:
        {{
        "company_size": "",
        "funding_stage": "",
        "listing_status": "",
        "revenue": ""
        }}
        """
        response = get_gemini_response(query)
        return json.loads(response)

    async def search_product_service_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for product and service information
        """
        query = f"""
        Give me the following information about "{company_name}":
        - Key Products / Services
        - Target Customers (B2B / B2C / Govt)
        - Technology Focus (if applicable)
        - Main Revenue Source
        - GTM Strategy

        Respond only in the following JSON format, without any extra text:
        {{
        "key_products_services": "",
        "target_customers": "",
        "technology_focus": "",
        "main_revenue_source": "",
        "gtm_strategy": ""
        }}
        """
        response = get_gemini_response(query)
        return json.loads(response)
    
    async def search_industry_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for industry and competitive information
        """
        query = f"""
        Firt I want to to know the industry that {company_name} is it.

        Give me the following information about the industry:
        - pricing strategy
        - after-sales service
        - customer base
        - market share
        - competitive landscape
        - Data Security and Compliance
        - channel strategy

        Respond ONLY in the following JSON format, without any extra text:
        {{
            "pricing_strategy": "",
            "after_sales_service": "",
            "customer_base": "",
            "market_share": "",
            "competitive_landscape": "",
            "data_security_compliance": "",
            "channel_strategy": ""
        }}
        """
        
        response = get_gemini_response(query)
        print("industry info:" + response)
        return json.loads(response)

    async def search_industry_company_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for industry and competitive information
        """
        query = f"""
        Give me the following information about the {company_name}:
        - pricing strategy
        - after-sales service
        - customer base
        - market share
        - competitive landscape
        - Data Security and Compliance
        - channel strategy

        Respond only in the following JSON format, without any extra text:
        {{
            "pricing_strategy": "",
            "after_sales_service": "",
            "customer_base": "",
            "market_share": "",
            "competitive_landscape": "",
            "data_security_compliance": "",
            "channel_strategy": ""
        }}
        """
        response = get_gemini_response(query)
        return json.loads(response)
        
    async def search_competitor_company_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for industry and competitive information
        """

        query = f"""
        Give me two competitors of {company_name}

        Give the following information for the first competitor and the second competitor
        - pricing strategy
        - after-sales service
        - customer base
        - market share
        - competitive landscape
        - Data Security and Compliance
        - channel strategy

        Respond only in the following JSON format, without any extra text:
        {{
            "first competitor": {{
            "pricing_strategy": "",
            "after_sales_service": "",
            "customer_base": "",
            "market_share": "",
            "competitive_landscape": "",
            "data_security_compliance": "",
            "channel_strategy": ""
            }}, 
            "second competitor": {{
            "pricing_strategy": "",
            "after_sales_service": "",
            "customer_base": "",
            "market_share": "",
            "competitive_landscape": "",
            "data_security_compliance": "",
            "channel_strategy": ""
            }}
        }}
        """
        response = get_gemini_response(query)
        #print(f"""""======\n{response}\n=====\n""")
        return json.loads(response)
    
    async def process_research_data(self, research_data: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process research data and populate analysis result
        """
        try:
            # Process basic info
            if research_data.get("basic_info"):
                basic = research_data["basic_info"]
                if basic.get("website"):
                    analysis_result["company_info"]["Company Website"] = basic["website"]
                if basic.get("headquarters"):
                    analysis_result["company_info"]["Location (HQ)"] = basic["headquarters"]
                if basic.get("industry"):
                    analysis_result["company_info"]["Industry"] = basic["industry"]
                if basic.get("parent_company"):
                    analysis_result["company_info"]["Company Group / Parent (if any)"] = basic["parent_company"]
                if basic.get("linkedin_page"):
                    analysis_result["company_info"]["LinkedIn Company Page"] = basic["linkedin_page"]
                if basic.get("market_region"):
                    analysis_result["company_info"]["Market Region"] = basic["market_region"]
            
            # Process financial info
            if research_data.get("financial_info"):
                financial = research_data["financial_info"]
                if financial.get("company_size"):
                    analysis_result["company_info"]["Company Size (Global Headcount)"] = financial["company_size"]
                if basic.get("description"):
                    analysis_result["products_services"]["Product / Service Differentiation"] = basic["description"]
                if financial.get("funding_stage"):
                    analysis_result["company_info"]["Funding Stage (if startup)"] = financial["funding_stage"]
                if financial.get("listing_status"):
                    analysis_result["company_info"]["Listed / Private / PE-Owned"] = financial["listing_status"]
            
            if research_data.get("product_service_info"):
                search_product_service_info = research_data.get("product_service_info")
                if search_product_service_info.get("key_products_services"):
                    analysis_result["products_services"]["Key Products / Services"] = search_product_service_info["key_products_services"]
                if search_product_service_info.get("target_customers"):
                    analysis_result["products_services"]["Target Customers"] = search_product_service_info["target_customers"]
                if search_product_service_info.get("technology_focus"):
                    analysis_result["products_services"]["Technology Focus"] = search_product_service_info["technology_focus"]
                if search_product_service_info.get("main_revenue_source"):
                    analysis_result["products_services"]["Main Revenue Source"] = search_product_service_info["main_revenue_source"]
                if search_product_service_info.get("gtm_strategy"):
                    analysis_result["products_services"]["GTM Strategy"] = search_product_service_info["gtm_strategy"]

            # Process industry info
            if research_data.get("industry_info"):
                industry = research_data["industry_info"]
                analysis_result["market_comparison"]["产品定价"]["行业常规标准"] = industry["pricing_strategy"]
                analysis_result["market_comparison"]["售后服务"]["行业常规标准"] = industry["after_sales_service"]
                analysis_result["market_comparison"]["客户群体"]["行业常规标准"] = industry["customer_base"]
                analysis_result["market_comparison"]["市场份额"]["行业常规标准"] = industry["market_share"]
                analysis_result["market_comparison"]["技术能力"]["行业常规标准"] = industry["competitive_landscape"]
                analysis_result["market_comparison"]["数据安全 / 合规"]["行业常规标准"] = industry["data_security_compliance"]
                analysis_result["market_comparison"]["渠道策略"]["行业常规标准"] = industry["channel_strategy"]

                target_company = research_data["industry_company_info"] 
                analysis_result["market_comparison"]["产品定价"]["target_company"] = target_company["pricing_strategy"]
                analysis_result["market_comparison"]["售后服务"]["target_company"] = target_company["after_sales_service"]
                analysis_result["market_comparison"]["客户群体"]["target_company"] = target_company["customer_base"]
                analysis_result["market_comparison"]["市场份额"]["target_company"] = target_company["market_share"]
                analysis_result["market_comparison"]["技术能力"]["target_company"] = target_company["competitive_landscape"]
                analysis_result["market_comparison"]["数据安全 / 合规"]["target_company"] = target_company["data_security_compliance"]
                analysis_result["market_comparison"]["渠道策略"]["target_company"] = target_company["channel_strategy"]

                competitor1 = research_data["competitor_company_info"]["first competitor"]
                analysis_result["market_comparison"]["产品定价"]["competitor_a"] = competitor1["pricing_strategy"]
                analysis_result["market_comparison"]["售后服务"]["competitor_a"] = competitor1["after_sales_service"]
                analysis_result["market_comparison"]["客户群体"]["competitor_a"] = competitor1["customer_base"]
                analysis_result["market_comparison"]["市场份额"]["competitor_a"] = competitor1["market_share"]
                analysis_result["market_comparison"]["技术能力"]["competitor_a"] = competitor1["competitive_landscape"]
                analysis_result["market_comparison"]["数据安全 / 合规"]["competitor_a"] = competitor1["data_security_compliance"]
                analysis_result["market_comparison"]["渠道策略"]["competitor_a"] = competitor1["channel_strategy"]
                
                competitor2 = research_data["competitor_company_info"]["second competitor"]
                analysis_result["market_comparison"]["产品定价"]["competitor_b"] = competitor2["pricing_strategy"]
                analysis_result["market_comparison"]["售后服务"]["competitor_b"] = competitor2["after_sales_service"]
                analysis_result["market_comparison"]["客户群体"]["competitor_b"] = competitor2["customer_base"]
                analysis_result["market_comparison"]["市场份额"]["competitor_b"] = competitor2["market_share"]
                analysis_result["market_comparison"]["技术能力"]["competitor_b"] = competitor2["competitive_landscape"]
                analysis_result["market_comparison"]["数据安全 / 合规"]["competitor_b"] = competitor2["data_security_compliance"]
                analysis_result["market_comparison"]["渠道策略"]["competitor_b"] = competitor2["channel_strategy"]

            # Add research sources
            analysis_result["research_sources"] = [
                "Web search results",
                "Company official sources",
                "Financial databases",
                "Industry reports"
            ]

            #print(analysis_result)

            return analysis_result
            
        except Exception as e:
            print(f"Data processing error: {str(e)}")
            # Add research sources
        analysis_result["research_sources"] = [
            "Web search results",
            "Company official sources",
            "Financial databases",
            "Industry reports"
        ]

        return analysis_result

    def generate_analysis_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate formatted analysis report
        """
        company_name = analysis_result["company_name"]
        
        report = f"""
# Company Analysis Report: {company_name}

## 📌 Company Information Table

| Field | Value |
|-------|-------|
"""
        
        # Add company info table
        for key, value in analysis_result["company_info"].items():
            report += f"| {key} | {value} |\n"
        
        report += f"""
## 📌 Products & Services Information

| Field | Value |
|-------|-------|
"""
        
        # Add products/services table
        for key, value in analysis_result["products_services"].items():
            report += f"| {key} | {value} |\n"
        
        report += f"""
## 📊 Product/Service Market Comparison Table

| 维度 | 行业常规标准 / 主流做法 | {company_name} | 行业头部公司A | 行业头部公司B |
|------|--------------------------|----------------|----------------|----------------|
"""
        
        # Add market comparison table
        for dimension, data in analysis_result["market_comparison"].items():
            report += f"| {dimension} | {data['行业常规标准']} | {data['target_company']} | {data['competitor_a']} | {data['competitor_b']} |\n"
        
        report += f"""
## 📣 Research Sources
"""
        
        for source in analysis_result["research_sources"]:
            report += f"- {source}\n"
        
        report += f"""
## 📅 Analysis Date
{analysis_result["analysis_timestamp"]}

---
*Note: Fields marked with 【待补充 🔘】 require additional information or manual input.*
"""
        
        return report

# Example usage function
async def analyze_company_main(company_name: str) -> Dict[str, Any]:
    """
    Main function to analyze a company
    """
    analyzer = CompanyAnalyzer()
    result = await analyzer.analyze_company(company_name)
    return result

if __name__ == "__main__":
    # Test the analyzer
    import asyncio
    
    async def test():
        result = await analyze_company_main("Tesla")
        analyzer = CompanyAnalyzer()
        report = analyzer.generate_analysis_report(result)
        print(report)
    
    asyncio.run(test())
