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
    Send OTP request to Flipkart API - exactly like your working code
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
        
        # Try to parse JSON response
        try:
            return response.status_code, response.json()
        except:
            return response.status_code, {"text": response.text}
            
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return 408, {"error": "Request timeout", "message": "The request timed out"}
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return 503, {"error": "Connection error", "message": "Failed to connect to Flipkart"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 500, {"error": str(e), "message": "Internal server error"}

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
            }
        },
        "example": "https://your-domain.vercel.app/spam?number=9876543210",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/spam', methods=['GET'])
def send_otp_endpoint():
    """
    Send OTP endpoint - exactly as you requested
    URL Pattern: /spam?number=9876543210
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
        
        # Clean phone number
        phone = phone.strip()
        
        # Validate phone number format
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
        
        # Send OTP request using your exact function
        status_code, response_data = send_flipkart_otp(phone)
        
        # Prepare response
        result = {
            "timestamp": datetime.now().isoformat(),
            "phone": f"+91{phone}",
            "request_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "success": False
        }
        
        # Check response status
        if status_code == 200:
            result["success"] = True
            result["message"] = "OTP request sent successfully"
            result["status_code"] = status_code
            result["flipkart_response"] = response_data
            
            # Check if OTP was actually sent
            if isinstance(response_data, dict):
                if response_data.get("STATUS") == "SUCCESS":
                    result["otp_status"] = "SUCCESS"
                    result["details"] = "OTP has been sent to the phone number"
                else:
                    result["otp_status"] = "PENDING"
                    result["details"] = "Request sent, waiting for OTP delivery"
            else:
                result["otp_status"] = "UNKNOWN"
                result["details"] = "Request processed by Flipkart"
                
            return jsonify(result), 200
            
        elif status_code == 408:
            result["message"] = "Request timeout - Flipkart server not responding"
            result["error"] = "TIMEOUT"
            result["details"] = response_data
            return jsonify(result), 503
            
        elif status_code == 503:
            result["message"] = "Connection error - Unable to reach Flipkart"
            result["error"] = "CONNECTION_ERROR"
            result["details"] = response_data
            return jsonify(result), 503
            
        else:
            result["message"] = f"Failed with status code: {status_code}"
            result["error"] = "REQUEST_FAILED"
            result["details"] = response_data
            return jsonify(result), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in send_otp_endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": "INTERNAL_ERROR",
            "message": "An internal server error occurred",
            "details": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Flipkart OTP API"
    })

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
