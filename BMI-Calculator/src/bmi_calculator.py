# bmi_calculator.py

from PyQt5.QtWidgets import QMessageBox
from datetime import date
class BMICalculator:
    def __init__(self,db_manager):
        self.db_manager = db_manager

    def calculate_bmi(self, height, weight, units_height, units_weight, info_label,username_display):
        try:


            if height < 0:
                raise ValueError("Height cannot be negative")
            # Check if weight is negative
            if weight < 0:
                raise ValueError("Weight cannot be negative")
                

            # Convert height to meters
            if units_height == "m":
                height_meters = height
                if height < 0.5 or height >2.5 :
                    raise ValueError("the height value is impractical in real life \n(0.2-2.5 m values accepted)")
            elif units_height == "In":

                if height < 20 or height >100 :
                    raise ValueError("the height value is impractical in real life \n(20-100 In values accepted)")
                
                height_meters = height * 0.0254  # Convert inches to meters
            else:
                raise ValueError("Invalid height units")

            # Convert weight to kilograms
            if units_weight == "Kg":
                weight_kg = weight
                if weight < 10 or weight > 500:
                    raise ValueError("the weight value is impractical in real life \n(10-500 kg values accepted)")
            elif units_weight == "lb":
                if weight < 22 or weight > 1100:
                    raise ValueError("the weight value is impractical in real life \n(22-1100 lb values accepted)")
                weight_kg = weight * 0.453592  # Convert pounds to kilograms
            else:
                raise ValueError("Invalid weight units")
            
            
                
            
                
            
            # Calculate BMI
            bmi = weight_kg / (height_meters ** 2)

            if bmi < 18.5:
                color = "blue"  # Underweight
                bmi_range_text = "(Underweight)"
                suggestion_text = "You are Underweight, consider increasing your calorie intake through nutritious foods and incorporating strength training exercises to build muscle mass."
            elif 18.5 <= bmi <= 24.9:
                color = "green"  # Healthy Weight
                bmi_range_text = "(Healthy Weight)"
                suggestion_text = "You are within the healthy BMI range. Maintain your current lifestyle with balanced nutrition and regular physical activity."
            elif 25.0 <= bmi <= 29.9:
                color = "orange"  # Overweight
                bmi_range_text = "(Overweight)"
                suggestion_text = "You are Overweight, focus on a balanced diet with portion control, increase physical activity levels, and consider consulting a healthcare professional for personalized advice."
            else:
                color = "red"  # Obese
                bmi_range_text = "(Obese)"
                suggestion_text = "You are Obese, it's recommended to focus on weight loss through a combination of calorie-controlled diet, regular exercise, and consulting with a healthcare professional for personalized guidance."

            # Set text color based on BMI range
# Set text color based on BMI range
            info_label.setText(f"<font color={color}>BMI: {bmi:.2f}</font>")
            existing_username = username_display.text()
            existing_username = existing_username.split('(')[0].strip()
            username_display.setText(f"{existing_username} {bmi_range_text}")

            # Set color for the username display label
            username_display.setStyleSheet(f"color: {color};")
            # Create a QMessageBox for the suggestion
            suggestion_box = QMessageBox()
            suggestion_box.setIcon(QMessageBox.Information)
            suggestion_box.setWindowTitle("BMI Suggestion")
            suggestion_box.setText(suggestion_text)
            suggestion_box.exec_()


            if username_display.text() != "Guest":
                user_id = self.db_manager.get_user_id(username_display.text())
                today = date.today().strftime("%Y-%m-%d")
                self.db_manager.insert_bmi_record(user_id, height, weight, bmi, today)


        except ValueError as e:
            info_label.setText("Wrong input")

            # Show error message
            self.show_message("Error", str(e))

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
