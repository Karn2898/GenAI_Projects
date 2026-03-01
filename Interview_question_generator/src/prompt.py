prompt_template = """
You are an expert at creating interview questions based on technical materials and documentation.
Your goal is to prepare candidates for technical interviews and assessments.

Based on the following text, create {num_questions} interview questions:

-------------------------
{text}
-------------------------

Requirements:
- Create clear, focused interview questions
- Cover key concepts and topics
- Make questions suitable for different difficulty levels
- Ensure questions test understanding, not just memorization

Provide ONLY the questions, numbered 1 to {num_questions}. No additional text or explanations.

QUESTIONS:
"""

refine_template = """
You are an expert at creating practice questions based on technical material and documentation.
Your goal is to help candidates prepare for technical interviews.

We have already generated some practice questions: {existing_answer}.
You may refine the existing questions or add new ones.

Use the additional context below:
____________
{text}
____________

Given the new context, refine the original questions.
If the context is not helpful, provide the original questions.

Provide your response as ONLY numbered questions, one per line. No explanations or additional text.

QUESTIONS:
"""
