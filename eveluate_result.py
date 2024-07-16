import json
import argparse


def eveluate_result(task, result_dir):

    path_dict = {
        "gameof24": "benchmarks/gameof24.jsonl",
        "checkmate": "benchmarks/CheckmateInOne.jsonl",
        "wordsorting": "benchmarks/word_sorting.jsonl",
    }
    benchmark_dir = path_dict[task]
    to_eveluate = []

    benchmark = []
    with open(benchmark_dir, "r") as f:
        for line in f:
            benchmark.append(json.loads(line)["target"])
        f.close()
    correct = 0
    incorrect = []
    i = 0
    with open(result_dir, "r") as f:
        for line in f:
            to_eveluate.append(json.loads(line)["output"].strip())
            if task != "gameof24":
                if to_eveluate[i] == benchmark[i]:
                    correct += 1
                else:
                    incorrect.append(i)
            else:
                result = to_eveluate[i].split("=")[0]
                try:
                    if eval(result) == 24:
                        correct += 1
                    else:
                        incorrect.append(i)
                except Exception:
                    incorrect.append(i)


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser(description="Eveluate the result of Accumulation of Thoughts")
    parser.add_argument("--task", type=str, help="The task to evaluate")
    parser.add_argument("--result_dir", type=str, help="The directory of the result file")
    args = parser.parse_args()
    # fmt: on
    eveluate_result(args.task, args.result_dir)
