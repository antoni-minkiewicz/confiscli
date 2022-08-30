class Clause:
    def __init__(self, party_val=" ", modal_verb=" ", action_val=" ", object_thing_or_party_val=" ", conditions=" ",
                 match_id="", string_id="", start="", end="", text="", full_sentence=""):

        self.party_val = party_val.lower()
        self.modal_verb = modal_verb
        self.action_val = action_val
        self.object_thing_or_party_val = object_thing_or_party_val.lower()
        self.conditions = conditions
        self.match_id = match_id
        self.string_id = string_id
        self.start = start
        self.end = end
        self.text = text
        self.full_sentence =full_sentence

        self.make_attributes_valid()

    """TODO replace with a validity check first etc."""

    def make_attributes_valid(self):
        return 0
        # self.val = self.val.split()[0]
        # self.named = self.named.replace('\n', '')
        # self.description = self.description.replace('\n', '')

    def to_string(self):
        if self.party_val.isspace():
            return ""
        elif self.conditions.isspace():
            return self.party_val + " " + self.modal_verb + " " + self.action_val + "(" + self.object_thing_or_party_val + ")\n\n"
        else:
            """TODO: this is where conditions will go"""
            str = self.party_val + " " + self.modal_verb + " " + self.action_val + "(" + self.object_thing_or_party_val + ")\n\n"
            return str