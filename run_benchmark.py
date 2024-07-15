import argparse
import datetime

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
    aot = AccumulationOfThoughts(
        model_name=args.model,
        api_key=args.api_key,
        sentence_model_name=args.smodel,
        emb_pth=args.emb,
        template_pth=args.template,
        threshold=args.threshold,
        inputs=None,
        use_guidance=True,
    )

    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    logger.add(f"logs/{timestamp_str}.log")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmark for Accumulation of Thoughts")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML configuration file.")
    args = parser.parse_args()

    main(args)
