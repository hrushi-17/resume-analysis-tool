# Resume Analysis Tool

## About the Project
The Resume Analysis Tool is a web application designed to analyze technical resumes and provide insights to users and administrators.

## Scope
This project aims to assist job seekers in optimizing their resumes by providing actionable insights based on uploaded content. It also includes administrative functionalities to manage user data and view analytics.

## Tech Stack

### Frontend
- HTML
- CSS (Bootstrap)
- JavaScript (Plotly for charts)

### Backend
- Python
- Flask framework

### Database
- SQLite (for local development)
- PostgreSQL (for production)

### Modules
- Flask (web framework)
- Pandas (data manipulation)
- Plotly (data visualization)
- Bootstrap (CSS framework)

## Features

### User Side
- Upload PDF resumes for analysis
- Receive detailed analysis reports including skill recommendations and resume scores
- View tips for resume improvement and job role recommendations
- Access YouTube links for resume creation tips

### Admin Side
- View all user submissions and their analysis results
- Download user data in Excel format
- Visualize user data with interactive pie charts for job role and location distributions

## Requirements
- Python 3.x
- Flask
- Plotly
- Pandas
- SQLAlchemy (for PostgreSQL)
- Flask-WTF (for forms handling)

## Setup and Installation Guide

### Using VS Code Terminal
1. Clone the repository:
git clone https://github.com/hrushi-17/resume-analysis-tool.git

2. Navigate to the project directory:
cd resume-analysis-tool

3. Install dependencies:
pip install -r requirements.txt

4. Set up environment variables (if necessary).
5. Run the application:
python app.py


### Downloading Zip File from GitHub
1. Download the project zip file from [GitHub](https://github.com/hrushi-17/resume-analysis-tool).
2. Extract the zip file to your preferred directory.
3. Open a terminal window in VS Code and navigate to the extracted project folder.
4. Follow steps 3-5 from the "Using VS Code Terminal" section above.

## Usage
- Access the application through your web browser.
- Upload a PDF resume for analysis on the user side.
- Admins can log in to view user submissions and analytics.
- Download Excel reports and view distribution charts.

## Roadmap
- Implement user authentication and authorization for enhanced security.
- Integrate more advanced AI-based analysis features.
- Enhance UI/UX for a more intuitive user experience.
- Scale the application for higher traffic and multiple users concurrently.

## Preview

### User Side
![User Interface](/path/to/user_interface_screenshot.png)

### Admin Side
![Admin Interface](/path/to/admin_interface_screenshot.png)
