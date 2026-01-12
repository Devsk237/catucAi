import os
import json
import requests
import glob
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

class LegendBot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.school_data_cache = {}
        self.load_school_data_files()
    
    def load_school_data_files(self):
        """Load all JSON files from the data folder"""
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            return
        
        json_files = glob.glob(os.path.join(data_folder, '*.json'))
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    filename = os.path.basename(file_path).replace('.json', '')
                    self.school_data_cache[filename] = json.load(f)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    def get_school_data(self):
        """Get combined school data from all files"""
        combined_data = {}
        for filename, data in self.school_data_cache.items():
            if isinstance(data, dict):
                combined_data.update(data)
            else:
                combined_data[filename] = data
        return combined_data
        
    def call_openrouter_api(self, prompt, model="google/gemini-2.0-flash-exp:free"):
        """Call OpenRouter API with the given prompt"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': 'http://localhost:3000',  # Update with your actual URL
            'X-Title': 'LegendBot School Assistant'
        }
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
 #               error_msg = f"OpenRouter API Error: {response.status_code}"
                error_msg = f"Please Check What your wrote or Internet Connection"
                try:
                    error_details = response.json()
                    if 'error' in error_details:
                        error_msg += f" - {error_details['error'].get('message', 'Unknown error')}"
                except:
                    error_msg += f" - {response.text[:100]}"
                return error_msg
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except Exception as e:
#            return f"Error connecting to AI service: {str(e)}"
            return f"Error connecting to AI service: Check your Connection"
    
    def check_school_data(self, question, school_data):
        """Check if school_data contains relevant information for the question"""
        if not school_data:
            return None
            
        # Check for specific keywords that map to data sections
        question_lower = question.lower()
        
        # Course-related questions
        if any(word in question_lower for word in ['course', 'courses', 'program', 'programs', 'major', 'study']):
            if 'courses' in school_data:
                return self.format_course_response(school_data['courses'])
        
        # Registration-related questions
        if any(word in question_lower for word in ['registration', 'register', 'enroll', 'deadline', 'apply']):
            if 'registrations' in school_data:
                return self.format_registration_response(school_data['registrations'])
        
        # Exam-related questions
        if any(word in question_lower for word in ['exam', 'exams', 'test', 'tests', 'schedule']):
            if 'exams' in school_data:
                return self.format_exam_response(school_data['exams'])
        
        # Contact-related questions
        if any(word in question_lower for word in ['contact', 'call', 'email', 'phone', 'office']):
            if 'contacts' in school_data:
                return self.format_contact_response(school_data['contacts'])
        
        # FAQ-related questions
        if any(word in question_lower for word in ['faq', 'help', 'question', 'how to', 'what', 'when', 'where']):
            if 'faqs' in school_data:
                return self.format_faq_response(school_data['faqs'])
        
        return None
    
    def format_course_response(self, courses_data):
        """Format response for course-related questions"""
        response_parts = []
        
        if isinstance(courses_data, dict):
            response_parts.append("Here are the courses we offer:")
            for course_key, course_info in courses_data.items():
                if isinstance(course_info, dict):
                    name = course_info.get('name', course_key.title())
                    desc = course_info.get('description', '')
                    duration = course_info.get('duration', '')
                    prereq = course_info.get('prerequisites', '')
                    
                    course_text = f"{name}"
                    if desc:
                        course_text += f" - {desc}"
                    if duration:
                        course_text += f"\nDuration: {duration}"
                    if prereq:
                        course_text += f"\nPrerequisites: {prereq}"
                    
                    response_parts.append(course_text)
        
        if response_parts:
            response = "\n\n".join(response_parts)
            response += "\n\n(source: school database)"
            return response
        
        return None
    
    def format_registration_response(self, registration_data):
        """Format response for registration-related questions"""
        response_parts = []
        
        if isinstance(registration_data, dict):
            response_parts.append("Registration Information:")
            for reg_key, reg_info in registration_data.items():
                if isinstance(reg_info, dict):
                    deadline = reg_info.get('deadline', '')
                    start_date = reg_info.get('start_date', '')
                    form_link = reg_info.get('form_link', '')
                    
                    reg_text = f"{reg_key.replace('_', ' ').title()}"
                    if deadline:
                        reg_text += f"\nDeadline: {deadline}"
                    if start_date:
                        reg_text += f"\nStart Date: {start_date}"
                    if form_link:
                        reg_text += f"\nRegistration Form: {form_link}"
                    
                    response_parts.append(reg_text)
        
        if response_parts:
            response = "\n\n".join(response_parts)
            response += "\n\n(source: school database)"
            return response
        
        return None
    
    def format_exam_response(self, exam_data):
        """Format response for exam-related questions"""
        response_parts = []
        
        if isinstance(exam_data, dict):
            response_parts.append("Exam Information:")
            for exam_key, exam_info in exam_data.items():
                if isinstance(exam_info, dict):
                    date_range = exam_info.get('date_range', '')
                    schedule = exam_info.get('schedule', '')
                    location = exam_info.get('location', '')
                    
                    exam_text = f"{exam_key.replace('_', ' ').title()}"
                    if date_range:
                        exam_text += f"\nDates: {date_range}"
                    if schedule:
                        exam_text += f"\nSchedule: {schedule}"
                    if location:
                        exam_text += f"\nLocation: {location}"
                    
                    response_parts.append(exam_text)
        
        if response_parts:
            response = "\n\n".join(response_parts)
            response += "\n\n(source: school database)"
            return response
        
        return None
    
    def format_contact_response(self, contact_data):
        """Format response for contact-related questions"""
        response_parts = []
        
        if isinstance(contact_data, dict):
            response_parts.append("Contact Information:")
            for dept_key, contact_info in contact_data.items():
                if isinstance(contact_info, dict):
                    phone = contact_info.get('phone', '')
                    email = contact_info.get('email', '')
                    hours = contact_info.get('office_hours', '')
                    location = contact_info.get('location', '')
                    
                    contact_text = f"{dept_key.replace('_', ' ').title()}"
                    if phone:
                        contact_text += f"\nPhone: {phone}"
                    if email:
                        contact_text += f"\nEmail: {email}"
                    if hours:
                        contact_text += f"\nHours: {hours}"
                    if location:
                        contact_text += f"\nLocation: {location}"
                    
                    response_parts.append(contact_text)
        
        if response_parts:
            response = "\n\n".join(response_parts)
            response += "\n\n(source: school database)"
            return response
        
        return None
    
    def format_faq_response(self, faq_data):
        """Format response for FAQ-related questions"""
        response_parts = []
        
        if isinstance(faq_data, list):
            response_parts.append("Frequently Asked Questions:")
            for i, faq in enumerate(faq_data, 1):
                response_parts.append(f"{i}. {faq}")
        
        if response_parts:
            response = "\n\n".join(response_parts)
            response += "\n\nFor specific answers to these questions, please contact the appropriate department.\n\n(source: school database)"
            return response
        
        return None
    
    def web_search_fallback(self, question, model="google/gemini-2.0-flash-exp:free"):
        """Use OpenRouter API for general knowledge fallback"""
        prompt = f"""You are LegendBot, a helpful and accurate school inquiry assistant. 

A student asked: "{question}"

I could not find this information in the school's database. Please provide a helpful response based on general knowledge about schools, education, or common school procedures.

Guidelines:
- Answer clearly and politely in simple language
- Include examples or next steps when helpful
- Be clear when you are making reasonable assumptions
- Never invent exact dates, contact details, or links
- If specific information is needed, suggest how to retrieve it from the school admin
- Label your response with "(source: general knowledge)"

Please provide a helpful response."""
        
        return self.call_openrouter_api(prompt, model)
    
    def generate_response(self, question, school_data=None, model="google/gemini-2.0-flash-exp:free"):
        """Generate response for the given question"""
        # First check school_data
        school_response = self.check_school_data(question, school_data)
        if school_response:
            return school_response
        
        # Fall back to AI model
        return self.web_search_fallback(question, model)

# Initialize the bot with your OpenRouter API key
OPENROUTER_API_KEY = "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"  # Replace with your actual OpenRouter API key
bot = LegendBot(OPENROUTER_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    model = data.get('model', 'google/gemini-2.0-flash-exp:free')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Automatically load school data from data folder
    school_data = bot.get_school_data()
    response = bot.generate_response(question, school_data, model)
    return jsonify({'response': response})

@app.route('/models', methods=['GET'])
def get_available_models():
    """Get available models from OpenRouter"""
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                'Authorization': f'Bearer {bot.api_key}',
                'HTTP-Referer': 'http://localhost:3000'
            }
        )
        if response.status_code == 200:
            models = response.json().get('data', [])
            # Filter to show free/affordable models first
            filtered_models = [
                {
                    'id': model['id'],
                    'name': model.get('name', model['id']),
                    'description': model.get('description', ''),
                    'pricing': model.get('pricing', {})
                }
                for model in models
                if 'free' in model['id'].lower() or 'gpt' in model['id'].lower() or 'gemini' in model['id'].lower()
            ]
            return jsonify({'models': filtered_models})
        else:
            return jsonify({'error': 'Failed to fetch models'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)