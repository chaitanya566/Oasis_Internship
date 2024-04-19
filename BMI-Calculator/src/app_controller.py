# app_controller.py
from src.login_handler import LoginHandler
from src.database_interaction import DatabaseManager
from PyQt5.QtWidgets import QMessageBox
from src.bmi_calculator import BMICalculator
from src.link_copier import LinkCopier
from src.bmi_analysis import BMIAnalysis
from PyQt5.QtWidgets import QVBoxLayout

class AppController:
    def __init__(self, 
                username_input,
                email_input, 
                password_input, 
                re_password_input,
                username_input_login, 
                pass_input_login, 
                login_info_after_check, 
                user_name_display,
                height_input_bmi, 
                weight_input_bmi, 
                units_height, 
                units_weight, 
                info_bmi_after_check,
                github_link_button,
                linkedin_link_button,
                analysis_graph_frame, 
                Analysis_info):
        
        
        self.analysis_graph_frame = analysis_graph_frame
        self.Analysis_info = Analysis_info
        self.analysis_graph_layout = QVBoxLayout()
        self.analysis_graph_frame.setLayout(self.analysis_graph_layout)
        self.username_input = username_input
        self.email_input = email_input
        self.password_input = password_input
        self.re_password_input = re_password_input
        self.username_input_login = username_input_login
        self.pass_input_login = pass_input_login
        self.login_info_after_check = login_info_after_check
        self.user_name_display = user_name_display
        self.github_link_button = github_link_button
        self.linkedin_link_button = linkedin_link_button
        self.link_copier = LinkCopier()
        self.db_manager = DatabaseManager(host='127.0.0.1', user='root', password='saradhi@2005', database='bmi_db', app_controller=self)
        self.login_handler = LoginHandler(self.db_manager)
        self.bmi_analysis = BMIAnalysis(self.db_manager)
        self.height_input_bmi = height_input_bmi
        self.weight_input_bmi = weight_input_bmi
        self.units_height = units_height
        self.units_weight = units_weight
        self.info_bmi_after_check = info_bmi_after_check
        self.bmi_calculator = BMICalculator(self.db_manager)

    def show_bmi_history(self):
        self.bmi_analysis.show_bmi_history(self.user_name_display, self.analysis_graph_frame, self.Analysis_info)


    def calculate_bmi(self):
        try:
            height = float(self.height_input_bmi.text())
            weight = float(self.weight_input_bmi.text())

            # Validate if input is numeric
            if not (isinstance(height, (int, float)) and isinstance(weight, (int, float))):
                raise ValueError("Height and weight must be numeric.")

            units_height = self.units_height.currentText()
            units_weight = self.units_weight.currentText()

            self.bmi_calculator.calculate_bmi(height, weight, units_height, units_weight, self.info_bmi_after_check,self.user_name_display)
        except ValueError as e:
            if "could not convert string to float" in str(e):
                self.info_bmi_after_check.setText("Character detected. Height and weight must be numeric.")
            else:
                self.info_bmi_after_check.setText("Wrong input")
            self.bmi_calculator.show_message("Error", str(e))
    
    def sign_up(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        re_password = self.re_password_input.text()

        if password == re_password:
            self.db_manager.create_account(username, email, password)
        else:
            print("Passwords do not match.")


    def login(self):
        username = self.username_input_login.text()
        password = self.pass_input_login.text()

        user_data = self.db_manager.get_user_by_username(username)

        if user_data is not None:
            stored_password = user_data[3]
            if password == stored_password:
                self.login_info_after_check.setText("Login successful")
                self.user_name_display.setText(username)
                self.bmi_analysis.show_bmi_history(self.user_name_display, self.analysis_graph_frame, self.Analysis_info)
            else:
                self.login_info_after_check.setText("Incorrect password")
        else:
            self.login_info_after_check.setText("Username not found")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        message += "\n\nCheck the database credentials and restart the app."

        msg_box.setText(message)
        msg_box.setFixedSize(400, 200)
        msg_box.exec_()