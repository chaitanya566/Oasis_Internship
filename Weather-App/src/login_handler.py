# login_handler.py

from src.database_interaction import DatabaseManager

class LoginHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def login(self, username_input_login, pass_input_login, login_info_after_check, user_name_display):
        username = username_input_login.text()
        password = pass_input_login.text()

        user_data = self.db_manager.get_user_by_username(username)

        if user_data is not None:
            stored_password = user_data[3]
            if password == stored_password:
                login_info_after_check.setText("Login successful")
                user_name_display.setText(username)
            else:
                login_info_after_check.setText("Incorrect password")
        else:
            login_info_after_check.setText("Username not found")
