import re
import requests
from PyQt5.QtGui import QPixmap

class PasswordStrengthChecker:
    def __init__(self):
        pass
    
    def check_password_strength(self, password, length_check, complexity_check, common_p_check, scc_check):
        strength = 0
        # Length check
        if len(password) >= 8:
            length_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/check-circle.png"))
            strength += 1
        else:
            length_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/x-circle.png"))
        
        # Complexity check
        if re.search(r'[A-Z]', password) and \
           re.search(r'[a-z]', password) and \
           re.search(r'\d', password) and \
           re.search(r'[!@#$%^&*()_+{}|:"<>?~\-=[\];\',./]', password):
            complexity_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/check-circle.png"))
            strength += 1
        else:
            complexity_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/x-circle.png"))
        
        # Avoid common patterns
        if not self.is_common_password(password):
            common_p_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/check-circle.png"))
            strength += 1
        else:
            common_p_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/x-circle.png"))
        
        # Avoid sequential characters
        if not re.search(r'(123|abc)', password, re.IGNORECASE):
            scc_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/check-circle.png"))
            strength += 1
        else:
            scc_check.setPixmap(QPixmap("Qss/icons/fd5028/feather/x-circle.png"))
        
        # Additional checks can be added here
        
        if strength == 4:
            return "Very strong"
        elif strength == 3:
            return "Strong"
        elif strength == 1:
            return "Barely Acceptable"
        else:
            return "Very Weak"

    def is_common_password(self, password):
        url = "https://api.pwnedpasswords.com/range/" + password[:5]
        response = requests.get(url)
        if response.status_code == 200:
            hashes = response.text.split('\n')
            hash_suffix = password.upper()[5:].encode('utf-8')
            for hash in hashes:
                if hash.startswith(hash_suffix.decode('utf-8')):
                    return True
        return False
