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
            self.app_controller.show_message("Error", error_message)


    def get_bmi_history(self, user_id):
        try:
            sql = "SELECT BMIScore, DateRecorded FROM BMIRecords WHERE UserID = %s"
            self.cursor.execute(sql, (user_id,))
            bmi_history = self.cursor.fetchall()
            return bmi_history
        except mysql.connector.Error as e:
            print(f"Error fetching BMI history: {e}")
            return []
        
        
    def get_user_id(self, username):
        sql = "SELECT UserID FROM Users WHERE Username = %s"
        self.cursor.execute(sql, (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None

    def insert_bmi_record(self, user_id, height, weight, bmi_score, date_recorded):
        sql = "INSERT INTO BMIRecords (UserID, Height, Weight, BMIScore, DateRecorded) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, height, weight, bmi_score, date_recorded)
        self.cursor.execute(sql, values)
        self.connection.commit()
        print("BMI record inserted successfully!")

    def create_account(self, username, email, password):
        try:
            sql = "INSERT INTO UserInfo (Username, Email, Password) VALUES (%s, %s, %s)"
            values = (username, email, password)
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Account created successfully!")
            # Call the show_message function directly
            self.app_controller.show_message("Success", "Account created successfully!")
        except mysql.connector.Error as e:
            error_message = f"Error creating account: {e}"
            print(error_message)
            self.app_controller.show_message("Error", error_message)
            
    def get_user_by_username(self, username):
        try:
            sql = "SELECT * FROM Users WHERE Username = %s"
            self.cursor.execute(sql, (username,))
            user_data = self.cursor.fetchone()
            return user_data
        except Exception as e:
            print("Error fetching user data:", e)
            return None
        
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
