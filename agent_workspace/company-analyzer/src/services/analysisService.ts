import { AnalysisResult } from '../types/analysis';

class AnalysisService {
  //private baseUrl = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5001/api';

  private baseUrl = 'http://107.182.26.178:5001';

  async analyzeCompany(companyName: string): Promise<AnalysisResult> {
    try {
      // First try to use the real API if available
      const response = await fetch(`${this.baseUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company_name: companyName }),
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.log('API not available, using mock data');
    }

    // Fall back to mock data if API is not available
    return this.getMockAnalysis(companyName);
  }

  async updateField(section: string, field: string, value: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/update_field`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ section, field, value }),
      });

      return response.ok;
    } catch (error) {
      console.log('API not available for field update');
      return true; // Return true for mock scenario
    }
  }

  async exportAnalysis(analysisResult: AnalysisResult): Promise<string> {
    try {
      const response = await fetch(`${this.baseUrl}/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ analysis_result: analysisResult }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.report;
      }
    } catch (error) {
      console.log('API not available for export');
    }

    // Fall back to basic export
    return this.generateBasicReport(analysisResult);
  }

  private getMockAnalysis(companyName: string): AnalysisResult {
    return {
      company_name: companyName,
      company_info: {
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
      products_services: {
        "Key Products / Services": "待补充 🔘",
        "Product / Service Differentiation": "待补充 🔘",
        "Target Customers": "待补充 🔘",
        "Technology Focus": "待补充 🔘",
        "Main Revenue Source": "待补充 🔘",
        "GTM Strategy": "待补充 🔘"
      },
      market_comparison: {
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
      research_sources: [
        "Web search results",
        "Company official sources",
        "Financial databases",
        "Industry reports"
      ],
      analysis_timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')
    };
  }

  private generateBasicReport(analysisResult: AnalysisResult): string {
    const { company_name, company_info, products_services, market_comparison } = analysisResult;
    
    let report = `# Company Analysis Report: ${company_name}\n\n`;
    
    report += `## 📌 Company Information Table\n\n`;
    report += `| Field | Value |\n|-------|-------|\n`;
    Object.entries(company_info).forEach(([key, value]) => {
      report += `| ${key} | ${value} |\n`;
    });
    
    report += `\n## 📌 Products & Services Information\n\n`;
    report += `| Field | Value |\n|-------|-------|\n`;
    Object.entries(products_services).forEach(([key, value]) => {
      report += `| ${key} | ${value} |\n`;
    });
    
    report += `\n## 📊 Product/Service Market Comparison Table\n\n`;
    report += `| 维度 | 行业常规标准 / 主流做法 | ${company_name} | 行业头部公司A | 行业头部公司B |\n`;
    report += `|------|--------------------------|----------------|----------------|----------------|\n`;
    Object.entries(market_comparison).forEach(([dimension, data]) => {
      report += `| ${dimension} | ${data['行业常规标准']} | ${data['target_company']} | ${data['competitor_a']} | ${data['competitor_b']} |\n`;
    });
    
    report += `\n## 📅 Analysis Date\n${analysisResult.analysis_timestamp}\n\n`;
    report += `---\n*Note: Fields marked with 【待补充 🔘】 require additional information or manual input.*\n`;
    
    return report;
  }
}

export const analysisService = new AnalysisService();
