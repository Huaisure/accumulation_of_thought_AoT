from typing import List, Dict, Tuple
import re


def parselist(string: str) -> List[str]:
    """
    Parse the list from the string
    """
    # to parse: "[[1,2,3],[4,5,6]]"
    # result:['[1,2,3]','[4,5,6]'] List[str]
    string = string.replace(" ", "")
    string = string.strip("[] \n").split("],[")
    ls = ["[" + s + "]" for s in string]
    return ls


def replace_operators(ls: List[str]) -> List[str]:
    return [s.replace("×", "*").replace("÷", "/") for s in ls]


def clean_expression(expression: str) -> str:
    # Remove unmatched parentheses
    stack = []
    clean_expr = ""
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if stack:
                stack.pop()
                clean_expr += char
        else:
            clean_expr += char
    # Append remaining '(' in stack
    clean_expr += ")" * len(stack)
    return clean_expr


def safe_eval(expression: str) -> str:
    # Ensure the expression contains only numbers and operators
    if re.match(r"^[0-9+\-*/(). ]+$", expression):
        try:
            return str(eval(expression))
        except ZeroDivisionError:
            return None
        except Exception:
            return None
    return None


def check_brackets(expression: str) -> str:
    stack = []
    fixed_expr = expression
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if stack:
                stack.pop()
            else:
                fixed_expr = "(" + fixed_expr
    if stack:
        fixed_expr += ")" * len(stack)

    return fixed_expr


def parse_and_count(ls: List[str]) -> Tuple[List[Dict], List[str]]:
    ls_ = []
    fixed_ls = []
    for s in ls:
        count_dict = {}
        elements = s.strip("[]").split(",")
        fixed_ls.append("")

        for elem in elements:
            elem = elem.strip()
            if elem.strip("()").isdigit():
                key = elem
                fixed_ls[-1] += elem + ","
            else:
                checked_elem = check_brackets(elem)
                key = safe_eval(checked_elem)
                fixed_ls[-1] += checked_elem + ","
            if key:
                if key in count_dict:
                    count_dict[key] += 1
                else:
                    count_dict[key] = 1
        fixed_ls[-1] = fixed_ls[-1].strip(",")
        fixed_ls[-1] = "[" + fixed_ls[-1] + "]"
        ls_.append(count_dict)
    return ls_, fixed_ls


def remove_duplicates(ls: List[str], ls_: List[Dict]) -> List[str]:
    ls_copy = ls.copy()
    for i in range(len(ls_)):
        for j in range(i + 1, len(ls_)):
            if ls_[i] == ls_[j]:
                ls_copy[j] = "None"
    return [s for s in ls_copy if s != "None"]


def compress(ls: List[str]) -> List[str]:
    """
    Compress the list by removing the duplicates.

    If two items have exactly the same number (order is irrelevant), remove the duplicate.

    Args:
        ls: A list of lists of numbers and expressions

    Returns:
        A compressed list

    Example:
        >>> compress(['[(9+5),5,5]','[(9×5),5,5]','[5,(9+5),5]','[5,5,(5+9)]','[5,5,(2×7)]'])
        -> ['[(9+5),5,5]','[(9×5),5,5]']
    """
    ls = replace_operators(ls)
    ls_, fixed_ls = parse_and_count(ls)
    return remove_duplicates(fixed_ls, ls_)
