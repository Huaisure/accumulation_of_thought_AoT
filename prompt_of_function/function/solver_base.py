from .function import PromptFunction, PROMPT_FUNCTION_SYSTEM_PROMPT
from .solve_stage import SolveStage

from typing import List, Union, Dict
from abc import abstractmethod


class FunctionSolverBase:
    """
    Base class for function solver

    Args:
        functions (List[PromptFunction]): The functions defined by the user
        func (Dict[str,PromptFunction]): The function dictionary

    """

    functions: List[PromptFunction] = []
    func: Dict[str, PromptFunction] = {}
    solve_stage: List[SolveStage] = []

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

    def _set_stage(
        self,
        func_list,
        task: str,
        outermost_func=None,
        system_prompt: str = PROMPT_FUNCTION_SYSTEM_PROMPT,
    ):
        """set the stage"""
        self.solve_stage.append(
            SolveStage(
                func_list,
                task,
                self.assistant,
                outermost_func,
                system_prompt,
            )
        )

    @abstractmethod
    def solve(self):
        """
        According to the specific task, return the specific expression composed of functions.
        """
        pass
