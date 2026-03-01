import os
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

def file_processing(file_path):
    """Extract and process text from PDF file"""
    try:
        reader = PdfReader(file_path)
        text_content = ""
        
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
        
        # Basic text cleaning
        text_content = text_content.lower()
        
        # Remove URLs
        text_content = re.sub(r'http[s]?://\S+', '', text_content)
        text_content = re.sub(r'www\.\S+', '', text_content)
        
        return text_content
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return ""

def extract_key_topics(text_content, max_topics=20):
    """Extract key topics from text content"""
    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
    
    topics = []
    for line in lines:
        # Look for topic-like lines (not too short, not too long)
        if 15 < len(line) < 120:
            # Skip lines that are mostly numbers or special characters
            if sum(c.isalpha() for c in line) / len(line) > 0.5:
                topics.append(line)
        
        if len(topics) >= max_topics:
            break
    
    return topics

def generate_questions_simple(file_path, num_questions=10):
    """Generate questions without AI (fallback method)"""
    text_content = file_processing(file_path)
    
    if not text_content:
        return []
    
    topics = extract_key_topics(text_content, max_topics=num_questions * 2)
    
    questions = []
    question_templates = [
        "Explain the concept: {}",
        "What is the significance of: {}",
        "Describe the importance of: {}",
        "How does {} work?",
        "What are the key aspects of: {}",
    ]
    
    for i in range(min(num_questions, len(topics))):
        template = question_templates[i % len(question_templates)]
        questions.append(template.format(topics[i]))
    
    # Add generic questions if needed
    generic_questions = [
        "What are the main topics covered in this document?",
        "Explain the key concepts presented in the material.",
        "What practical applications are discussed?",
        "Describe the methodology or approach outlined.",
        "What are the important takeaways from this content?",
        "How can this knowledge be applied in practice?",
        "What are the challenges discussed in the material?",
        "What solutions or approaches are proposed?",
    ]
    
    while len(questions) < num_questions and len(questions) < len(generic_questions):
        questions.append(generic_questions[len(questions)])
    
    return questions[:num_questions]

def llm_pipeline(file_path, num_questions=10):
    """
    Generate questions using AI if configured, otherwise use simple extraction
    """
    # Check if HuggingFace token is configured
    if not HUGGINGFACE_TOKEN or HUGGINGFACE_TOKEN == 'your_huggingface_token_here':
        print("HuggingFace token not configured. Using simple question generation.")
        return generate_questions_simple(file_path, num_questions)
    
    # Try AI-powered generation if token is available
    try:
        from langchain_community.llms import HuggingFaceEndpoint
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from prompt import prompt_template
        
        # Get text content
        text_content = file_processing(file_path)
        
        if not text_content:
            return []
        
        # Initialize LLM
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            huggingfacehub_api_token=HUGGINGFACE_TOKEN,
            temperature=0.7,
            max_length=512
        )
        
        # Create prompt
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text", "num_questions"]
        )
        
        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate questions
        result = chain.run(text=text_content[:4000], num_questions=num_questions)
        
        # Parse questions from result
        questions = [q.strip() for q in result.split('\n') if q.strip() and any(c.isalpha() for c in q)]
        
        return questions[:num_questions] if questions else generate_questions_simple(file_path, num_questions)
        
    except Exception as e:
        print(f"AI generation failed: {e}. Falling back to simple generation.")
        return generate_questions_simple(file_path, num_questions)
    