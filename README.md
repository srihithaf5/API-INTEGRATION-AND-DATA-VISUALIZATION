# API-INTEGRATION-AND-DATA-VISUALIZATION

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: PATTEM SRIHITHA

*INTERN ID*:  CT04DY1528

*DOMAIN*:  PYTHON PROGRAMMING

*DURATION*: 4 WEEKS

*MENTOR*: NEELA SANTHOSH KUMAR

*DESCRIPTION ABOUT THIS TASK

API-INTEGRATION-AND-DATA-VISUALIZATION

This project has been developed as part of the CODTECH Internship – Task 1, which focuses on API Integration and Data Visualization using Python. The task demonstrates the ability to integrate with a public API, process the retrieved data, and visualize it using popular Python libraries.

The chosen API is Open-Meteo, a free and reliable weather API that provides forecast data without the need for an authentication key. This makes it very suitable for internship projects and educational purposes. The project uses Python to send requests to the API, parse the response into a structured dataset, and then generate visualizations for easier understanding.

The task has been divided into two major deliverables:

Python Script: A standalone script that fetches data for a given city, saves the data as a CSV file, generates charts, and prints summary statistics.

Streamlit Dashboard: An interactive visualization dashboard that allows users to enter a city name, choose the forecast duration, and view weather trends dynamically.

The solution highlights not only technical skills in Python programming and data handling but also the ability to transform raw API data into meaningful insights through data visualization.

FILE DESCRIPTION

app.py – Provides the user interface with Streamlit where users can input city names and visualize weather data.

weather_fetch_and_viz.py – Runs as a script from the command line, fetches weather data, stores it, and produces visualizations.

outputs/ – Stores the generated files (CSV datasets and PNG figures).

requirements.txt – Ensures reproducibility by listing required packages.

README.md – Documentation for installation, usage, and explanation.

Dependencies include:

requests – For sending API calls.

pandas – For handling and cleaning tabular data.

matplotlib – For generating charts.

streamlit – For building the interactive dashboard.

USAGE

Running the Script

python weather_fetch_and_viz.py --city "Hyderabad" --days 7


This command fetches weather forecast data for 7 days in Hyderabad. The script will:

Save the dataset as a CSV file in outputs/data/.

Generate three charts (temperature, average daily temperature, precipitation) in outputs/figs/.

Print a quick summary (min, max, average values) in the terminal.

Running the Dashboard

streamlit run app.py

The dashboard allows:

Entering a city name.

Choosing forecast days between 3 and 16.

Viewing real-time visualizations such as hourly temperature trends, daily averages, and rainfall totals.

VISUALIZATIONS:

The project produces the following visualizations:

Hourly Temperature Line Chart – Shows variation in temperature with respect to time.

Daily Average Temperature Bar Chart – Highlights overall daily trends.

Daily Precipitation Bar Chart – Summarizes daily rainfall totals.

These visualizations are simple yet effective in understanding weather data at both granular (hourly) and aggregate (daily) levels.

TECHNOLOGIES USED

Python – Core programming language.

Requests – For API calls.

Pandas – Data cleaning and transformation.

Matplotlib – Data visualization library.

Streamlit – Web framework for dashboards.

 DELIVERABLES

Script (weather_fetch_and_viz.py) – Fetches API data, stores it in CSV, generates charts, and prints summary statistics.

Dashboard (app.py) – Interactive, user-friendly interface for exploring API data visually.

Outputs (CSV + Charts) – Evidence of successful execution.

Documentation (README.md) – Step-by-step guide for users and evaluators.

 Completion Criteria

Integration with a public API has been demonstrated.

Weather data is successfully processed and visualized.

Both script and dashboard run without errors.

Outputs are generated and stored correctly.

Documentation explains the setup and usage clearly.

Future Enhancements

Add advanced plots using Seaborn (correlation, heatmaps).

Provide export options (Excel, PDF reports).

Allow multiple cities to be compared simultaneously.

Deploy dashboard online using Streamlit Cloud or Heroku

OUTPUT:

<img width="1650" height="600" alt="Image" src="https://github.com/user-attachments/assets/9c13cb41-0e13-44fd-95c4-ab615c16eed8" />

<img width="1200" height="600" alt="Image" src="https://github.com/user-attachments/assets/0bcac696-655a-4f0c-b38c-106ed7ac5330" />

<img width="1200" height="600" alt="Image" src="https://github.com/user-attachments/assets/1c32d074-640b-4aeb-847d-25575c2caea3" />


















