from src.Text_copy import LinkCopier
from src.login_handler import LoginHandler
from src.database_interaction import DatabaseManager
from PyQt5.QtWidgets import QMessageBox
from src.get_weather_details import WeatherAPI_Details
from PyQt5.QtGui import QPixmap

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
                city_name_input_main,

                city_name_main,
                main_weather_main,
                min_temp_main,
                feels_like_main,
                max_temp_main,
                wind_speed_main,
                cloud_coverage_main,
                wind_speed_settings,
                temp_units_settings,
                visablity_main,
                main_weather_image_main
                ):
        

        self.main_weather_image_main=main_weather_image_main
        self.visablity_main=visablity_main
        self.email_input = email_input
        self.username_input=username_input
        self.password_input = password_input
        self.re_password_input = re_password_input
        self.username_input_login = username_input_login
        self.pass_input_login = pass_input_login
        self.login_info_after_check = login_info_after_check
        self.Sign_Up_info_after_check=Sign_Up_info_after_check
        self.user_name_display = user_name_display
        self.github_link_button = github_link_button
        self.linkedin_link_button = linkedin_link_button
        self.link_copier = LinkCopier()
        self.db_manager = DatabaseManager(host='127.0.0.1', user='root', password='saradhi@2005', database='weather', app_controller=self)
        self.login_handler = LoginHandler(self.db_manager)
        self.API_key="f880252b9eb340fddd34dfb03c731b6f"
        self.weather_details = WeatherAPI_Details(self.API_key)
        self.city_name_input_main=city_name_input_main
        self.wind_speed_settings = wind_speed_settings
        self.temp_units_settings = temp_units_settings

        self.city_name_main=city_name_main
        self.main_weather_main=main_weather_main
        self.weather_data=None
        self.min_temp_main=min_temp_main
        self.feels_like_main=feels_like_main
        self.max_temp_main=max_temp_main
        self.wind_speed_main=wind_speed_main
        self.cloud_coverage_main=cloud_coverage_main





    def weather(self):
        try:
            city_input = self.city_name_input_main.text()
            
            if not city_input:
                raise ValueError("Please enter a city name.")
            self.weather_data = self.weather_details.get_weather(city_input)
            self.city_name_main.setText(city_input)
            self.visablity_main.setText(str(self.weather_data['visibility'])+" m")
            main_weather = self.weather_data['weather'][0]['main']
            if main_weather == 'Clouds':
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/cloud.png"))
                main_weather = 'Cloudy'
            elif main_weather == 'Clear':
                main_weather = 'Clear'
                #:/icons/Icons/feather/cloud-rain.png
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/sun.png"))
            elif main_weather == 'Rain':
                main_weather = 'Rainy'
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/cloud-rain.png"))
            elif main_weather == 'Drizzle':
                main_weather = 'Drizzling'
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/cloud-lightning.png"))
            elif main_weather == 'Thunderstorm':
                main_weather = 'Thunderstorm'
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/cloud-drizzle.png"))
            elif main_weather == 'Snow':
                main_weather = 'Snowy'
                self.main_weather_image_main.setPixmap(QPixmap("Qss/icons/e60540/feather/cloud-snow.png"))

            self.main_weather_main.setText(main_weather)
            
            self.set_weather_label()
            if not self.weather_data:
                raise ValueError("Error to featch Data")
        except ValueError as e:
            self.show_message("Error", str(e))

    def btn_weather(self):
        try:
            if self.city_name_main.text() == "Search a city!":
                raise ValueError("Select a city first!")
            else:
                self.set_weather_label()
                self.show_message("Success", "Refresh Successful!l")
        except ValueError as e:
            self.show_message("Error", str(e))


    def btn_weather1(self):
        try:
            if self.city_name_main.text() == "Search a city!":
                raise ValueError("Select a city first!")
            else:
                self.set_weather_label()
                self.show_message("Success", "Successfully Changed!")
        except ValueError as e:
            self.show_message("Error", str(e))

    
    def set_weather_label(self):

            self.weather_details.convert_weather_data(self.weather_data, self.temp_units_settings, self.wind_speed_settings)

            self.weather_details.update_weather_labels(self.weather_data,self.min_temp_main, self.feels_like_main, self.max_temp_main, self.wind_speed_main, self.cloud_coverage_main)



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