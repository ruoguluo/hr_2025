export interface CompanyInfo extends Record<string, string> {
  "Company Group / Parent (if any)": string;
  "Company Website": string;
  "LinkedIn Company Page": string;
  "Location (HQ)": string;
  "Location (Job Site)": string;
  "Market Region": string;
  "Industry": string;
  "Sub-Industry": string;
  "Company Stage": string;
  "Company Size (Global Headcount)": string;
  "Funding Stage (if startup)": string;
  "Listed / Private / PE-Owned": string;
  "Group Structure Notes": string;
}

export interface ProductsServices extends Record<string, string> {
  "Key Products / Services": string;
  "Product / Service Differentiation": string;
  "Target Customers": string;
  "Technology Focus": string;
  "Main Revenue Source": string;
  "GTM Strategy": string;
}

export interface MarketComparisonItem {
  "行业常规标准": string;
  "target_company": string;
  "competitor_a": string;
  "competitor_b": string;
}

export interface MarketComparison {
  "技术能力": MarketComparisonItem;
  "产品定价": MarketComparisonItem;
  "客户群体": MarketComparisonItem;
  "市场份额": MarketComparisonItem;
  "售后服务": MarketComparisonItem;
  "渠道策略": MarketComparisonItem;
  "数据安全 / 合规": MarketComparisonItem;
}

export interface AnalysisResult {
  company_name: string;
  company_info: CompanyInfo;
  products_services: ProductsServices;
  market_comparison: MarketComparison;
  research_sources: string[];
  analysis_timestamp: string;
}

export interface AnalysisState {
  isLoading: boolean;
  error: string | null;
  result: AnalysisResult | null;
}
