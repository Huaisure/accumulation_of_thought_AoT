from typing import List


def parselist(string: str) -> List[str]:
    """
    Parse the list from the string
    """
    # to parse: "[[1,2,3],[4,5,6]]"
    # result:['[1,2,3]','[4,5,6]'] List[str]
    string = string.strip("[] \n").split("],[")
    ls = ["[" + s + "]" for s in string]
    return ls
