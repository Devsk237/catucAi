# LegendBot - School Inquiry Assistant

A helpful and accurate school inquiry assistant powered by Google's Gemini AI. LegendBot provides instant answers to student questions by first checking authoritative school data, then falling back to web knowledge when needed.

## Features

- **Smart Data Integration**: Checks school database first for accurate, up-to-date information
- **AI-Powered Responses**: Uses Google Gemini 2.0 Flash for intelligent conversation
- **Web Interface**: Clean, modern web interface for real-time chat
- **Source Labeling**: Clearly indicates whether information comes from school data (firebase) or web knowledge
- **Example Questions**: Pre-built example questions for easy testing
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
school_inquiry_bot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Frontend functionality
└── data/
    └── sample_school_data.json  # Sample data for testing
```

## Setup Instructions

### 1. Clone or Download the Project

Download all files to your local machine or clone the repository.

### 2. Install Dependencies

```bash
cd school_inquiry_bot
pip install -r requirements.txt
```

### 3. Configure API Key

The application includes the provided Gemini API key. If you want to use a different key, update this line in `app.py`:

```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Basic Usage

1. Open your web browser and go to `http://localhost:5000`
2. Type your question in the input box and press Enter or click Send
3. LegendBot will respond with helpful information

### Using School Data

1. Copy your school data JSON and paste it in the "School Data" textarea
2. Click "Load School Data"
3. The bot will now优先 check this data before searching the web

### School Data Format

Your school data should be a JSON object with fields like:

```json
{
  "courses": {
    "course_name": {
      "name": "Course Name",
      "description": "Course description",
      "duration": "Duration",
      "prerequisites": "Requirements"
    }
  },
  "registrations": {
    "semester_name": {
      "deadline": "Date",
      "start_date": "Date",
      "form_link": "URL"
    }
  },
  "exams": {
    "exam_type": {
      "date_range": "Date range",
      "schedule": "Schedule info",
      "location": "Location"
    }
  },
  "faqs": [
    "Common question 1",
    "Common question 2"
  ],
  "contacts": {
    "department": {
      "phone": "Phone number",
      "email": "Email address",
      "office_hours": "Hours",
      "location": "Location"
    }
  }
}
```

## Example Questions

- "What courses are available?"
- "When is the registration deadline?"
- "How do I contact the admin office?"
- "What exams are coming up?"
- "What are the library hours?"
- "Is financial aid available?"

## API Endpoints

- `GET /` - Main web interface
- `POST /ask` - Ask a question (expects JSON with `question` and optional `school_data`)
- `GET /health` - Health check endpoint

## Response Format

LegendBot responses are clearly labeled with their source:

- `(source: firebase)` - Information from your school database
- `(source: web)` - Information from general web knowledge

## Technical Details

### Backend

- **Flask**: Web framework for the API
- **Requests**: HTTP client for Gemini API calls
- **Google Gemini 2.0 Flash**: AI model for generating responses

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Fetch API**: AJAX requests to backend

### Features

- Real-time chat interface
- Loading states and error handling
- Responsive design for mobile devices
- Character limit on input (500 characters)
- Automatic scrolling to new messages
- Time stamps on messages

## Testing

Use the provided `sample_school_data.json` file to test the functionality:

1. Copy the contents of `data/sample_school_data.json`
2. Paste it in the School Data textarea
3. Click "Load School Data"
4. Try questions like "What courses do you offer?" or "When is the fall registration deadline?"

## Deployment

To deploy this application:

1. Set up a web server (Apache, Nginx, etc.)
2. Configure WSGI for Flask application
3. Set up environment variables for API keys
4. Ensure all dependencies are installed
5. Configure proper security settings

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is valid and has proper permissions
2. **CORS Issues**: Ensure your web server allows cross-origin requests if needed
3. **Dependencies**: Install all required packages from requirements.txt

### Logs

Check the console output for error messages and debugging information.

## Contributing

Feel free to customize and extend this project:

- Add more school data fields
- Improve the UI/UX
- Add more intelligent response parsing
- Implement user authentication
- Add database persistence

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please check the troubleshooting section or examine the browser console for error messages.