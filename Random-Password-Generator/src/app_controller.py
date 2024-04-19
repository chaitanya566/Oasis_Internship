from src.Text_copy import LinkCopier
from src.login_handler import LoginHandler
from src.database_interaction import DatabaseManager
from PyQt5.QtWidgets import QMessageBox
from src.password_generator import PasswordGenerator
from src.Password_strength import PasswordStrengthChecker

class AppController:
    def __init__(self, 
                username_input,
                email_input, 
                password_input, 
                re_password_input,
                username_input_login, 
                pass_input_login,
                Sign_Up_info_after_check,
                login_info_after_check, 
                user_name_display,
                github_link_button,
                linkedin_link_button,
                Easy_char_box,
                Medium_char_box,
                Hard_char_box,
                VHard_char_box,
                Pass_complexity,
                Input_pass_Lineedit,
                Pass_create_label,
                your_passwords_db,
                Input_password_check,
                length_check,
                complexity_check,
                common_p_check,
                scc_check,
                final_review_check
                ):
        self.Input_password_check=Input_password_check
        self.length_check=length_check
        self.complexity_check=complexity_check
        self.common_p_check=common_p_check
        self.scc_check=scc_check
        self.final_review_check=final_review_check
        self.your_passwords_db=your_passwords_db
        self.username_input = username_input
        self.email_input = email_input
        self.password_input = password_input
        self.re_password_input = re_password_input
        self.username_input_login = username_input_login
        self.pass_input_login = pass_input_login
        self.login_info_after_check = login_info_after_check
        self.Sign_Up_info_after_check=Sign_Up_info_after_check
        self.user_name_display = user_name_display
        self.github_link_button = github_link_button
        self.linkedin_link_button = linkedin_link_button
        self.Pass_create_label=Pass_create_label
        self.link_copier = LinkCopier()
        self.db_manager = DatabaseManager(host='127.0.0.1', user='root', password='saradhi@2005', database='rrg', app_controller=self)
        self.login_handler = LoginHandler(self.db_manager)
        self.checker = PasswordStrengthChecker()

        self.Pass_complexity = Pass_complexity
        self.Easy_char_box = Easy_char_box
        self.Medium_char_box = Medium_char_box
        self.Hard_char_box = Hard_char_box
        self.VHard_char_box = VHard_char_box
        self.Input_pass_Lineedit = Input_pass_Lineedit

        self.complexity_level = 'Easy'
        self.easy_chars = False
        self.medium_chars = False
        self.hard_chars = False
        self.vhard_chars = False
        self.length = 8  # Default length

        self.Pass_complexity.currentIndexChanged.connect(self.update_complexity)
        self.Easy_char_box.stateChanged.connect(self.update_easy_chars)
        self.Medium_char_box.stateChanged.connect(self.update_medium_chars)
        self.Hard_char_box.stateChanged.connect(self.update_hard_chars)
        self.VHard_char_box.stateChanged.connect(self.update_vhard_chars)

        self.Pass_create_label=Pass_create_label



    def process_password_strength(self):
        password = self.Input_password_check.text()
        result = self.checker.check_password_strength(password, self.length_check, self.complexity_check, self.common_p_check, self.scc_check)
        self.final_review_check.setText(result)

    def Copy_password(self):
        # Get the password from the label
        generated_password = self.Pass_create_label.text()
        
        # Extract the password part
        password_start_index = generated_password.find(":") + 1
        password = generated_password[password_start_index:].strip()

        # Call the method to copy password to label
        self.link_copier.copy_password_to_label(password)
    
    def update_complexity(self, index):
        self.complexity_level = self.Pass_complexity.currentText()

    def update_easy_chars(self, state):
        self.easy_chars = self.Easy_char_box.isChecked()

    def update_medium_chars(self, state):
        self.medium_chars = self.Medium_char_box.isChecked()

    def update_hard_chars(self, state):
        self.hard_chars = self.Hard_char_box.isChecked()

    def update_vhard_chars(self, state):
        self.vhard_chars = self.VHard_char_box.isChecked()


    def update_length(self):
        text = self.Input_pass_Lineedit.text()
        try:
            self.length = int(text)
        except ValueError:
            # If the input cannot be converted to an integer, display a warning message
            self.show_message("Input Error", "Please enter a valid integer for password length.")
            # Raise a ValueError to stop the flow of execution
            raise ValueError("Invalid input for password length.")

    def generate_password(self):
        try:
            # Create an instance of PasswordGenerator
            self.update_length()

            generator = PasswordGenerator(
                Pass_create_label=self.Pass_create_label,
                length=self.length,
                easy_chars=self.easy_chars,
                medium_chars=self.medium_chars,
                hard_chars=self.hard_chars,
                vhard_chars=self.vhard_chars,
                complexity_level=self.complexity_level
            )
            generator.generate_password()
            generated_password = generator.Pass_create_label.text()

            # Retrieve the username from the 'UserName_Display' label
            username_display = self.user_name_display.text()

            # If the username is "Guest", do not continue
            if username_display == "Guest":
                print("Username is 'Guest'. Not continuing.")
                return

            # Find the index of ':' to extract password
            password_start_index = generated_password.find(":") + 1

            # Check if ':' is found in the generated password
            if password_start_index == 0:
                print("Password not found. Cannot call the function.")
                return generated_password

            # Extract password from the generated password
            password = generated_password[password_start_index:].strip()

            # Call the store_password function with the retrieved username and password
            self.db_manager.store_password(username_display, password)

            # Retrieve all passwords stored for this user
            passwords = self.db_manager.get_user_passwords(username_display)
            if passwords:
                self.display_user_passwords(passwords)
            else:
                self.your_passwords_db.setText("Create passwords for storage in the database and view them here! 🔒")
                
        except ValueError as e:
            # Catch the ValueError raised by update_length and handle it gracefully
            print(e)
            return None


    def get_passwords_from_label(self):
        # Retrieve the text from the label
        passwords_text = self.your_passwords_db.text()

        # Copy the passwords to clipboard
        self.link_copier.copy_password_to_label(passwords_text)

    def sign_up(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        re_password = self.re_password_input.text()

        if password == re_password:
            self.db_manager.create_account(username, email, password)
        else:
            self.Sign_Up_info_after_check.setText("Passwords do not match")


    def login(self):
        username = self.username_input_login.text()
        password = self.pass_input_login.text()

        user_data = self.db_manager.get_user_by_username(username)

        if user_data is not None:
            stored_password = user_data[3]
            if password == stored_password:
                self.login_info_after_check.setText("Login successful")
                self.user_name_display.setText(username)
                # Retrieve all passwords stored for this user
                passwords = self.db_manager.get_user_passwords(username)
                if passwords:
                    self.display_user_passwords(passwords)
                else:
                    self.your_passwords_db.setText("Create passwords for storage in the database and view them here! 🔒")
            else:
                self.login_info_after_check.setText("Incorrect password")
        else:
            self.login_info_after_check.setText("Username not found")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.setText(message)
        msg_box.setFixedSize(400, 200)
        msg_box.exec_()

    def account_created_message(self):
        title = "Success"
        message = "Account created successfully!"
        self.show_message(title, message)

    def display_user_passwords(self, passwords):
        if passwords:
            password_text = "\n".join(password[0] for password in passwords)
            self.your_passwords_db.setText(password_text)
        else:
            self.your_passwords_db.setText("Create passwords for storage in the database and view them here! 🔒")