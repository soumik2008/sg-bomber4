from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def send_flipkart_otp(phone_number):
    """
    Send OTP request to Flipkart API
    """
    url = "https://2.rome.api.flipkart.com/1/action/view"
    
    headers = {
        "authority": "2.rome.api.flipkart.com",
        "accept": "*/*",
        "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.flipkart.com",
        "referer": "https://www.flipkart.com/",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "x-user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 FKUA/msite/0.0.3/msite/Mobile"
    }
    
    payload = {
        "actionRequestContext": {
            "type": "LOGIN_IDENTITY_VERIFY",
            "loginIdPrefix": "+91",
            "loginId": phone_number,
            "clientQueryParamMap": {"ret": "/"},
            "loginType": "MOBILE",
            "verificationType": "OTP",
            "screenName": "LOGIN_V4_MOBILE",
            "sourceContext": "DEFAULT"
        }
    }
    
    try:
        logger.info(f"Sending OTP request for phone: {phone_number}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        logger.info(f"Response status: {response.status_code}")
        return response.status_code, response.json()
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return None, {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return None, {"error": "Connection error"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None, {"error": str(e)}

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "success": True,
        "status": "active",
        "message": "Flipkart OTP API is running",
        "endpoints": {
            "send_otp": {
                "method": "GET",
                "url": "/spam?number=9876543210",
                "description": "Send OTP to phone number"
            },
            "health": {
                "method": "GET", 
                "url": "/health",
                "description": "Health check endpoint"
            }
        },
        "example": "https://your-domain.vercel.app/spam?number=9876543210",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Flipkart OTP API"
    })

@app.route('/spam', methods=['GET'])
def send_otp():
    """
    Send OTP endpoint
    Usage: /spam?number=9876543210
    """
    try:
        # Get phone number from query parameter
        phone = request.args.get('number', '').strip()
        
        # Log request
        logger.info(f"Received request for phone: {phone}")
        
        # Validate phone number
        if not phone:
            return jsonify({
                "success": False,
                "error": "PHONE_REQUIRED",
                "message": "Phone number is required",
                "usage": "Please use: /spam?number=9876543210",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Remove any leading/trailing spaces and check if it's all digits
        phone = phone.strip()
        if not phone.isdigit():
            return jsonify({
                "success": False,
                "error": "INVALID_FORMAT",
                "message": "Phone number must contain only digits",
                "provided": phone,
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Check length
        if len(phone) != 10:
            return jsonify({
                "success": False,
                "error": "INVALID_LENGTH",
                "message": "Phone number must be exactly 10 digits",
                "provided": phone,
                "length": len(phone),
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Send OTP request
        status_code, response_data = send_flipkart_otp(phone)
        
        # Prepare base response
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "phone": f"+91{phone}",
            "request_id": datetime.now().strftime("%Y%m%d%H%M%S")
        }
        
        # Check if request was successful
        if status_code == 200:
            if response_data and response_data.get("STATUS") == "SUCCESS":
                result["success"] = True
                result["message"] = "OTP sent successfully"
                result["details"] = {
                    "status_code": status_code,
                    "flipkart_status": "SUCCESS"
                }
                return jsonify(result), 200
            else:
                result["message"] = "Flipkart returned unexpected response"
                result["details"] = {
                    "status_code": status_code,
                    "response": response_data
                }
                return jsonify(result), 202
        elif status_code is not None:
            result["message"] = f"Failed with status code: {status_code}"
            result["details"] = {
                "status_code": status_code,
                "response": response_data
            }
            return jsonify(result), status_code
        else:
            result["message"] = "Connection error"
            result["details"] = {
                "error": response_data.get("error", "Unknown error")
            }
            return jsonify(result), 503
            
    except Exception as e:
        logger.error(f"Unexpected error in send_otp: {str(e)}")
        return jsonify({
            "success": False,
            "error": "INTERNAL_ERROR",
            "message": "An internal server error occurred",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "NOT_FOUND",
        "message": "Endpoint not found",
        "available_endpoints": ["/", "/health", "/spam?number=9876543210"],
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "INTERNAL_ERROR",
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
