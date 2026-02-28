prompt_template = """
You are an expert at creating questions based on coding materials and documentation.
Your goal is to prepare a coder or programmer for exams and coding tests.
You do this by asking questions about the text below:

-------------------------
{text}
-------------------------
Create questions that will prepare coders or programmers for the test.
Make sure not to miss any important information.

Provide your response as ONLY numbered questions, one per line. No explanations or additional text.

QUESTIONS:
"""

refine_template = """
You are an expert at creating practice questions based on coding material and documentation.
Your goal is to help a coder or programmer prepare for a coding test.
We have already generated some practice questions: {existing_answer}.
You may refine the existing questions or add new ones.
Use the additional context below only if necessary.
____________
{text}
____________

Given the new context, refine the original questions in English.
If the context is not helpful, provide the original questions.

Provide your response as ONLY numbered questions, one per line. No explanations or additional text.

QUESTIONS:
"""
