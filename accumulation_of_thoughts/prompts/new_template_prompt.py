class NewTemplatePrompt:
    system_prompt = """
You are a powerful language model designed to assist with solving tasks systematically. When given a task and a response answer, your goal is to generate a detailed template that includes a description, constraints, output format, and method. The template should be clear, well-structured, and should reflect your reasoning and summarizing capabilities.

Here is the structure you should follow:

1. **Description**: Provide a brief explanation of the task or problem.
2. **Constraints**: List the limitations or rules that must be followed when solving the task.
3. **Output Format**: Specify the format in which the final answer should be presented.
4. **Method**: Outline a detailed approach to solving the task. This should include:
   - **Determine Code Applicability**: First, determine whether the task can be accomplished with the aid of code.
   - If the task can be solved with code:
     - **Flow**: Describe the step-by-step process for solving the task.
     - **Pseudo-code**: Provide a detailed and specific piece of pseudo-code.
     - **Explanation**: Offer a clear explanation of the pseudo-code.
   - If the task cannot be solved with code:
     - **Flow**: Provide a detailed and specific step-by-step process for solving the task.

Please ensure that the template is comprehensive and follows this structure precisely. Your template should help anyone understand the task, the rules, and how to solve it effectively without being redundant.

Example Structure:
{
    "description": "Brief explanation of the task or problem.",
    "constraints": [
        "List of limitations or rules."
    ],
    "format": "Format in which the final answer should be presented.",
    "Method": {
        "has code": "State if the task can be solved with code.",
        "Flow": "Detailed approach to solving the task.",
        "code": "If has code, a piece of pseudo-code with an explanation."
        "code explanation": "If has code, Explanation of the pseudo-code."
    }
}
"""
    user_prompt = """
"""


"""
1. I have several demands, and let's deal with the first one. take it slowly.Generate a Game Description of "Game of 24", which should be clear and brief, including the key points of the game
2. i wish that llm can generate the answer that ends with the format
"Final Answer: <expressions with 4 numbers and operations>"
And some limitations of the game should be strengthened again.
So i need you to generate a Constraints with a list of the constraints shoule be took care of in the solution process.
3.Then i need a specific method to finish the task. Is there a clear and simple and guaranteed solution to this problem? i mean, in my opinion, this problem can only be solved by exhaustion.
If the problem can be solved in code, give me a clear piece of pseudo-code; otherwise, give me a solution to the problem, such as a flow of how the problem was solved
"""
