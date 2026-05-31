# 🌤️ SkyPulse — Real-Time Weather Forecast Application

SkyPulse is a Python-based weather forecasting application that provides real-time weather information and 5-day forecasts using the OpenWeatherMap API. The project includes both a Command Line Interface (CLI) and a Flask-powered web application, demonstrating API integration, web development, error handling, and software testing.

## 🔗 Live Demo

https://skypulse-weather-app.onrender.com/


## 🚀 Features

* Real-time weather information for any city
* 5-day weather forecast
* Current temperature, humidity, pressure, visibility, and wind speed
* Command Line Interface (CLI)
* Flask-based web application
* Robust error handling

  * Invalid city names
  * Network connectivity issues
  * Invalid API keys
* Automated testing using pytest
* Environment variable management with `.env`

## 🛠️ Tech Stack

### Programming Language

* Python 3.x

### Libraries & Frameworks

* Flask
* Requests
* Python-Dotenv
* Pytest

### API

* OpenWeatherMap API

### Tools

* Git
* GitHub

## 📂 Project Structure

```text
skypulse-weather-app/
│
├── app.py
├── weather_cli.py
├── templates/
│   └── index.html
├── tests/
│   └── test_weather.py
├── requirements.txt
├── .env.example
├── README.md
└── screenshots/
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aditiborse15/skypulse-weather-app.git
cd skypulse-weather-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file and add your OpenWeatherMap API key:

```env
API_KEY=YOUR_OPENWEATHERMAP_API_KEY
```

Get your free API key from:
https://openweathermap.org/api

### 4. Run the CLI Application

```bash
python weather_cli.py
```

### 5. Run the Flask Web Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

### 6. Run Automated Tests

```bash
pytest tests/
```

## 📸 Screenshots

<img width="816" height="796" alt="image" src="https://github.com/user-attachments/assets/058a4f3a-8835-478a-8075-25f65bc9864f" />


Store images in:

```text
screenshots/
```

## 🎯 Key Learning Outcomes

* REST API Integration
* Flask Web Development
* Environment Variable Management
* JSON Data Processing
* Error Handling and Validation
* Unit Testing with Pytest
* Git & GitHub Version Control

## 🔮 Future Enhancements

* Weather icons and animations
* Search history
* Location-based weather detection
* Dark/Light theme support
* Hourly weather forecasts
* Deployment on Render


