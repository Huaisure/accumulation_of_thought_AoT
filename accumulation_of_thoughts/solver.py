"""
Solve the problem with function prompt

# TODO:
1. 我是否需要先将问题解构，再传出去
2. base中需要实现什么样的功能
"""

from typing import List, Union
from prompt_function import PromptFunction
from abc import abstractmethod


class FunctionSolverBase:
    """
    Base class for function solver

    Args:
        functions (List[PromptFunction]): The functions defined by the user

    Methods:

    """

    def __init__(self, functions: List[PromptFunction] = None):
        self.functions = functions

    def define_function(self):
        pass

    @abstractmethod
    def solve(self):
        """
        According to the specific task, return the specific expression composed of functions.
        """
        pass
