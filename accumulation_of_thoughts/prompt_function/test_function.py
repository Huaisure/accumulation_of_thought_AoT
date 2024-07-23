from .function import PromptFunction, PROMPT_FUNCTION_SYSTEM_PROMPT
from ..llm import GPT

# python -m accumulation_of_thoughts.prompt_function.test_function

api_key = "sk-Jp9YCIcVzEiwgIgg87F463EdC7F84992B8CcC4D6459d505a"
model_id = "gpt-4o"
gpt = GPT(api_key=api_key, model_id=model_id)

system_prompt = PROMPT_FUNCTION_SYSTEM_PROMPT

func1 = PromptFunction(
    rule=["Return the sum of the <a> and <b>."],
    name="add",
    input=["a", "b"],
)

func2 = PromptFunction(
    rule=["Return the multiplication of the <a> and <b>."],
    name="multiply",
    input=["a", "b"],
)

user_prompt = PromptFunction.function_definition([func1, func2])
user_prompt += (
    "Question: add(a=1, b=multiply(a=2, b=3))\nGenerate the result in Question."
)

print(user_prompt)

response = gpt.get_response(user_prompt, system_prompt)

print(response)
