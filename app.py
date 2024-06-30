from flask import Flask, render_template, request, redirect, url_for, session, send_file
from PyPDF2 import PdfReader
import nltk
import spacy
import os
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define a list to store user data for each session
session_user_data = []

# Define a list to store unique user data
unique_user_data = []

# Download NLTK data
nltk.download('punkt')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Define a list of technical skills
technical_skills = ["Java", "SQL", "HTML", "Python", "JavaScript", "CSS","C", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "TypeScript", "Git", "Data Analysis", "Machine Learning"]

# Define a list of headings to check for
headings_to_check = ["Basic Details", "Education", "Project", "Internship", "Skill", "Certificate", "Achievement", "Language", "Hobbies"]

# Define additional factors for calculating the resume score
resume_factors = {
    "Keywords Match": 20,
    "Education Match": 15,
    "Internship Relevance": 10,
    "Skills Match": 15,
    "Formatting and Readability": 10,
    "Job Title Match": 10,
    "Length of Employment": 10,
    "Section Headings": 5,
    "Chronological Order": 5,
    "Quantifiable Achievements": 5
}

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to ensure the 'uploads' directory exists
def ensure_upload_dir_exists():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Function to extract text from uploaded resume in PDF format
def extract_text_from_pdf(resume_path):
    with open(resume_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract technical skills from text using predefined list
def extract_technical_skills(text):
    doc = nlp(text)
    skills = [skill for skill in technical_skills if skill.lower() in text.lower()]
    return skills

# Function to check the presence of specific headings in the text
def check_headings_presence(text):
    present_headings = [heading for heading in headings_to_check if heading.lower() in text.lower()]
    return present_headings

# Function to recommend skills based on existing skills
def recommend_skills(existing_skills):
    # Create a list to store recommended skills
    recommended_skills = []
    
    # Define a dictionary mapping main skills to related skills
    related_skills = {
        "Java": ["Spring", "Hibernate", "JPA", "Maven"],
        "SQL": ["MySQL", "PostgreSQL", "SQLite"],
        "HTML": ["CSS", "JavaScript", "Bootstrap"],
        "Python": ["Django", "Flask", "NumPy", "Pandas"],
        "JavaScript": ["Node.js", "React", "Angular", "Vue.js"],
        "CSS": ["Sass", "Less", "Tailwind CSS"],
        "C": ["Embedded Systems", "Operating Systems", "Game Development"],
        "C++": ["Object-Oriented Programming", "Game Development", "Systems Programming"],
        "C#": ["Unity Game Development", ".NET Framework", "Windows Desktop Applications"],
        "Ruby": ["Ruby on Rails", "Web Development", "Scripting"],
        "PHP": ["Web Development", "WordPress Development", "Laravel"],
        "Swift": ["iOS App Development", "macOS App Development", "SwiftUI"],
        "Kotlin": ["Android App Development", "Multiplatform Development", "Jetpack Compose"],
        "TypeScript": ["Frontend Development", "Node.js Development", "React Development"],
        "Git": ["Version Control", "Collaborative Development", "GitHub Workflow"],
        "Data Analysis": ["Data Visualization", "Data Mining", "Data Warehousing"],
        "Machine Learning": ["Deep Learning", "Natural Language Processing", "Computer Vision"],
    }
    
    # Iterate through existing skills
    for skill in existing_skills:
        # Check if the skill has related skills
        if skill in related_skills:
            # Add related skills to the recommended skills list
            recommended_skills.extend(related_skills[skill])
    
    # Remove duplicates from recommended skills
    recommended_skills = list(set(recommended_skills))
    
    return recommended_skills

# Function to provide tips for each heading
def get_heading_tips(present_headings):
    tips = {
        "Basic Details": "Include your personal information such as name, contact details, and LinkedIn profile.",
        "Education": "Highlight your educational background, including the name of the college, degree, and graduation year.",
        "Project": "Describe your projects in detail, mentioning technologies used, your role, and outcomes.",
        "Internship": "Detail your internship experiences, emphasizing skills gained and contributions made.",
        "Skill": "List technical and soft skills relevant to the job you're applying for.",
        "Certificate": "Showcase any certifications you've earned to demonstrate your expertise.",
        "Achievement": "Highlight significant achievements or awards you've received.",
        "Language": "Specify languages you are proficient in, both programming languages and spoken languages.",
        "Hobbies": "Include hobbies and interests to add a personal touch to your resume."
    }
    tips_sentences = []
    for heading in present_headings:
        tips_sentence = f"Congratulations! You included {heading.lower()}. {tips[heading]}"
        tips_sentences.append(tips_sentence)
    return tips_sentences

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a dictionary mapping technical skills to recommended job roles
recommended_job_roles = {
    "Java": ["Software Developer", "Web Developer"],
    "SQL": ["Data Analyst", "Database Administrator"],
    "HTML": ["Web Designer", "Frontend Developer"],
    "Python": ["Data Scientist", "Machine Learning Engineer"],
    "Spring": ["Java Developer", "Backend Developer"],
    "Hibernate": ["Java Developer", "Backend Developer"],
    "JPA": ["Java Developer", "Backend Developer"],
    "Maven": ["Java Developer", "DevOps Engineer"],
    "MySQL": ["Database Administrator", "Database Developer"],
    "PostgreSQL": ["Data Analyst", "Database Administrator"],
    "SQLite": ["Mobile App Developer", "Database Administrator"],
    "CSS": ["Frontend Developer", "UI/UX Designer"],
     "C": ["Embedded Systems Developer", "Game Developer", "Systems Programmer"],
    "C++": ["Software Engineer", "Game Developer", "Systems Programmer"],
    "C#": ["Unity Developer", "Software Engineer", "Windows Developer"],
    "Ruby": ["Ruby on Rails Developer", "Web Developer", "Scripting Engineer"],
    "PHP": ["PHP Developer", "WordPress Developer", "Web Developer"],
    "Swift": ["iOS Developer", "macOS Developer", "Swift Developer"],
    "Kotlin": ["Android Developer", "Multiplatform Developer", "Kotlin Developer"],
    "TypeScript": ["Frontend Developer", "Full Stack Developer", "Node.js Developer"],
    "Git": ["Version Control Engineer", "DevOps Engineer", "Software Engineer"],
    "JavaScript": ["Web Developer", "Full Stack Developer"],
    "Node.js": ["Backend Developer", "Full Stack Developer"],
    "React": ["Frontend Developer", "UI Developer"],
    "Angular": ["Frontend Developer", "Web Developer"],
    "Vue.js": ["Frontend Developer", "Web Developer"],
    "Sass": ["UI/UX Designer", "Frontend Developer"],
    "Less": ["Frontend Developer", "UI Developer"],
    "Tailwind CSS": ["Frontend Developer", "UI Developer"],
    "Data Analysis": ["Data Analyst", "Business Intelligence Analyst"],
    "Data Visualization": ["Data Analyst", "Data Scientist"],
    "Data Mining": ["Data Scientist", "Machine Learning Engineer"],
    "Data Warehousing": ["Data Engineer", "Database Administrator"],
    "Deep Learning": ["Machine Learning Engineer", "AI Engineer"],
    "Natural Language Processing": ["Data Scientist", "Machine Learning Engineer"],
    "Computer Vision": ["Computer Vision Engineer", "AI Engineer"]
}

# Certificate recommendations based on technical skills
certificate_recommendations = {
    "Java": "https://www.udemy.com/topic/java/",
    "SQL": "https://www.coursera.org/courses?query=SQL",
    "HTML": "https://www.internshala.com/courses/html-css-javascript-training",
    "Python": "https://www.udacity.com/courses/python",
    "JavaScript": "https://www.codecademy.com/catalog/language/javascript",
    "CSS": "https://www.udemy.com/topic/css/",
    "C": "https://www.udemy.com/topic/c-programming/",
    "C++": "https://www.coursera.org/courses?query=c%2B%2B%20programming",
    "C#": "https://www.edx.org/learn/c-sharp",
    "Ruby": "https://www.udemy.com/topic/ruby/",
    "PHP": "https://www.coursera.org/courses?query=php%20programming",
    "Swift": "https://www.edx.org/learn/swift-programming",
    "Kotlin": "https://www.pluralsight.com/courses/kotlin-fundamentals",
    "TypeScript": "https://www.udemy.com/topic/typescript/",
    "Git": "https://www.udemy.com/topic/git/",
    "Data Analysis": "https://www.coursera.org/courses?query=data%20analysis",
    "Machine Learning": "https://www.udemy.com/topic/machine-learning/",
    "Spring": "https://www.udemy.com/topic/spring-framework/",
    "Hibernate": "https://www.udemy.com/topic/hibernate/",
    "JPA": "https://www.udemy.com/topic/java-persistence-api/",
    "MySQL": "https://www.udemy.com/topic/mysql/",
    "PostgreSQL": "https://www.udemy.com/topic/postgresql/",
    "SQLite": "https://www.udemy.com/topic/sqlite/",
    "Node.js": "https://www.udemy.com/topic/node-js/",
    "React": "https://www.udemy.com/topic/react-js/",
    "Angular": "https://www.udemy.com/topic/angular-js/",
    "Vue.js": "https://www.udemy.com/topic/vue-js/",
    "Sass": "https://www.udemy.com/topic/sass/",
    "Less": "https://www.udemy.com/topic/less/",
    "Tailwind CSS": "https://www.udemy.com/topic/tailwind-css/",
    "Data Visualization": "https://www.coursera.org/courses?query=data%20visualization",
    "Data Mining": "https://www.coursera.org/courses?query=data%20mining",
    "Data Warehousing": "https://www.coursera.org/courses?query=data%20warehousing",
    "Deep Learning": "https://www.udemy.com/topic/deep-learning/",
    "Natural Language Processing": "https://www.udemy.com/topic/natural-language-processing/",
    "Computer Vision": "https://www.udemy.com/topic/computer-vision/"
}

# Function to recommend job roles based on technical skills
def recommend_job_roles(technical_skills):
    # Create a dictionary to store the relevance score of each job role
    role_scores = {}
    
    # Iterate through each technical skill
    for skill in technical_skills:
        # Check if the skill has related job roles
        if skill in recommended_job_roles:
            # Iterate through each related job role
            for role in recommended_job_roles[skill]:
                # Increment the relevance score for the job role
                role_scores[role] = role_scores.get(role, 0) + 1
    
    # Sort the job roles by relevance score in descending order
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top 3 recommended job roles
    top_3_roles = [role for role, score in sorted_roles[:3]]
    
    return top_3_roles

# Function to get certificate recommendation for each skill
def get_certificate_recommendations(technical_skills):
    recommendations = {}
    for skill in technical_skills:
        if skill in certificate_recommendations:
            recommendations[skill] = certificate_recommendations[skill]
    return recommendations

def calculate_total_unique_users():
    unique_users = set()
    for user_result in session_user_data:
        user_info = (
            user_result['user_data']['name'],
            user_result['user_data']['email'],
            user_result['user_data']['phone'],
            user_result['user_data']['address'],
            user_result['user_data']['city'],
            user_result['user_data']['state'],
            user_result['user_data']['country'],
            user_result['user_data']['pincode']
        )
        unique_users.add(user_info)
        
    return len(unique_users)



# Define the Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_upload_dir_exists()

    # Calculate the total number of unique users
    total_unique_users = calculate_total_unique_users()

    if request.method == 'POST':
        # Get user information from the form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']  # Add address field
        city = request.form['city']  # Add city field
        state = request.form['state']  # Add state field
        country = request.form['country']  # Add country field
        # Get pincode from the form
        pincode = request.form['pincode']


        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store user data in session
        session['user_data'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,  # Store address
            'city': city,  # Store city
            'state': state,  # Store state
            'country': country,  # Store country
            'pincode': pincode,  # Add the pincode field
            'timestamp': timestamp  # Store timestamp
        }

        # Handle the uploaded resume file
        uploaded_resume = request.files['resume']

        # Check if the file is allowed and has a name
        if uploaded_resume.filename == '' or not allowed_file(uploaded_resume.filename):
            return "Invalid file"

        # Save the uploaded file to the upload folder with a secure filename
        filename = secure_filename(uploaded_resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Handle duplicate filenames
        count = 1
        while os.path.exists(resume_path):
            base, ext = os.path.splitext(resume_path)
            resume_path = f"{base}_{count}{ext}"
            count += 1

        uploaded_resume.save(resume_path)

        # Extract text from the uploaded resume
        resume_text = extract_text_from_pdf(resume_path)

        # Extract technical skills from resume text
        technical_resume_skills = extract_technical_skills(resume_text)

        # Check the presence of specific headings in the resume
        present_headings = check_headings_presence(resume_text)

        # Recommend skills based on extracted technical skills
        recommended_skills = recommend_skills(technical_resume_skills)

        # Recommend job roles based on extracted technical skills
        recommended_job_roles = recommend_job_roles(technical_resume_skills)
        
        # Calculate a simple score based on the presence of headings and additional factors
        resume_score = 0

        # Keywords Match
        if "Keywords Match" in present_headings:
            resume_score += resume_factors["Keywords Match"]

        # Education Match
        if "Education" in present_headings:
            resume_score += resume_factors["Education Match"]

        # Internship Relevance
        if "Internship" in present_headings:
            resume_score += resume_factors["Internship Relevance"]

        # Skills Match
        if "Skill" in present_headings:
            resume_score += resume_factors["Skills Match"]

        # Formatting and Readability
        resume_score += resume_factors["Formatting and Readability"]

        # Job Title Match
        if "Job Title Match" in present_headings:
            resume_score += resume_factors["Job Title Match"]

        # Length of Employment
        if "Internship" in present_headings:  # Assuming the internship section represents work experience
            resume_score += resume_factors["Length of Employment"]

        # Section Headings
        if "Internship" in present_headings or "Education" in present_headings:
            resume_score += resume_factors["Section Headings"]

        # Chronological Order
        if "Internship" in present_headings or "Education" in present_headings:
            resume_score += resume_factors["Chronological Order"]

        # Quantifiable Achievements
        if "Achievement" in present_headings:
            resume_score += resume_factors["Quantifiable Achievements"]

        # Store the calculated values in the session using appropriate keys
        session['technical_resume_skills'] = technical_resume_skills
        session['recommended_skills'] = recommended_skills
        session['resume_score'] = resume_score
        session['recommended_job_roles'] = recommended_job_roles

        # Display user information
        print("\nUser Information:")
        print("Name:", name)
        print("Email:", email)
        print("Phone Number:", phone)

        # Display results
        print("\nUploaded Technical Resume Skills:", technical_resume_skills)
        print("Headings Present in Resume:", present_headings)
        print("Recommended Skills:", recommended_skills)
        print("Resume Score:", resume_score)

        # Display tips based on missing headings
        missing_headings = [heading for heading in headings_to_check if heading not in present_headings and heading != "Basic Details"]
        if missing_headings:
            print("\nTips for Improvement:")
            for heading in missing_headings:
                print(f"- You didn't have any {heading.lower()}, please add {heading.lower()} to improve your resume score.")
        else:
            print("\nGreat job! Your resume includes all the recommended sections except for Basic Details.")

        # Display tips for each present heading
        heading_tips_sentences = get_heading_tips(present_headings)
        if heading_tips_sentences:
            print("\nAdditional Tips for Present Headings:")
            for tip_sentence in heading_tips_sentences:
                print(f"- {tip_sentence}")

        # Display YouTube links for resume creation tips
        youtube_links = {
            "Resume Writing Tips": "https://youtu.be/Tt08KmFfIYQ?si=OQjwJCYD5QN_M8FI",
            "Crafting an Ideal Resume": "https://youtu.be/IW472-d_8bs?si=MzUb35yESnHGdOzZ",
            "Resume Formatting Guidelines": "https://youtu.be/yTXZJqoppfo?si=iTkvWb1GZ8NrLDp8",
            "Showcasing Achievements on a Resume": "https://youtu.be/LuBUisj7SXA?si=seBrxTMlYjlrUEjz"
        }

        print("\nYouTube Links for Resume Creation Tips:")

        # Iterate through each YouTube link and display the title page
        for topic, link in youtube_links.items():
            print(f"- {topic}: {link}")

            # Fetch and display the title page
            title_page_url = f"{link.split('=')[0]}=embed/{link.split('=')[1]}"
            # Assuming you have a function display_iframe to render iframes in your HTML
            # display_iframe(title_page_url)

        # Get certificate recommendations based on technical skills
        certificate_recommendations = get_certificate_recommendations(technical_resume_skills)

        # Recommend job roles based on extracted technical skills
        recommended_job_roles = recommend_job_roles(technical_resume_skills)

        # Render the template with all necessary data
        return render_template('result.html', result={
            'name': name,
            'email': email,
            'phone': phone,
            'technical_resume_skills': technical_resume_skills,
            'present_headings': present_headings,
            'recommended_skills': recommended_skills,
            'resume_score': resume_score,
            'tips_for_improvement': missing_headings,
            'heading_tips_sentences': heading_tips_sentences,
            'recommended_job_roles': recommended_job_roles,
            'certification_recommendations': certificate_recommendations,  # Change here
            'youtube_links': youtube_links
        })

        # Code to handle form submission and analysis (omitted for brevity)
        return redirect(url_for('admin_result'))

    # Render the index template for GET requests and pass the total_unique_users count to the template
    return render_template('index.html', total_unique_users=total_unique_users)

# Your existing imports remain the same

# Route for admin result page
@app.route('/admin/result')
def admin_result():
    # Check if user data exists in session
    if 'user_data' in session:
        # Retrieve user data from session
        user_data = session['user_data']
        
        # Retrieve the user's uploaded technical resume skills, recommended skills, and resume score from the session
        technical_resume_skills = session.get('technical_resume_skills')
        recommended_skills = session.get('recommended_skills')
        resume_score = session.get('resume_score')
        recommended_job_roles = session.get('recommended_job_roles')
        
        # Create a dictionary containing the user's data
        user_result = {
            'user_data': user_data,
            'technical_resume_skills': technical_resume_skills,
            'recommended_skills': recommended_skills,
            'resume_score': resume_score,
            'recommended_job_roles': recommended_job_roles, 
        }
        
        # Check if the user data already exists in session_user_data list
        if user_result not in session_user_data:
            # Append user result to session_user_data list
            session_user_data.append(user_result)
            
        # Calculate the total number of unique users
        total_unique_users = calculate_total_unique_users()

        # Extract the predicted job roles from the recommended job roles
        predicted_job_roles_data = [role for user in session_user_data for role in user['recommended_job_roles']]

        # Render admin_result.html with user data list and predicted job roles data
        return render_template('admin_result.html', users=session_user_data, total_unique_users=total_unique_users, predicted_job_roles_data=predicted_job_roles_data)

    else:
        # If no user data in session, redirect to index.html
        return redirect(url_for('index'))

# Route for generating pie chart data for city
@app.route('/admin/result/pie-chart/city')
def generate_city_pie_chart_data():
    # Count occurrences of each city
    city_count = Counter([user['city'] for user in unique_user_data if user['city']])
    
    # Convert the count to a dictionary
    city_data = dict(city_count)
    
    # Convert the dictionary to JSON and return
    return jsonify(city_data)

# Route for generating pie chart data for state
@app.route('/admin/result/pie-chart/state')
def generate_state_pie_chart_data():
    # Count occurrences of each state
    state_count = Counter([user['state'] for user in unique_user_data if user['state']])
    
    # Convert the count to a dictionary
    state_data = dict(state_count)
    
    # Convert the dictionary to JSON and return
    return jsonify(state_data)

# Route for generating pie chart data for country
@app.route('/admin/result/pie-chart/country')
def generate_country_pie_chart_data():
    # Count occurrences of each country
    country_count = Counter([user['country'] for user in unique_user_data if user['country']])
    
    # Convert the count to a dictionary
    country_data = dict(country_count)
    
    # Convert the dictionary to JSON and return
    return jsonify(country_data)

# New route and function for admin result download
@app.route('/admin/result/download', methods=['GET', 'POST'])
def admin_result_download():
    global unique_user_data
    
    # Retrieve user data from session
    user_data = session.get('user_data')
    
    if user_data:
        # Check if the user data is already present in the unique_user_data list
        user_data_found = any(user_data['name'] == user['Name'] for user in unique_user_data)
        
        if not user_data_found:
            # Retrieve the technical resume skills, recommended skills, and resume score from the session
            technical_resume_skills = session.get('technical_resume_skills')
            recommended_skills = session.get('recommended_skills')
            resume_score = session.get('resume_score')
            recommended_job_roles = session.get('recommended_job_roles')
            
            # Create a dictionary containing the user's data
            user_result = {
                'Name': user_data['name'],
                'Email': user_data['email'],
                'Phone Number': user_data['phone'],
                'Address': user_data['address'],
                'City': user_data['city'],
                'State': user_data['state'],
                'Country': user_data['country'],
                'Pincode': user_data['pincode'],
                'Timestamp': user_data['timestamp'],
                'Uploaded Technical Resume Skills': ', '.join(technical_resume_skills) if technical_resume_skills else '',
                'Recommended Skills': ', '.join(recommended_skills) if recommended_skills else '',
                'Resume Score': resume_score,
                'recommended_job_roles':', '.join(recommended_job_roles) if recommended_job_roles else '', 
            }
            
            # Append the user result to the unique_user_data list
            unique_user_data.append(user_result)
        
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(unique_user_data)
        
        # Specify the path for the Excel file inside the "your data" folder
        excel_file_dir = 'your data'
        excel_file_path = os.path.join(excel_file_dir, 'user_data.xlsx')
        
        # Create the directory if it doesn't exist
        if not os.path.exists(excel_file_dir):
            os.makedirs(excel_file_dir)
        
        # Generate the Excel file
        df.to_excel(excel_file_path, index=False)
        
        # Return the Excel file as a response for download
        return send_file(excel_file_path, as_attachment=True)
    else:
        return "No user data found"


if __name__ == '__main__':
    app.run(debug=True)
