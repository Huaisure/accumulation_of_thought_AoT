"""
Run Benchmark

Prompt Function Method

Task: Game of 24
"""

from .prompt_of_function.env.gameof24.gameof24_solver import GameOf24Solver
from .llm import GPT
from loguru import logger
import argparse
import datetime
import json


def run_task(task: str, solver: GameOf24Solver) -> str:
    return solver.solve_with_compress(task)


def benchmark(task_path: str, solver: GameOf24Solver):
    logger.remove()
    today = datetime.date.today().strftime("%m-%d")
    now = datetime.datetime.now().strftime("%H-%M-%S")
    logger.add(f"logs/experiment/gameof24/{today}/{now}.log", rotation="1 day")
    logger.info("** Start Benchmarking Game of 24 **")

    results = []
    with open(task_path, "r") as f:
        tasks = f.readlines()
    for task in tasks:
        task = json.loads(task)
        task_str = task["input"]
        logger.info(f"Task: {task_str}")
        res = run_task(task_str, solver)
        logger.info(f"Result: {res}")
        results.append({"input": task_str, "output": res})

    with open(f"results/gameof24/{today}/{now}.json", "w") as f:
        for res in results:
            f.write(json.dumps(res) + "\n")
    logger.info("** End Benchmarking Game of 24 **")


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser(description="Run benchmark")
    parser.add_argument("--model", type=str, default="gpt4o", help="Model name")
    parser.add_argument("--api_key", type=str, default=None, help="API key")
    parser.add_argument("--benchmark_path", type=str, default="benchmarks/gameof24.jsonl", help="Path to the benchmark file")
    args = parser.parse_args()

    assistant = GPT(model=args.model, api_key=args.api_key)
    solver = GameOf24Solver(assistant)
    benchmark(args.benchmark_path, solver)
