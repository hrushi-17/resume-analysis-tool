# 🎓📄 Resume Analysis Tool

## 📘 About the Project
The Resume Analysis Tool is a sophisticated web application developed to analyze technical resumes and provide valuable insights. This tool is designed to assist job seekers in refining their resumes and increasing their chances of landing their desired roles. It leverages machine learning and natural language processing techniques to evaluate the content of resumes, offering users personalized feedback.

## 📈 Scope
This project aims to:
- Provide job seekers with a detailed analysis of their resumes.
- Recommend improvements based on industry standards and trends.
- Predict suitable job roles for users based on their resume content.
- Offer administrators an interface to manage user data and view analytical reports.

## 🛠️ Tech Stack

### 🌐 Frontend
- **HTML**: For structuring the web pages.
- **CSS (Bootstrap)**: For styling the web pages and ensuring a responsive design.
- **JavaScript (Plotly for charts)**: For creating interactive charts and enhancing user interaction.

### 🖥️ Backend
- **Python**: The core programming language used for developing the application.
- **Flask**: A lightweight WSGI web application framework used for building the backend services.

### 🗄️ Database
- **SQLite**: Used for local development and testing.
- **PostgreSQL**: Used for production to handle larger datasets and provide more robust data management.

### 📦 Modules
- **Flask**: For web framework.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive data visualizations.
- **Bootstrap**: For responsive design and UI components.

## ⭐ Features

### 🔹 User Side
- 📤 **Upload PDF resumes** for analysis.
- 📊 **Receive detailed analysis reports** including:
  - Skill recommendations.
  - Resume scores.
  - Tips for improvement.
  - Predicted job roles.
- 🎥 **Access YouTube links** for tips on creating impactful resumes.

### 🔸 Admin Side
- 🗃️ **View all user submissions** and their analysis results.
- 📈 **Download user data** in Excel format.
- 📊 **Visualize user data** with interactive pie charts for job role and location distributions.

## 📋 Requirements
- Python 3.x
- Flask
- Plotly
- Pandas
- SQLAlchemy (for PostgreSQL)
- Flask-WTF (for form handling)

## 🛠️ Setup and Installation Guide

<details>
<summary>🔧 Install Python</summary>

1. Download and install Python from [python.org](https://www.python.org/).
2. Ensure Python is added to your system PATH during installation.
</details>

<details>
<summary>🛠️ Set Up Virtual Environment (Optional but Recommended)</summary>

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to set up your project.
3. Run the following commands:
    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```
</details>

<details>
<summary>📂 Create the Project Directory</summary>

1. Create a new directory for your project:
    ```sh
    mkdir resume-analysis-tool
    cd resume-analysis-tool
    ```
</details>

<details>
<summary>📦 Install Required Packages</summary>

1. In the project directory, install the necessary Python packages:
    ```sh
    pip install Flask PyPDF2 NLTK spaCy Pandas Werkzeug Jinja2
    ```
</details>

<details>
<summary>📁 Directory Structure</summary>

1. Create the following directory structure within the `resume-analysis-tool` directory:
    ```
    resume-analysis-tool/
    ├── templates/
    │   ├── index.html
    │   ├── result.html
    │   ├── admin_result.html
    ├── static/
    │   └── images/
    ├── uploads/
    │   └── # Placeholder for uploaded resumes
    ├── your data/
    │   └── user_data.csv
    ├── venv/
    ├── app.py
    ├── requirements.txt
    ├── temp_resume.pdf
    ```
2. Ensure that the `templates` directory contains your HTML templates (`index.html`, `result.html`, `admin_result.html`).
3. Place any static files like images in the `static/images` directory.
4. Store uploaded resumes in the `uploads` directory.
5. Store user data in the `your data` directory.
</details>

<details>
<summary>🚀 Run the Application</summary>

1. In the terminal, navigate to the project directory.
2. Ensure the virtual environment is activated.
3. Run the Flask application:
    ```sh
    flask run
    ```
4. Open a web browser and navigate to `http://127.0.0.1:5000`.
</details>

<details>
<summary>🖥️ Using VS Code</summary>

1. Open VS Code and the Project Folder
    - Open VS Code.
    - Open the `resume-analysis-tool` directory in VS Code.

2. Create and Activate Virtual Environment
    - Open the terminal in VS Code.
    - Create and activate the virtual environment in the terminal:
      ```sh
      python -m venv venv
      source venv/bin/activate # On Windows, use `venv\Scripts\activate`
      ```

3. Install Required Packages
    - Ensure the virtual environment is active.
    - Install the required packages using pip:
      ```sh
      pip install Flask PyPDF2 nltk spacy pandas Werkzeug
      ```

4. Run the Flask Application
    - In the VS Code terminal, run the Flask application:
      ```sh
      flask run
      ```
    - Open a web browser and navigate to `http://127.0.0.1:5000`.
</details>

## 🚀 Usage
To use the application:
- Open the web application in your browser.
- **User Side**:
  - Upload a PDF resume.
  - View the detailed analysis and recommendations.
- **Admin Side**:
  - Log in to access user data.
  - Download reports and view data visualizations.

## 🛤️ Roadmap
The future developments for the Resume Analysis Tool include:
- Implementing user authentication and authorization for enhanced security.
- Integrating advanced AI-based analysis features for more accurate insights.
- Enhancing UI/UX for a more intuitive user experience.
- Scaling the application to handle higher traffic and concurrent users.

## 📸 Preview

### User Side
![User Interface](path/to/user_interface_screenshot.png)

### Admin Side
![Admin Interface](path/to/admin_interface_screenshot.png)

## 📥 Download and Installation
You can download the project by cloning the repository or downloading the ZIP file.

### Clone the Repository
```sh
git clone https://github.com/hrushi-17/resume-analysis-tool.git
cd resume-analysis-tool
