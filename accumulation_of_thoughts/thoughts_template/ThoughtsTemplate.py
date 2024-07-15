"""
Thoughts Template Module
deal with the template of thoughts
"""


class ThoughtsTemplate:
    def __init__(self, path):
        self.path = path

    def gettemplate(self, idx: int) -> dict:
        with open(self.path, "r") as file:
            templates = file.readlines()
        return templates[idx]

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

    def add_template(self, new_template):
        with open(self.path, "a") as file:
            file.write(new_template)