from typing import List
from prompt_of_function.function.function import PromptFunction
from .solve_stage import SolveStage
from .function import PROMPT_FUNCTION_SYSTEM_PROMPT

EVALUATE_TASK = "evaluate({question})"

evaluate_function = {
    "name": "evaluate",
    "input": ["a list of current states"],
    "rule": [
        "Here is a task: {task_description}, whose objective state is {objective}.",
        "Solving the problem requires a step-by-step exploration, here are some states (inputs to the function) that others have gotten after exploration",
        "Now you need to evaluate these states in the inputs in terms of the probability that these states can reach the objective, return as a list.",
        "The probabilities should be in range [0,1].",
        "Example: input=['state1', 'state2', 'state3'] -> output: [0.8, 0.2, 0.5]",
    ],
}


class EvaluateSolver(SolveStage):
    def __init__(
        self,
        task_description: str,
        objective: str,
        current_states: List[str],
        assistant,
    ) -> None:
        self.task_description = task_description
        self.objective = objective
        self.func = self.__evaluate_function()
        super().__init__(
            [self.func],
            EVALUATE_TASK.format(question=current_states),
            assistant,
            None,
            PROMPT_FUNCTION_SYSTEM_PROMPT,
        )

    def __evaluate_function(self):
        # Assuming evaluate_function is a global dictionary or defined elsewhere
        evaluate_function["rule"][0] = evaluate_function["rule"][0].format(
            task_description=self.task_description, objective=self.objective
        )
        return PromptFunction(**evaluate_function)

    def solve(self):
        return super().solve()
