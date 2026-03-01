# Interview Question Generator



https://github.com/user-attachments/assets/0d71c7a9-3b2b-4f62-b9d5-094583c6e594


An AI-powered application that automatically generates interview questions from PDF documents. Upload your PDF, and the system will extract key concepts and generate relevant interview questions with optional AI enhancement using HuggingFace.

## Features

- **PDF Upload**: Drag-and-drop or click to upload PDF files
- **Question Generation**: Automatically generates interview questions from document content
- **Multiple Question Types**: Concept explanation, applications, methodologies, and more
- **Configurable**: Adjust number of questions and difficulty levels
- **AI-Ready**: Built with support for HuggingFace LLMs for enhanced generation
- **Web Interface**: Clean, modern UI for easy interaction
- **API Endpoints**: RESTful endpoints for programmatic access

## Prerequisites

- **Python**: 3.10 or higher
- **Virtual Environment**: venv, conda, or pipenv
- **Git**: For version control
- **HuggingFace Token** (Optional): For AI-powered question generation
  - Get one at: https://huggingface.co/settings/tokens

## Project Structure

```
Interview_question_generator/
├── src/
│   ├── app.py              # FastAPI application with endpoints
│   ├── helper.py           # Question generation pipeline
│   ├── prompt.py           # LLM prompt templates
│   └── __init__.py
├── templates/
│   └── index.html          # Web UI
├── static/
│   ├── docs/               # Uploaded PDFs (generated at runtime)
│   └── output/             # Generated CSV files (generated at runtime)
├── Requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Karn2898/GenAI_Projects.git
cd GenAI_Projects/Interview_question_generator
```

### 2. Create Virtual Environment

#### Option A: Using venv (Python built-in)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Option B: Using conda

```bash
conda create -n interview-gen python=3.10 -y
conda activate interview-gen
```

#### Option C: Using pipenv

```bash
pipenv install --python 3.10
pipenv shell
```

### 3. Install Dependencies

```bash
pip install -r Requirements.txt
```

## Configuration

### Basic Setup (No AI)

The application works out-of-the-box with simple PDF text extraction. No configuration needed.

### Enable AI-Powered Generation (Optional)

1. **Get HuggingFace Token**:
   - Visit https://huggingface.co/settings/tokens
   - Create a new token with read permissions

2. **Create `.env` file**:

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your token
# Windows
notepad .env

# Linux/Mac
nano .env
```

3. **Add your token**:

```env
HUGGINGFACE_TOKEN=hf_your_token_here
```

## Running the Application

### Start the Server

```bash
cd src

# Windows (PowerShell)
.\..\..\venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8081

# Windows (Command Prompt)
python -m uvicorn app:app --host 127.0.0.1 --port 8081

# Linux/Mac
python -m uvicorn app:app --host 127.0.0.1 --port 8081
```

Server will start at: `http://127.0.0.1:8081`

### Access the Application

1. **Open in Browser**:
   ```
   http://127.0.0.1:8081/
   ```

2. **Interactive API Docs**:
   ```
   http://127.0.0.1:8081/docs
   ```

### Using the Web Interface

1. **Upload PDF**:
   - Click on the upload area or drag & drop a PDF file
   - Select the file and it will show the file name

2. **Configure Options**:
   - **Number of Questions**: 1-50 (default: 10)
   - **Difficulty Level**: Easy, Medium, Hard, or Mixed
   - **Topic/Subject** (Optional): Specify the topic for better filtering

3. **Generate Questions**:
   - Click "Generate Questions" button
   - Wait for processing (usually 5-30 seconds depending on PDF size)
   - View generated questions in the results panel

4. **Download Results**:
   - Click "Download Questions as JSON" to export the questions

## API Endpoints

### 1. Home Page

```
GET /
```

Returns the web interface HTML.

### 2. Upload PDF

```
POST /upload
```

**Parameters:**
- `pdf_file` (file): PDF file to upload
- `filename` (string): Name to save the file as

**Response:**
```json
{
  "msg": "success",
  "pdf_filename": "/static/docs/filename.pdf",
  "file_path": "C:\\path\\to\\file"
}
```

**Example (curl)**:
```bash
curl -X POST http://127.0.0.1:8081/upload \
  -F "pdf_file=@document.pdf" \
  -F "filename=document.pdf"
```

### 3. Generate Questions

```
POST /generate
```

**Parameters:**
- `file_path` (string): Full path to the PDF file
- `num_questions` (integer): Number of questions to generate (default: 10)

**Response:**
```json
{
  "questions": [
    {"question": "What are the main topics covered in this document?"},
    {"question": "Explain the key concepts presented in the material."},
    ...
  ],
  "total": 10
}
```

**Example (curl)**:
```bash
curl -X POST http://127.0.0.1:8081/generate \
  -d "file_path=C:/path/to/file.pdf&num_questions=10"
```

### 4. API Documentation

```
GET /docs
```

Interactive Swagger UI documentation for all endpoints.

## Command Examples

### Full Workflow via API

```bash
# 1. Upload a PDF
curl -X POST http://127.0.0.1:8081/upload \
  -F "pdf_file=@machine-learning.pdf" \
  -F "filename=machine-learning.pdf"

# 2. Generate questions
curl -X POST http://127.0.0.1:8081/generate \
  -d "file_path=C:/Users/YourName/GenAI_Projects/Interview_question_generator/static/docs/machine-learning.pdf&num_questions=8"

# 3. Save output (Linux/Mac)
curl -X POST http://127.0.0.1:8081/generate \
  -d "file_path=/path/to/file.pdf&num_questions=8" > questions.json
```

## Troubleshooting

### Issue: Port 8081 Already in Use

**Solution**: Use a different port
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8082
```

### Issue: Module Not Found Errors

**Solution**: Reinstall dependencies
```bash
pip install -r Requirements.txt --force-reinstall
```

### Issue: PDF Upload Fails

**Solution**: Check file permissions and ensure `static/docs/` directory exists
```bash
# Create directories if missing
mkdir -p static/docs
mkdir -p static/output
```

### Issue: Question Generation Times Out

**Solution**: Try with a smaller PDF or fewer questions
- Start with 5 questions
- Use smaller PDF files (< 50 MB)
- Check server logs for errors

### Issue: HuggingFace AI Not Working

**Solution**: Verify configuration
```bash
# Check if token is set
echo $HUGGINGFACE_TOKEN  # Linux/Mac
echo %HUGGINGFACE_TOKEN% # Windows

# Verify .env file has correct token
cat .env  # Linux/Mac
type .env # Windows
```

## Development

### Project Dependencies

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | ASGI server |
| python-multipart | Form data handling |
| aiofiles | Async file operations |
| PyPDF2 | PDF text extraction |
| jinja2 | HTML templating |
| langchain | AI pipeline (optional) |
| python-dotenv | Environment variables |

### Running in Development Mode (with auto-reload)

```bash
cd src
python -m uvicorn app:app --host 127.0.0.1 --port 8081 --reload
```

### Creating a New Feature

1. Edit the relevant file in `src/`
2. Server will auto-reload if using `--reload` flag
3. Test via API docs at `/docs`

## Question Generation Methods

### 1. Simple Method (Default)
- Extracts text from PDF
- Identifies key topics
- Generates questions about those topics
- **No external API required**
- **Fast (< 5 seconds)**

### 2. AI Method (With HuggingFace)
- Uses Mistral 7B or similar model
- Generates more contextual questions
- **Requires HuggingFace token**
- **Slower (30-60 seconds)**

## Output Formats

### JSON Output
```json
{
  "questions": [
    {"question": "What are the main topics covered in this document?"},
    {"question": "Explain the key concepts presented in the material."}
  ],
  "total": 2
}
```

### CSV Output (via `/get_csv` endpoint - optional)
```
Question,Answer
"What is the main concept?","..."
"How does it work?","..."
```

## Performance Notes

- **Small PDFs (< 5 MB)**: < 3 seconds
- **Medium PDFs (5-20 MB)**: 3-15 seconds
- **Large PDFs (> 20 MB)**: 15-60 seconds
- **AI Generation**: Add 20-40 seconds

## Security Considerations

- **Don't commit `.env` file** with real tokens to Git
- **Use `.env.example`** as template only
- **Validate file uploads** (already done)
- **Limit PDF file size** for production (add in future)
- **Use HTTPS** in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Commit with descriptive messages
6. Push and create a Pull Request

## License

This project is part of the GenAI_Projects repository. See LICENSE file for details.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review server logs
3. Check `/docs` endpoint for API issues
4. Open an issue on GitHub

## Future Enhancements

- [ ] Answer generation with explanations
- [ ] Multiple PDF batch processing
- [ ] Question difficulty ranking
- [ ] Export to multiple formats (PDF, DOCX)
- [ ] Question filtering and editing UI
- [ ] User authentication
- [ ] Database for storing generated questions
- [ ] Advanced NLP for better topic extraction

## Changelog

### v1.0.0 (March 1, 2026)
- Initial release
- PDF upload and text extraction
- Basic question generation
- Web UI
- API endpoints
- HuggingFace AI integration (optional)

---

**Happy generating!**
