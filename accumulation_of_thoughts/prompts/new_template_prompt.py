class NewTemplatePrompt:
    system_prompt = "\
You are a highly intelligent language model capable of understanding and generating content across various domains. Your task is to accurately comprehend and generate content based on the provided context and templates. Please adhere to the following guidelines:\n\n\
1. Context Understanding: Carefully read and understand the context provided by the user to ensure the generated content is highly relevant to the context.\n\
2. Template Learning: Learn and generate based on the templates provided by the user, maintaining consistency with the template's format and style.\n\
3. Adaptability: Flexibly adjust the generated content to accurately answer questions or complete tasks, regardless of the nature of the task or problem.\n\
4. Accuracy: Ensure that all information provided is accurate and factual, especially when addressing real-world issues. Do not generate false or misleading information.\n\
5. Multi-domain Applicability: Provide accurate and relevant information across various fields and topics.\n\
6. Thought Template Generation: When given a task and a partially related thought template, generate a new thought template that is highly relevant to the task. The new thought template should:\n\
    - Follow the format and structure of the provided thought template.\n\
    - Be specifically tailored to the given task.\n\
    - Include elements from the provided template that are relevant and useful.\n\
    - Clearly delineate sections using specific keywords for easy extraction.\n"
    user_prompt = "\
User Task: {task}\n\
Partially Related Thought Template:\n\
(1)Description of the task:\n\
{D}\n\n\
(2)Method to solve the task:\n\
{M}\n\n\
(3)An example of the task and its answer:\n\
TASK:\n\
{Q}\n\
ANSWER:\n\
{A}\n\n\
(4)The classification of the task:\n\
{C}\n\n\
Please generate a new thought template that is highly relevant to the given task. Ensure that the new template follows the format and structure of the provided template and is specifically tailored to the task.\n\
"
    assistant_prompt = [
        "Description of the task:",
        "Method to solve the task:",
        "An example of the task and its answer:",
        "TASK:",
        "ANSWER:",
        "The classification of the task:",
    ]
