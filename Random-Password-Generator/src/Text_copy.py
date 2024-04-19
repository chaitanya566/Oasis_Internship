
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QClipboard

class LinkCopier:
    def __init__(self):
        pass

    def copy_github_link(self):
        github_link = "https://github.com/chaitanya566"
        clipboard = QApplication.clipboard()
        clipboard.setText(github_link, mode=QClipboard.Clipboard)
        QMessageBox.information(None, "GitHub Link Copied", "GitHub link has been copied to the clipboard.")

    def copy_linkedin_link(self):
        linkedin_link = "https://www.linkedin.com/in/chaitanya-saradhi-eerla-0793132a1/"
        clipboard = QApplication.clipboard()
        clipboard.setText(linkedin_link, mode=QClipboard.Clipboard)
        QMessageBox.information(None, "LinkedIn Link Copied", "LinkedIn link has been copied to the clipboard.")
    
    
    def copy_password_to_label(self, password):
        # Check if there's any password present
        if password:
            # Copy the password to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            QMessageBox.information(None, "Password Copied", "Password has been copied to the clipboard.")
        else:
            # If no password is present, show a message
            QMessageBox.warning(None, "Error", "No password found. Please generate a password first.")
