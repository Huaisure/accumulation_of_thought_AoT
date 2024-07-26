import openai


class GPT:
    """
    GPT openai chatbot

    This class interfaces with the OpenAI GPT model.

    Args:
        api_key (str): openai api key
        model_id (str): openai model id
        temperature (float): temperature for the chatbot
    """

    def __init__(self, api_key, model_id, temperature=0.0):
        self.api_key = api_key
        self.model_id = model_id
        self.temperature = temperature

    def get_response(self, user_prompt, system_prompt=None, max_try=3):
        """
        Get the response from the chatbot

        Args:
            user_prompt (str): user prompt
            system_prompt (str): system prompt if have

        Returns:
            str: response from the chatbot
        """
        messages = self._prompt2messages(user_prompt, system_prompt)
        client = openai.OpenAI(
            api_key=self.api_key, base_url="https://gtapi.xiaoerchaoren.com:8932/v1"
        )

        # several tries
        for _ in range(max_try):
            try:
                response = client.chat.completions.create(
                    model=self.model_id, messages=messages, temperature=self.temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                continue
        # response = client.chat.completions.create(
        #     model=self.model_id, messages=messages, temperature=self.temperature
        # )
        # # print("response:",response)
        # return response.choices[0].message.content

    def _prompt2messages(self, user_prompt, system_prompt=None):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages


# gpt = GPT(
#     api_key="sk-Jp9YCIcVzEiwgIgg87F463EdC7F84992B8CcC4D6459d505a", model_id="gpt-4o"
# )

# # TODO: add an example in the user_prompt
# system_prompt = """
# You are an advanced language model designed to assist with complex tasks. Your objective is to follow the instructions and constraints provided to generate accurate and reliable solutions. For each task, ensure you thoroughly understand the task requirements and adhere to the specified constraints, use the given method, and produce the output in the required format.

# - **Constraints**: Follow all the constraints provided to ensure the solution is valid.
# - **Output Format**: Present the final answer in the specified format.
# - **Method**: Use the provided method, which may include a flow of the solving process and pseudo-code with explanations, to arrive at the solution. Reference any provided examples to guide your solution.

# Your responses should be clear, concise, and adhere strictly to the provided guidelines. Ensure to verify your solution against the constraints and the expected output format before finalizing your answer.
# """

# user_prompt = """You are given the task of solving the following problem:

# **Current Problem:**
# -
#     We are going to play a game called 24. You will be given four integers, and your objective is to use each number exactly once, combined with any of the four arithmetic operations (addition, subtraction, multiplication, and division) and parentheses, to achieve a total of 24.
#     Four integers:
#     3 3 7 12

# **Constraints:**
# - Usage of Numbers: All four given numbers must be used exactly once in the solution.
# - Allowed Operations: You can only use the basic arithmetic operations: addition (+), subtraction (-), multiplication (×), and division (÷).
# - Combination: Numbers can be combined in any order using parentheses to structure the operations as needed.
# - Result: The final result of the operations must be exactly 24.
# - No Repetition of Numbers: Each number must be used only once in the expression.
# - Intermediate Results: All intermediate results must be valid and must not involve division by zero or any undefined operations.

# **Output Format:**
# - The final answer should be presented in the format: "Final Answer: <expression with 4 given numbers and operations>"

# **Method:**
# - Follow this method to solve the task:
#   - **Flow of Solving Process:**
#     - Generate Permutations: Generate all possible permutations of the four given numbers. Since there are four numbers, there will be 4!=24 permutations.
#     - Generate Operator Combinations: Generate all possible combinations of three operators (addition, subtraction, multiplication, division) since you need three operations to combine four numbers.
#     - Generate Parentheses Combinations: Generate all valid ways to insert parentheses to define the order of operations. This includes considering all valid expressions such as (a⋅(b⋅(c⋅d))), (a⋅b)⋅(c⋅d), etc.
#     - Evaluate Expressions: Evaluate each generated expression. If an expression evaluates to 24, return it as a solution.
#   - **Pseudo-code:**
#     -
# function solveGameOf24(numbers):
#     permutations = generatePermutations(numbers)
#     operators = ['+', '-', '*', '/']
#     operatorCombinations = generateOperatorCombinations(operators, 3)
#     parenthesesCombinations = generateParenthesesCombinations()

#     for perm in permutations:
#         for opCombo in operatorCombinations:
#             for parens in parenthesesCombinations:
#                 expression = createExpression(perm, opCombo, parens)
#                 if evaluateExpression(expression) == 24:
#                     return "Final Answer: " + expression
#     return "No solution found"

# function generatePermutations(numbers):
#     // Returns all permutations of the list `numbers`

# function generateOperatorCombinations(operators, length):
#     // Returns all combinations of `length` operators from `operators`

# function generateParenthesesCombinations():
#     // Returns all valid parentheses combinations for expressions of four numbers and three operators

# function createExpression(perm, opCombo, parens):
#     // Creates an expression string from a permutation of numbers, a combination of operators, and a parentheses structure

# function evaluateExpression(expression):
#     // Evaluates the expression string and returns the result

#   - **Explanation:**
#     - generatePermutations: This function generates all possible ways to arrange the four numbers.
#     - generateOperatorCombinations: This function generates all possible combinations of three operators.
#     - generateParenthesesCombinations: This function generates all valid ways to insert parentheses into an expression involving four numbers and three operators.
#     - createExpression: This function constructs an expression string from a given permutation of numbers, combination of operators, and parentheses structure.
#     - evaluateExpression: This function evaluates the constructed expression to check if it equals 24.

# Using the information provided, generate a solution that adheres to the constraints and is presented in the specified format."""

# response = gpt.get_response(user_prompt, system_prompt)
# print(response)
