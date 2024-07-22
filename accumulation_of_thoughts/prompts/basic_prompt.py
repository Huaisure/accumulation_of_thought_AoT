class BasicPrompt:
    @staticmethod
    def format(task: str, template) -> tuple:
        """
        Format the task and template into a system prompt and a user prompt.
        Args:
            task (str): The task details.
            template (dict): The template details.
        Returns:
            tuple: A tuple containing the system prompt and the user prompt.
        """
        problem_description = task["Description"]
        constraints = "\n- ".join(task["Constraints"])
        output_format = task["Format"]
        solving_process_flow = "\n    - ".join(template["Method"]["Flow"])
        pseudo_code = template["Method"]["Code"]
        explanation = "\n    - ".join(template["Method"]["Code Explanation"])
        system_prompt = """
You are an advanced language model designed to assist with complex tasks. Your objective is to follow the instructions and constraints provided to generate accurate and reliable solutions. For each task, ensure you adhere to the specified constraints, use the given method, and produce the output in the required format.

- Constraints: Follow all the constraints provided to ensure the solution is valid.
- Output Format: Present the final answer in the specified format.
- Method: Use the provided method, which may include a flow of the solving process and pseudo-code with explanations, to arrive at the solution.

Your responses should be clear, concise, and adhere strictly to the provided guidelines.
"""
        user_prompt = f"""
You are given the task of solving the following problem:

**Current Problem:**
- {problem_description}

**Constraints:**
- {constraints}

**Output Format:**
- {output_format}

**Method:**
- Follow this method to solve the task:
  - **Flow of Solving Process:**
    - {solving_process_flow}
  - **Pseudo-code:**
    - {pseudo_code}
  - **Explanation:**
    - {explanation}

Using the information provided, generate a solution that adheres to the constraints and is presented in the specified format.
"""
        # TODO: update the situation that there is no code provided
        return system_prompt, user_prompt
