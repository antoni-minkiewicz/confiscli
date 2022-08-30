class Party:
    def __init__(self, val=" ", named=" ", description=" "):
        self.val = val
        self.named = named
        self.description = description
        self.make_attributes_valid()

    """TODO replace with a validity check first etc."""

    def make_attributes_valid(self):
        self.val = self.val.split()[0]
        self.named = self.named.replace('\n', '')
        self.description = self.description.replace('\n', '')

    def to_string(self):
        if self.val.isspace():
            return ""
        elif self.named.isspace():
            return "val " + self.val + " by party \n"
        elif self.description.isspace():
            str = "val " + self.val + " by party( \n"
            str += "\t\tnamed = \"" + self.named + "\"\n"
            str += ")\n"
            return str
        else:
            str = "val " + self.val + " by party( \n"
            str += "\t\tnamed = \"" + self.named + "\",\n"
            str += "\t\tdescription = \"" + self.description + "\"\n"
            str += ")\n"
            return str