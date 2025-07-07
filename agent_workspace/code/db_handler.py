import mysql.connector
from typing import Dict, Any
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="107.182.26.178",
            user="root",
            password="secret-2025",
            database="hr_db"
        )
        self.cursor = self.connection.cursor(buffered=True)
        self.create_tables()

    def create_tables(self):
        # Companies table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Basic info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS basic_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            website VARCHAR(255),
            headquarters VARCHAR(255),
            industry VARCHAR(255),
            linkedin_page VARCHAR(255),
            parent_company VARCHAR(255),
            description TEXT,
            market_region VARCHAR(255),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        # Financial info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            company_size VARCHAR(255),
            funding_stage VARCHAR(255),
            listing_status VARCHAR(255),
            revenue VARCHAR(255),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        # Industry info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS industry_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            pricing_strategy TEXT,
            after_sales_service TEXT,
            customer_base TEXT,
            market_share TEXT,
            competitive_landscape TEXT,
            data_security_compliance TEXT,
            channel_strategy TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        # Product service info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_service_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            key_products_services TEXT,
            target_customers TEXT,
            technology_focus TEXT,
            main_revenue_source TEXT,
            gtm_strategy TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        # Industry company info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS industry_company_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            pricing_strategy TEXT,
            after_sales_service TEXT,
            customer_base TEXT,
            market_share TEXT,
            competitive_landscape TEXT,
            data_security_compliance TEXT,
            channel_strategy TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        # Competitor info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitor_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            competitor_type ENUM('first', 'second'),
            pricing_strategy TEXT,
            after_sales_service TEXT,
            customer_base TEXT,
            market_share TEXT,
            competitive_landscape TEXT,
            data_security_compliance TEXT,
            channel_strategy TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        """)

        self.connection.commit()

    def store_research_data(self, company_name: str, research_data: Dict[str, Any]):
        try:
            # Insert company
            self.cursor.execute(
                "INSERT INTO companies (company_name) VALUES (%s)",
                (company_name,)
            )
            company_id = self.cursor.lastrowid

            # Store basic info
            if research_data.get("basic_info"):
                self.cursor.execute("""
                INSERT INTO basic_info (
                    company_id, website, headquarters, industry, linkedin_page,
                    parent_company, description, market_region
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    company_id,
                    research_data["basic_info"].get("website"),
                    research_data["basic_info"].get("headquarters"),
                    research_data["basic_info"].get("industry"),
                    research_data["basic_info"].get("linkedin_page"),
                    research_data["basic_info"].get("parent_company"),
                    research_data["basic_info"].get("description"),
                    research_data["basic_info"].get("market_region")
                ))

            # Store financial info
            if research_data.get("financial_info"):
                self.cursor.execute("""
                INSERT INTO financial_info (
                    company_id, company_size, funding_stage, listing_status, revenue
                ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    company_id,
                    research_data["financial_info"].get("company_size"),
                    research_data["financial_info"].get("funding_stage"),
                    research_data["financial_info"].get("listing_status"),
                    research_data["financial_info"].get("revenue")
                ))

            # Store industry info
            if research_data.get("industry_info"):
                self.cursor.execute("""
                INSERT INTO industry_info (
                    company_id, pricing_strategy, after_sales_service, customer_base,
                    market_share, competitive_landscape, data_security_compliance, channel_strategy
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    company_id,
                    research_data["industry_info"].get("pricing_strategy"),
                    research_data["industry_info"].get("after_sales_service"),
                    research_data["industry_info"].get("customer_base"),
                    research_data["industry_info"].get("market_share"),
                    research_data["industry_info"].get("competitive_landscape"),
                    research_data["industry_info"].get("data_security_compliance"),
                    research_data["industry_info"].get("channel_strategy")
                ))

            # Store product service info
            if research_data.get("product_service_info"):
                self.cursor.execute("""
                INSERT INTO product_service_info (
                    company_id, key_products_services, target_customers, technology_focus,
                    main_revenue_source, gtm_strategy
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    company_id,
                    research_data["product_service_info"].get("key_products_services"),
                    research_data["product_service_info"].get("target_customers"),
                    research_data["product_service_info"].get("technology_focus"),
                    research_data["product_service_info"].get("main_revenue_source"),
                    research_data["product_service_info"].get("gtm_strategy")
                ))

            # Store industry company info
            if research_data.get("industry_company_info"):
                self.cursor.execute("""
                INSERT INTO industry_company_info (
                    company_id, pricing_strategy, after_sales_service, customer_base,
                    market_share, competitive_landscape, data_security_compliance, channel_strategy
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    company_id,
                    research_data["industry_company_info"].get("pricing_strategy"),
                    research_data["industry_company_info"].get("after_sales_service"),
                    research_data["industry_company_info"].get("customer_base"),
                    research_data["industry_company_info"].get("market_share"),
                    research_data["industry_company_info"].get("competitive_landscape"),
                    research_data["industry_company_info"].get("data_security_compliance"),
                    research_data["industry_company_info"].get("channel_strategy")
                ))

            # Store competitor info
            if research_data.get("competitor_company_info"):
                # Store first competitor
                if research_data["competitor_company_info"].get("first competitor"):
                    self.cursor.execute("""
                    INSERT INTO competitor_info (
                        company_id, competitor_type, pricing_strategy, after_sales_service,
                        customer_base, market_share, competitive_landscape,
                        data_security_compliance, channel_strategy
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        company_id,
                        'first',
                        research_data["competitor_company_info"]["first competitor"].get("pricing_strategy"),
                        research_data["competitor_company_info"]["first competitor"].get("after_sales_service"),
                        research_data["competitor_company_info"]["first competitor"].get("customer_base"),
                        research_data["competitor_company_info"]["first competitor"].get("market_share"),
                        research_data["competitor_company_info"]["first competitor"].get("competitive_landscape"),
                        research_data["competitor_company_info"]["first competitor"].get("data_security_compliance"),
                        research_data["competitor_company_info"]["first competitor"].get("channel_strategy")
                    ))

                # Store second competitor
                if research_data["competitor_company_info"].get("second competitor"):
                    self.cursor.execute("""
                    INSERT INTO competitor_info (
                        company_id, competitor_type, pricing_strategy, after_sales_service,
                        customer_base, market_share, competitive_landscape,
                        data_security_compliance, channel_strategy
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        company_id,
                        'second',
                        research_data["competitor_company_info"]["second competitor"].get("pricing_strategy"),
                        research_data["competitor_company_info"]["second competitor"].get("after_sales_service"),
                        research_data["competitor_company_info"]["second competitor"].get("customer_base"),
                        research_data["competitor_company_info"]["second competitor"].get("market_share"),
                        research_data["competitor_company_info"]["second competitor"].get("competitive_landscape"),
                        research_data["competitor_company_info"]["second competitor"].get("data_security_compliance"),
                        research_data["competitor_company_info"]["second competitor"].get("channel_strategy")
                    ))

            self.connection.commit()
            return True

        except Exception as e:
            print(f"Error storing research data: {str(e)}")
            self.connection.rollback()
            return False

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_research_data(self, company_name: str) -> Dict[str, Any]:
        try:
            # Check if company exists
            self.cursor.execute(
                "SELECT id FROM companies WHERE company_name = %s",
                (company_name,)
            )
            company = self.cursor.fetchone()
            if not company:
                return None
            
            company_id = company[0]
            research_data = {}
            
            # Get basic info
            self.cursor.execute(
                "SELECT * FROM basic_info WHERE company_id = %s",
                (company_id,)
            )
            basic = self.cursor.fetchone()
            if basic:
                research_data['basic_info'] = {
                    'website': basic[2],
                    'headquarters': basic[3],
                    'industry': basic[4],
                    'linkedin_page': basic[5],
                    'parent_company': basic[6],
                    'description': basic[7],
                    'market_region': basic[8]
                }
            
            # Get financial info
            self.cursor.execute(
                "SELECT * FROM financial_info WHERE company_id = %s",
                (company_id,)
            )
            financial = self.cursor.fetchone()
            if financial:
                research_data['financial_info'] = {
                    'company_size': financial[2],
                    'funding_stage': financial[3],
                    'listing_status': financial[4],
                    'revenue': financial[5]
                }
            
            # Get industry info
            self.cursor.execute(
                "SELECT * FROM industry_info WHERE company_id = %s",
                (company_id,)
            )
            industry = self.cursor.fetchone()
            if industry:
                research_data['industry_info'] = {
                    'pricing_strategy': industry[2],
                    'after_sales_service': industry[3],
                    'customer_base': industry[4],
                    'market_share': industry[5],
                    'competitive_landscape': industry[6],
                    'data_security_compliance': industry[7],
                    'channel_strategy': industry[8]
                }
            
            # Get product service info
            self.cursor.execute(
                "SELECT * FROM product_service_info WHERE company_id = %s",
                (company_id,)
            )
            product = self.cursor.fetchone()
            if product:
                research_data['product_service_info'] = {
                    'key_products_services': product[2],
                    'target_customers': product[3],
                    'technology_focus': product[4],
                    'main_revenue_source': product[5],
                    'gtm_strategy': product[6]
                }
            
            # Get industry company info
            self.cursor.execute(
                "SELECT * FROM industry_company_info WHERE company_id = %s",
                (company_id,)
            )
            industry_company = self.cursor.fetchone()
            if industry_company:
                research_data['industry_company_info'] = {
                    'pricing_strategy': industry_company[2],
                    'after_sales_service': industry_company[3],
                    'customer_base': industry_company[4],
                    'market_share': industry_company[5],
                    'competitive_landscape': industry_company[6],
                    'data_security_compliance': industry_company[7],
                    'channel_strategy': industry_company[8]
                }
            
            # Get competitor info
            self.cursor.execute(
                "SELECT * FROM competitor_info WHERE company_id = %s",
                (company_id,)
            )
            competitors = self.cursor.fetchall()
            if competitors:
                research_data['competitor_company_info'] = {}
                for competitor in competitors:
                    competitor_type = competitor[2] + ' competitor'
                    research_data['competitor_company_info'][competitor_type] = {
                        'pricing_strategy': competitor[3],
                        'after_sales_service': competitor[4],
                        'customer_base': competitor[5],
                        'market_share': competitor[6],
                        'competitive_landscape': competitor[7],
                        'data_security_compliance': competitor[8],
                        'channel_strategy': competitor[9]
                    }

            print(research_data)
            
            return research_data
            
        except Exception as e:
            print(f"Error retrieving research data: {str(e)}")
            return None