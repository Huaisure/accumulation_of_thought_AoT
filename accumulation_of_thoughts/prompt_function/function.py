from typing import List, Union

PROMPT_FUNCTION_SYSTEM_PROMPT = """
You are an advanced language model designed to assist with complex tasks.

To help you understand my request more easily, I'm going to use a template to describe the things I want to deal with, and I'll represent them as functions to avoid confusion and ambiguity.

The format of the function definition is as follows:
function <function_name>(input:[<argument_1>, <argument_2>, ...]) -> output:
    <rule>

The function may be used like this:
<function_name>(<argument_1>=<value_1>, <argument_2>=<value_2>, ...)
It means that you should generate the output based on the <input> and the <rule> provided in the function <function_name> definition.

Guidelines:
- Please follow the function definition format strictly.
- Ensure that the output adheres to the provided rules.
- If there are inner functions, please evaluate them first, and then use the results to evaluate the outer function.
"""


class PromptFunction:
    """
    Prompt Function defines a function that can be used to prompt the user for input.
    """

    def __init__(
        self,
        rule: List[str],
        name: str,
        input: List[str],
    ):
        self.name = name
        self.rule = rule
        self.input = input
        pass

    def __str__(self):
        name = self.name
        rule = "\n".join(self.rule)
        input = ", ".join(self.input)
        return f"""function {name}(input:[{input}]) -> output:
    {rule}
"""

    @staticmethod
    def function_definition(ls: Union[List["PromptFunction"], "PromptFunction"]) -> str:
        if ls.__class__ is PromptFunction:
            ls = [ls]
        func_num = len(ls)
        s = ""
        if func_num > 1:
            s = "s"
        define = (
            f"**Function Difinition**:\n{func_num} function"
            + s
            + " are difinted as follows:\n"
        )
        for i in range(func_num):
            define += f"{i+1}.\n{ls[i].__str__()}"
        define += "\n\n"
        return define
