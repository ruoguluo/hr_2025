"""
Flask API Server for Company Analysis
Wraps the CompanyAnalyzer class with REST API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import sys
import os
from datetime import datetime

# Add the code directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from company_analyzer import CompanyAnalyzer, analyze_company_main

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global analyzer instance
analyzer = CompanyAnalyzer()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Company Analysis API"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_company():
    """
    Analyze a company and return structured data
    """
    print("Request received for /api/analyze")
    try:
        data = request.get_json()
        
        if not data or 'company_name' not in data:
            return jsonify({
                "error": "Missing company_name in request body"
            }), 400
        
        company_name = data['company_name'].strip()
        company_name = company_name.lower().capitalize()
        
        if not company_name:
            return jsonify({
                "error": "Company name cannot be empty"
            }), 400
        
        # Run the async analysis function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(analyze_company_main(company_name))
            # Update timestamp
            result["analysis_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify(result)
        finally:
            loop.close()
        
    except Exception as e:
        return jsonify({
            "error": f"Analysis failed: {str(e)}"
        }), 500

@app.route('/api/update_field', methods=['POST'])
def update_field():
    """
    Update a specific field in the analysis result
    This endpoint can be used to update editable fields
    """
    try:
        data = request.get_json()
        
        required_fields = ['section', 'field', 'value']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "Missing required fields: section, field, value"
            }), 400
        
        # In a real application, you would save this to a database
        # For now, we'll just return success
        return jsonify({
            "success": True,
            "message": "Field updated successfully",
            "updated": {
                "section": data['section'],
                "field": data['field'],
                "value": data['value'],
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Update failed: {str(e)}"
        }), 500

@app.route('/api/export', methods=['POST'])
def export_analysis():
    """
    Export analysis result as formatted report
    """
    try:
        data = request.get_json()
        
        if not data or 'analysis_result' not in data:
            return jsonify({
                "error": "Missing analysis_result in request body"
            }), 400
        
        analysis_result = data['analysis_result']
        
        # Generate report using the existing method
        report = analyzer.generate_analysis_report(analysis_result)
        
        return jsonify({
            "report": report,
            "timestamp": datetime.now().isoformat(),
            "format": "markdown"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Export failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting Company Analysis API Server...")
    print("Server will be available at: http://localhost:5001")
    print("API endpoints:")
    print("  GET  /api/health - Health check!")
    print("  POST /api/analyze - Analyze company")
    print("  POST /api/update_field - Update analysis field")
    print("  POST /api/export - Export analysis report")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
    # app.run(host='0.0.0.0', port=5001)
