"""
Solve the problem with function prompt

# TODO:
1. 我是否需要先将问题解构，再传出去
2. base中需要实现什么样的功能
"""

from typing import List, Union, Dict
from .function import PromptFunction
from abc import abstractmethod


class FunctionSolverBase:
    """
    Base class for function solver

    Args:
        functions (List[PromptFunction]): The functions defined by the user
        func (Dict[str,PromptFunction]): The function dictionary

    Methods:

    """

    def __init__(self) -> None:
        self.functions: List[PromptFunction] = []
        self.func: Dict[str, PromptFunction] = {}

    def define_function_all(self):
        """
        Define all the involved functions

        Usually used at the beginning of the user prompt
        """
        return PromptFunction.function_definition(self.functions)

    def define_function(self, func_list: List[PromptFunction]):
        """
        Define the function

        Args:
            func_list (List[PromptFuntion]): the functions list to define
        """
        return PromptFunction.function_definition(func_list)

    def load_function(self, func_dict_list: List[dict]):
        """
        Load the function from the dictionary
        """
        for func in func_dict_list:
            self.functions.append(PromptFunction(**func))

        for func in self.functions:
            self.func[func.name] = func

    @abstractmethod
    def solve(self):
        """
        According to the specific task, return the specific expression composed of functions.
        """
        pass
