import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database, app_controller):
        self.app_controller = app_controller
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established successfully!")
        except mysql.connector.Error as e:
            error_message = f"Error connecting to the database: {e}"
            print(error_message)
            error_message += "\n\nCheck the database credentials and restart the app."
            self.app_controller.show_message("Error", error_message)

    def create_account(self, username, email, password):
        try:
            sql = "INSERT INTO UserInfo (Username, Email, Password) VALUES (%s, %s, %s)"
            values = (username, email, password)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Account created successfully!")
            self.app_controller.show_message("Success", "Account created successfully!")
        except mysql.connector.Error as e:
            error_message = f"Error creating account: {e}"
            print(error_message)
            self.app_controller.show_message("Error", error_message)

    def get_user_by_username(self, username):
        try:
            sql = "SELECT * FROM UserInfo WHERE Username = %s"
            self.cursor.execute(sql, (username,))
            user_data = self.cursor.fetchone()
            return user_data
        except mysql.connector.Error as e:
            error_message = f"Error fetching user data: {e}"
            print(error_message)
            self.app_controller.show_message("Error", error_message)
            return None