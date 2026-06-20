import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QGraphicsOpacityEffect)
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QFont

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App Widget")
        self.setGeometry(100, 100, 350, 280)
        self.setFixedSize(350, 280) # Locks the window size for a clean widget look

        # Global Application Styling (Modern Dark Theme)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e24;
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            }
            QLineEdit {
                background-color: #2a2a35;
                color: #ffffff;
                border: 2px solid #3a3a4a;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #6c5ce7;
            }
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5b4cc4;
            }
            QPushButton:pressed {
                background-color: #4a3db0;
            }
            QLabel {
                color: #ffffff;
                font-size: 15px;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(15)

        # Title Label
        self.title_label = QLabel("Live Weather", self)
        self.title_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Input Field
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.returnPressed.connect(self.fetch_weather) # Added Enter key shortcut
        self.layout.addWidget(self.city_input)

        # Button
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.get_weather_btn.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.get_weather_btn)

        # Result Label with Opacity Effect for Animation
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        # Setting up the Fade-in Animation configuration
        self.opacity_effect = QGraphicsOpacityEffect(self.result_label)
        self.result_label.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(600) # Duration in milliseconds (0.6 seconds)

        self.setLayout(self.layout)

    def trigger_fade_in(self):
        """Starts the smooth fade-in animation for the text."""
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

    def fetch_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        try:
            # Step 1: Geocoding API
            url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1}
            geo_resp = requests.get(url, params=geo_params, timeout=5)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            
            if not geo_data.get("results"):
                self.result_label.setText("❌ City not found.")
                self.trigger_fade_in()
                return
                
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            actual_name = geo_data["results"][0]["name"]

            # Step 2: Weather API
            weather_url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "timezone": "auto"
            }
            weather_resp = requests.get(weather_url, params=params, timeout=5)
            weather_resp.raise_for_status()
            data = weather_resp.json()

            if "current_weather" in data:
                weather = data["current_weather"]
                temp = weather["temperature"]
                wind = weather["windspeed"]
                
                # Formatted output with modern design elements
                weather_str = f"🌍 {actual_name}\n\n🌡️ Temp: {temp}°C\n💨 Wind: {wind} km/h"
                self.result_label.setText(weather_str)
                self.trigger_fade_in() # Run the fade animation
            else:
                self.result_label.setText("Weather data unavailable.")
                self.trigger_fade_in()

        except Exception as e:
            self.result_label.setText(f"Error connecting to server.")
            self.trigger_fade_in()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec_())