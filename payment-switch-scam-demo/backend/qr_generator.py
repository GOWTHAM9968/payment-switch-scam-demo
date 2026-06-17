import qrcode
import io
import base64
import re
from upi_parser import UPIParser

class QRGenerator:
    """Generate QR codes for UPI payments"""
    
    @staticmethod
    def create_qr_image(data, box_size=10, border=2):
        """Create QR code image and return as base64"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
        except Exception as e:
            print(f"Error creating QR: {e}")
            return None
    
    @staticmethod
    def generate_scam_qr(attacker_vpa, amount, scam_type="refund"):
        """
        Generate scam QR code
        """
        # Create deceptive link
        deceptive = UPIParser.create_deceptive_upi_link(
            attacker_vpa=attacker_vpa,
            amount=amount,
            scam_type=scam_type
        )
        
        # Generate QR
        qr_image = QRGenerator.create_qr_image(deceptive["upi_link"], box_size=12)
        
        # Parse
        parsed = UPIParser.parse_upi_link(deceptive["upi_link"])
        
        return {
            "success": True,
            "qr_image": qr_image,
            "upi_link": deceptive["upi_link"],
            "parsed": parsed,
            "deception": deceptive["deception"],
            "attacker": {
                "vpa": attacker_vpa,
                "amount": amount
            }
        }