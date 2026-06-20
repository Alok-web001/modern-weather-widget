Modern Weather Widget 🌍

A beautiful, responsive desktop weather application built using Python and PyQt5. The application fetches real-time meteorological data using the open-source Open-Meteo API.

Features ✨
1. Two-Step API Workflow: Automatically converts city names to precise latitude/longitude coordinates via the Geocoding API, then requests live forecast metrics.
2. Modern UI/UX: Styled using customized Qt Style Sheets (QSS) featuring an elegant dark mode dashboard architecture.
3. Smooth Animations: Features a fluid fade-in animation using `QPropertyAnimation` whenever new weather data updates on the screen.
4. Keyboard Shortcuts: Allows users to fetch data instantly by pressing the `Enter` key.

Tech Stack 🛠️
1. Language: Python 3
2. GUI Framework: PyQt5
3. Networking: Requests library
4. Data Provider: Open-Meteo API

Setup Instructions 🚀
1. Clone or download this repository.
2. Install the necessary dependencies:
   ```bash
   pip install PyQt5 requests
