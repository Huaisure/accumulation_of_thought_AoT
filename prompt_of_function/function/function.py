from typing import List, Union
import warnings

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
- Note the formatting, examples are given in the function rules.
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
        self.input = input
        self.rule = rule
        pass

    def __str__(self):
        name = self.name
        input = ", ".join(self.input)
        string = f"""function {name}(input:[{input}]) -> output:
Rules:
"""
        for i in range(len(self.rule)):
            string += f"- {self.rule[i]}\n"
        return string

    def output_parse(self, response: str) -> str:
        """
        Parse the output from the response
        """
        res = None
        if response.count(self.name) > 1:
            warnings.warn(
                f"LLM's output contains multiple parts that contain the function name {self.name}, which may lead to incorrect parsing of the output.\nBy default, the results of these parts are processed according to stitching them together."
            )
            response_ = response.split("function")
            res = []
            for r in [r_ for r_ in response_ if self.name in r_]:
                r = r.split("\n")
                output_idx = 1e9
                for i in range(len(r)):
                    if "output" in r[i]:
                        res.append(r[i].split("output")[-1].strip(" :"))
                        output_idx = i
                    if i > output_idx:
                        if r[i] != "":
                            res[-1] += r[i].strip(" :")
            return ",".join(res)

        if self.name not in response:
            warnings.warn(
                f"LLM's output does not contain the function name {self.name}, which has been required in the system prompt. This may lead to incorrect parsing of the output."
            )
            response = response.split("output")[-1].strip(" :")
            response = response.split("\n")
            res = ""
            for r in response:
                if r != "":
                    res += r
            return res
        response = response.split("function")
        for r in response:
            if self.name in r:
                r = r.split("\n")
                output_idx = 1e9
                for i in range(len(r)):
                    if "output" in r[i]:
                        res = r[i].split("output")[-1].strip(" :")
                        output_idx = i
                    if i > output_idx:
                        if r[i] != "":
                            res += r[i].strip(" :")
                return res

    @staticmethod
    def function_definition(ls: Union[List["PromptFunction"], "PromptFunction"]) -> str:
        """
        String representation of the function definition

        Args:
            ls (Union[List[PromptFunction], PromptFunction]): The function list

        Returns:
            str: The string representation of the function definition
        """
        if ls.__class__ is PromptFunction:
            ls = [ls]
        func_num = len(ls)
        define = (
            f"**Function Difinition**:\n{func_num} function" + "s are "
            if func_num > 1
            else " is " + "difinted as follows:\n\n"
        )
        for i in range(func_num):
            define += f"{i+1}.\n{ls[i].__str__()}\n"
        define += "\n\n"
        return define
