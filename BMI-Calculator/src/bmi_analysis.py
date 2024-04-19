# bmi_analysis.py

from PyQt5.QtWidgets import QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from src.database_interaction import DatabaseManager
from matplotlib.dates import DateFormatter
import numpy as np

class BMIAnalysis:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def show_bmi_history(self, username_display, analysis_graph_frame, label_6):
        username = username_display.text()
        user_id = self.db_manager.get_user_id(username)

        if user_id:
            bmi_history = self.db_manager.get_bmi_history(user_id)
            if bmi_history:
                bmis = [record[0] for record in bmi_history]
                dates = [record[1] for record in bmi_history]

                # Create color map for bars
                colors = plt.cm.viridis(np.linspace(0, 1, len(bmis)))

                # Create bar graph
                fig, ax = plt.subplots()
                ax.bar(dates, bmis, color=colors)
                
                # Format date labels
                ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

                # Adjust spacing of the ticks
                plt.xticks(rotation=45, ha='right')

                ax.set_xlabel('Date')
                ax.set_ylabel('BMI')
                ax.set_title('BMI History')

                # Clear previous plot from frame
                for widget in analysis_graph_frame.findChildren(FigureCanvas):
                    widget.deleteLater()

                # Display graph on frame
                canvas = FigureCanvas(fig)
                layout = analysis_graph_frame.layout()
                layout.addWidget(canvas)
                label_6.setText("")  # Clear "not enough info" label
            else:
                label_6.setText("Not enough info")
        else:
            label_6.setText("User not found")
