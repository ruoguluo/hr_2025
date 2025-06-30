#!/usr/bin/env python3
"""
Simple HTTP API Server for Company Analysis
Uses built-in Python libraries to avoid dependency issues
"""

import json
import asyncio
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from datetime import datetime

# Add the code directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

try:
    from company_analyzer import CompanyAnalyzer, analyze_company_main
    ANALYZER_AVAILABLE = True
except ImportError:
    print("Warning: CompanyAnalyzer not available, using mock data only")
    ANALYZER_AVAILABLE = False

class CompanyAnalysisHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/health':
            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "Company Analysis API",
                "analyzer_available": ANALYZER_AVAILABLE
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        if parsed_path.path == '/api/analyze':
            self.handle_analyze(data)
        elif parsed_path.path == '/api/update_field':
            self.handle_update_field(data)
        elif parsed_path.path == '/api/export':
            self.handle_export(data)
        else:
            self.send_error(404)

    def handle_analyze(self, data):
        """Handle company analysis requests"""
        if 'company_name' not in data:
            self.send_error(400, "Missing company_name")
            return

        company_name = data['company_name'].strip()
        if not company_name:
            self.send_error(400, "Company name cannot be empty")
            return

        try:
            if ANALYZER_AVAILABLE:
                # Use the real analyzer
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(analyze_company_main(company_name))
                finally:
                    loop.close()
            else:
                # Fall back to mock data
                result = self.get_mock_analysis(company_name)

            # Update timestamp
            result["analysis_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_error(500, f"Analysis failed: {str(e)}")

    def handle_update_field(self, data):
        """Handle field update requests"""
        required_fields = ['section', 'field', 'value']
        if not all(field in data for field in required_fields):
            self.send_error(400, "Missing required fields: section, field, value")
            return

        response = {
            "success": True,
            "message": "Field updated successfully",
            "updated": {
                "section": data['section'],
                "field": data['field'],
                "value": data['value'],
                "timestamp": datetime.now().isoformat()
            }
        }

        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_export(self, data):
        """Handle export requests"""
        if 'analysis_result' not in data:
            self.send_error(400, "Missing analysis_result")
            return

        try:
            analysis_result = data['analysis_result']
            report = self.generate_report(analysis_result)

            response = {
                "report": report,
                "timestamp": datetime.now().isoformat(),
                "format": "markdown"
            }

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_error(500, f"Export failed: {str(e)}")

    def get_mock_analysis(self, company_name):
        """Generate mock analysis data"""
        return {
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
            "research_sources": [
                "Web search results",
                "Company official sources",
                "Financial databases",
                "Industry reports"
            ],
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def generate_report(self, analysis_result):
        """Generate markdown report"""
        company_name = analysis_result["company_name"]
        
        report = f"# Company Analysis Report: {company_name}\n\n"
        
        report += "## 📌 Company Information Table\n\n"
        report += "| Field | Value |\n|-------|-------|\n"
        for key, value in analysis_result["company_info"].items():
            report += f"| {key} | {value} |\n"
        
        report += "\n## 📌 Products & Services Information\n\n"
        report += "| Field | Value |\n|-------|-------|\n"
        for key, value in analysis_result["products_services"].items():
            report += f"| {key} | {value} |\n"
        
        report += "\n## 📊 Product/Service Market Comparison Table\n\n"
        report += f"| 维度 | 行业常规标准 / 主流做法 | {company_name} | 行业头部公司A | 行业头部公司B |\n"
        report += "|------|--------------------------|----------------|----------------|----------------|\n"
        for dimension, data in analysis_result["market_comparison"].items():
            report += f"| {dimension} | {data['行业常规标准']} | {data['target_company']} | {data['competitor_a']} | {data['competitor_b']} |\n"
        
        report += f"\n## 📅 Analysis Date\n{analysis_result['analysis_timestamp']}\n\n"
        report += "---\n*Note: Fields marked with 【待补充 🔘】 require additional information or manual input.*\n"
        
        return report

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass

def run_server(port=5000):
    """Run the HTTP server"""
    server = HTTPServer(('0.0.0.0', port), CompanyAnalysisHandler)
    print(f"Starting Company Analysis API Server on port {port}...")
    print(f"Server available at: http://localhost:{port}")
    print("API endpoints:")
    print("  GET  /api/health - Health check")
    print("  POST /api/analyze - Analyze company")
    print("  POST /api/update_field - Update analysis field")
    print("  POST /api/export - Export analysis report")
    print(f"Company Analyzer Available: {ANALYZER_AVAILABLE}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == '__main__':
    run_server()
