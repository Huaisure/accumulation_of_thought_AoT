"""
Thoughts Template
4-tuple: (Description of the task, Method to solve the task, An example of the task and its answer, The classification of the task)
(D, M, E = (T, A), C)
load template given a template path and index
"""


class ThoughtsTemplate:
    """
    class of thoughts template
    dict: {D: description of the task, M: method to solve the task, E: example of the task and its answer, C: classification of the task}
    E = {T: task, A: answer}
    """

    def __init__(self, path, idx):
        """
        args:
        path: str, the path of the template file
        idx: int, the index of the template in the template file
        """
        self.path = path
        self.idx = idx
        self._gettemplate()

    def __getitem__(self, key):
        """
        key:[D, M, E, C], return the corresponding value
        """
        if key == "D":
            return self.D
        if key == "M":
            return self.M
        if key == "E":
            return self.E
        if key == "C":
            return self.C

    def _gettemplate(self) -> dict:
        idx = self.idx
        with open(self.path, "r") as file:
            templates = file.readlines()
        self.D, self.M, self.E, self.C = (
            templates[idx]["D"],
            templates[idx]["M"],
            templates[idx]["E"],
            templates[idx]["C"],
        )

    def update(self, idx, new_template):
        """
        Currently, this method only supports updating the template
        in the small file.
        """
        with open(self.path, "r") as file:
            templates = file.readlines()
        templates[idx] = new_template
        with open(self.path, "w") as file:
            file.writelines(templates)
