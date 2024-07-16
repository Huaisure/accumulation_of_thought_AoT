import argparse
import json
import datetime

from tqdm import tqdm
from .accumulation_of_thoughts import AccumulationOfThoughts
from loguru import logger


def main(args):
    GameOf24 = """
    Let's play a game called 24. You'll be given four integers, and your objective is to use each number only once, combined with any of the four arithmetic operations (addition, subtraction, multiplication, and division) and parentheses, to achieve a total of 24. For example, if the input is 4, 7, 8, and 8, the output could be 7 * 8 - 4 * 8 = 24. You only need to find one feasible solution!
    Input:
    """
    CheckmateInOne = """
    Given a series of chess moves written in Standard Algebraic Notation (SAN), determine the next move that will result in a checkmate.
    Input:
    """
    WordSorting = """
    Sort a list of words alphabetically, placing them in a single line of text separated by spaces.
    Input:
    """

    path_dict = {
        "gameof24": "benchmarks/gameof24.jsonl",
        "checkmate": "benchmarks/CheckmateInOne.jsonl",
        "wordsorting": "benchmarks/word_sorting.jsonl",
    }

    prompt_dict = {
        "gameof24": GameOf24,
        "checkmate": CheckmateInOne,
        "wordsorting": WordSorting,
    }

    if args.task not in path_dict:
        raise ValueError(
            f"Task {args.task} not supported. Choose from {list(path_dict.keys())}"
        )
    data_pth = path_dict[args.task]
    prompt = prompt_dict[args.task]

    aot = AccumulationOfThoughts(
        model_name=args.model,
        api_key=args.api_key,
        sentence_model_name=args.smodel,
        emb_pth=args.emb,
        template_pth=args.template,
        threshold=args.threshold,
        inputs=None,
        use_guidance=True,
        logger=logger,
    )

    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    model_name = args.model.strip("/").split("/")[-1]
    logger.remove()
    logger.add(
        f"logs/{args.task}_{model_name}_{timestamp_str}.log",
        format="{time} | {level} | {message}",
    )
    logger.info(f"Running benchmark for task {args.task}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Sentence model: {args.smodel}")
    logger.info(f"threshold: {args.threshold}")
    logger.info(f"Start Time:{timestamp_str}")

    # get the number of lines in the file
    count = 0
    with open(data_pth) as f:
        for ff in f:
            count += 1

    tq = tqdm(total=count)

    with open(data_pth) as f:
        for line in f:
            input = json.loads(line)["input"]
            inputs = prompt + input
            res = aot.run(inputs)
            tq.update(1)
            output = {"input": input, "output": res}
            with open(
                f"experiments/{args.task}/{model_name}_{timestamp_str}.jsonl", "a"
            ) as f_:
                f_.write(json.dumps(output) + "\n")
    tq.close()


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser(description="Run benchmark for Accumulation of Thoughts")
    parser.add_argument("--task", type=str, default="gameof24", help="Task name")
    parser.add_argument("--model", type=str, default="gpt4o", help="Model name")
    parser.add_argument("--api_key", type=str, default=None, help="API key")
    parser.add_argument("--smodel", "-s", type=str, default=None, required=True, help="Sentence model name")
    parser.add_argument("--emb", type=str, default=None, help="Path to embeddings")
    parser.add_argument("--template", "-t", type=str, default=None, help="Path to templates")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold for similarity")
    args = parser.parse_args()

    main(args)
