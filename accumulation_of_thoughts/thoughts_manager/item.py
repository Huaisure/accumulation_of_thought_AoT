import json
import warnings


class ThoughtItem:
    """
    class of thought item

    keys:
        id: int, the id of the thought item
        description: str, the description of the thought task
        method: dict, the method to solve the task
            - flow: list, the flow of the solving process
            - has code: bool, whether the method has code
            - code: str, the pseudo code
            - code explanation: list, the explanation of the code
        constraints: list, the constraints of the thought task
        format: str, the format of the output
        category: str, the category of the thought task

    """

    KEY_DICT = {
        "id": "int, the id of the thought item",
        "description": "str, the description of the thought task",
        "method": "dict, the method to solve the task",
        "constraints": "list, the constraints of the thought task",
        "format": "str, the format of the output",
        "category": "str, the category of the thought task",
    }

    def __init__(self, path: str = None, idx: int = None):
        """
        args:
            path: str, the path of the template file
            idx: int, the index of the template in the template file
        """
        self.path = path
        self.idx = idx
        self.data = self._gettemplate()

    def _gettemplate(self) -> dict:
        idx = self.idx
        with open(self.path, "r") as file:
            templates = file.readlines()
        template = json.loads(templates[idx])
        # check if id matches, else warn
        if template["id"] != self.idx:
            warnings.warn(
                f"The index in the template file does not match the thought id {idx}."
            )
        return template

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f"{key} not found in the thought item.")

    def upgrade(self, new_item: dict):
        """
        upgrade current template with the new template
        """
        new_file = []
        idx = 0
        original_data = self.data
        new_data = {}
        for key in original_data:
            if key in new_item:
                new_data[key] = new_item[key]
            else:
                new_data[key] = original_data[key]
        with open(self.path, "r") as f:
            for line in f:
                if idx == self.idx:
                    new_file.append(json.dumps(new_data))
                else:
                    new_file.append(line)
                idx += 1
        with open(self.path, "w") as f:
            for line in new_file:
                f.write(line)

    def __repr__(self):
        return f"ThoughtItem({self.data})"

    def help(self):
        """
        return the key dict
        """
        return self.KEY_DICT
