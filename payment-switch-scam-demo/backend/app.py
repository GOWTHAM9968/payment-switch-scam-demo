from flask import Flask, render_template, request, jsonify
from qr_generator import QRGenerator
from upi_parser import UPIParser
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate-scam-qr', methods=['POST'])
def generate_scam_qr():
    """Generate scam QR code"""
    try:
        data = request.json
        
        attacker_vpa = data.get('attacker_vpa', '5653216548@okhdfcbank')
        amount = data.get('amount', 2000)
        scam_type = data.get('scam_type', 'refund')
        
        result = QRGenerator.generate_scam_qr(
            attacker_vpa=attacker_vpa,
            amount=amount,
            scam_type=scam_type
        )
        
        return jsonify({
            "success": True,
            "qr_image": result["qr_image"],
            "upi_link": result["upi_link"],
            "parsed": result["parsed"],
            "deception": result["deception"],
            "attacker": result["attacker"]
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')