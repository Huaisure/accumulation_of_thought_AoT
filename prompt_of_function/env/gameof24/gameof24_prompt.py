STAGE1_TASK = "Compression(Choose2Numbers({task}))"

STAGE2_TASK = "Compression(Choose2NumbersForEachItem({list}))"

STAGE3_TASK = "Evaluate({list})"

STAGE3_TASK_ = """list = Choose2NumbersForEachItem({list})
For item in list:
    if EvaluateExpression(item,{task}) is True:
        return item
If no item satisfies the condition, return None
"""

STAGE1_TASK_WITHOUT_COMPRESSION = "Choose2Numbers({task})"

STAGE2_TASK_WITHOUT_COMPRESSION = "Choose2NumbersForEachItem({list})"
