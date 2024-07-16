"""
Thoughts Template Class
4-tuple: (Description of the task, Method to solve the task, An example of the task and its answer, The classification of the task)
(D, M, E = (Q, A), C)
load template given a template path and index
"""

import json


class ThoughtsTemplate:
    """
    class of thoughts template
    dict: {D: description of the task, M: method to solve the task, E: example of the task and its answer, C: classification of the task}
    E = {Q: question, A: answer}
    """

    def __init__(self, path: str = None, idx: int = None, **kwargs):
        """
        args:
        path: str, the path of the template file
        idx: int, the index of the template in the template file
        """
        if path is not None:
            if idx is None:
                raise ValueError("Please provide the index of the template.")
            else:
                self.path = path
                self.idx = idx
                self._gettemplate()
        else:
            self.D = kwargs["D"]
            self.M = kwargs["M"]
            self.E = kwargs["E"]
            self.C = kwargs["C"]

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
        template = json.loads(templates[idx])
        self.D, self.M, self.E, self.C = (
            template["D"],
            template["M"],
            template["E"],
            template["C"],
        )

    def __dict__(self) -> dict:
        return {"D": self.D, "M": self.M, "E": self.E, "C": self.C}

    def upgrade(self, new_template: "ThoughtsTemplate"):
        """
        upgrade current template with the new template
        """
        new_file = []
        idx = 0
        # TODO: problem here
        with open(self.path, "r") as f:
            for line in f:
                if idx == self.idx:
                    new_file.append(json.dumps(new_template.__dict__()))
                else:
                    new_file.append(line)
                idx += 1
        with open(self.path, "w") as f:
            for line in new_file:
                f.write(line)
