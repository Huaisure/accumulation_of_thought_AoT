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

Answer like this: (only present the input and output)
1. function <function_name>(input:[<argument_1>, <argument_2>, ...])
-> output: <output>
2. function <function_name>(input:[<argument_1>, <argument_2>, ...])
-> output: <output>
...
Unless otherwise specified, the output should be a non-linefeed string.

Guidelines:
- Please follow the function definition format strictly.
- Ensure that the output adheres to the provided rules.
- Output as requested, no explanation is needed.
- Use the probided functions, not define new ones.
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
        input = ", ".join(self.input)
        string = f"""function {name}(input:[{input}]) -> output:
Rules:
"""
        for i in range(len(self.rule)):
            string += f"    - {self.rule[i]}\n"
        return string

    def output_parse(self, response: str) -> str:
        """
        Parse the output from the response
        """
        response = response.split("function")
        for r in response:
            if self.name in r:
                r = r.split("\n")
                for rr in r:
                    if "output" in rr:
                        r = rr
                res = r.split("-> output:")[-1].strip()
        return res

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
            + " are difinted as follows:\n\n"
        )
        for i in range(func_num):
            define += f"{i+1}.\n{ls[i].__str__()}\n"
        define += "\n\n"
        return define


delete = "- If there are inner functions, please evaluate them first, and then use the results to evaluate the outer function."
