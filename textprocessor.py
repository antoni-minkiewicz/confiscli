import json
import re
from json import JSONEncoder
from operator import itemgetter

import spacy
from spacy import displacy
from spacy.matcher import Matcher, DependencyMatcher

import utils
from clausematcher import ClauseMatcher
from confiscomponents.action import Action
from confiscomponents.clause import Clause
from confiscomponents.party import Party
from confiscomponents.thing import Thing
from textprocessorinterface import TextProcessorInterface


class TextProcessor(TextProcessorInterface):
    def __init__(self, clause_matcher= ClauseMatcher()):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except BaseException as e:
            print("You need to download \"en_core_web_sm\" ")
            raise e

        self.clause_matcher = clause_matcher
        self.confis_meta_file = None
        self.confis_file = None

        self.confis_meta = {
            "parties": [],
            "actions": [],
            "things": [],
            "definitions": [],
            "clauses": [],
            "clause_matcher_output": [],
            "sentences": [],
        }

    """This method goes from txt to nlp-post-hitl"""

    def run_full_extraction(self, txt, confis_meta_file, confis_file):
        self.confis_meta_file = confis_meta_file
        self.confis_file = confis_file

        self.confis_meta["clause_matcher_output"] = utils.convert_list_of_list_of_tuples_to_list_of_lists(self.clause_matcher.extraction_to_hierarchical_json_from_txt(txt))

        """Processing"""
        # self.confis_meta["ner"] = self.get_named_entities(txt)
        self.confis_meta["parties"] = self.get_parties_from_txt_yes_hitl(txt)
        self.confis_meta["things"] = self.get_things_from_txt_no_hitl(txt)
        self.confis_meta["actions"] = self.get_actions_from_txt_no_hitl(txt)
        self.confis_meta["sentences"] = self.get_properly_split_text_into_roots_circumstances_and_untranslatable(txt)
        self.confis_meta["clauses"] = self.get_confis_clauses_from_txt_no_hitl(txt)


        self.make_confis_meta_object_valid()

        """Removing definitions that never get used"""
        self.remove_parties_without_clauses()
        self.remove_things_without_clauses()
        self.remove_actions_without_clauses()

        self.remove_things_that_are_also_parties()

        """Output"""
        self.generate_confis_meta_file()
        self.generate_confis_contract_from_confis_meta()

        """FOR TESTING"""
        # self.print_sentences()

    """Processing Methods"""

    def get_named_entities(self, txt):
        doc = self.nlp(txt)

        matcher = Matcher(self.nlp.vocab)

        patterntwo = [{"ENT_TYPE": "ORG"}]
        patternthree = [{"ENT_TYPE": "PERSON"}]
        matcher.add("clausetwo", [patterntwo, patternthree], greedy='LONGEST')

        matches = matcher(doc)

        ne = []

        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            ne.append(span.text)

        return ne

    def get_parties_in_clauses(self):
        """TODO: You need to account for parties which only appear as objects of the clause"""
        parties_in_clauses = []
        for clause in self.confis_meta["clauses"]:
            if clause.party_val not in parties_in_clauses:
                parties_in_clauses.append(clause.party_val)
        return parties_in_clauses

    def remove_parties_without_clauses(self):
        parties_in_clauses = self.get_parties_in_clauses()
        new_parties = []
        for party in self.confis_meta["parties"]:
            if party.val in parties_in_clauses:
                new_parties.append(party)
        self.confis_meta["parties"] = new_parties

    def get_things_in_clauses(self):
        things_in_clauses = []
        for clause in self.confis_meta["clauses"]:
            if clause.object_thing_or_party_val not in things_in_clauses:
                things_in_clauses.append(clause.object_thing_or_party_val)
        return things_in_clauses

    def remove_things_without_clauses(self):
        things_in_clauses = self.get_things_in_clauses()
        new_things = []
        for thing in self.confis_meta["things"]:
            if thing.val in things_in_clauses:
                new_things.append(thing)
        self.confis_meta["things"] = new_things

    def get_actions_in_clauses(self):
        actions_in_clauses = []
        for clause in self.confis_meta["clauses"]:
            if clause.action_val not in actions_in_clauses:
                actions_in_clauses.append(clause.action_val)
        return actions_in_clauses

    def remove_actions_without_clauses(self):
        actions_in_clauses = self.get_actions_in_clauses()
        new_actions = []
        for party in self.confis_meta["actions"]:
            if party.val in actions_in_clauses:
                new_actions.append(party)
        self.confis_meta["actions"] = new_actions

    """IO Methods"""

    def make_confis_meta_object_valid(self):
        self.make_parties_valid_in_confis_meta_object()
        self.make_things_valid_in_confis_meta_object()
        self.make_clauses_valid_in_confis_meta_object()

    def make_clauses_valid_in_confis_meta_object(self):
        for clause in self.confis_meta["clauses"]:
            if clause.has_conditions:
                for condition in clause.conditions:
                    condition_text = self.remove_non_alphanumeric_characters_from_string(condition[0])
                    condition[0] = condition_text

    def make_parties_valid_in_confis_meta_object(self):

        """Making party val names unique"""
        party_vals = []
        for party in self.confis_meta["parties"]:
            party_vals.append(party.val)

        party_vals_new = []
        for i, ele in enumerate(party_vals):
            count = 0
            for party_val in party_vals[:i]:
                if ele == party_val:
                    count += 1
            if count == 0:
                party_vals_new.append(ele)
            else:
                party_vals_new.append(ele + str(count))

        for i, ele in enumerate(self.confis_meta["parties"]):
            ele.val = party_vals_new[i]

        """Making party val names kotlin legal (filtering out keywords and no alphanum chars)"""

    def make_things_valid_in_confis_meta_object(self):
        """Removing non-alphanumeric characters from thing vals"""

        """Making thing val names unique"""
        thing_vals = []
        for thing in self.confis_meta["things"]:
            string = self.remove_non_alphanumeric_characters_from_string(thing.val)
            thing_vals.append(string)

        thing_vals_new = []
        for i, ele in enumerate(thing_vals):
            count = 0
            for thing_val in thing_vals[:i]:
                if ele == thing_val:
                    count += 1
            if count == 0:
                thing_vals_new.append(ele)
            else:
                thing_vals_new.append(ele + str(count))

        for i, ele in enumerate(self.confis_meta["things"]):
            ele.val = thing_vals_new[i]

    def remove_things_that_are_also_parties(self):
        party_vals = []
        for party in self.confis_meta["parties"]:
            party_vals.append(party.val)
        for thing in self.confis_meta["things"]:
            if thing.val in party_vals:
                self.confis_meta["things"].remove(thing)

    def generate_confis_meta_file(self):
        """This converst the confis_meta attribute to a JSON file
        It assumes that the confis_meta attribute of the text processor has been created"""

        with open(self.confis_meta_file, 'w', encoding='utf-8') as f_out:
            json_object = json.dumps(self.confis_meta, indent=4, cls=PartyEncoder)
            f_out.write(json_object)

    def generate_confis_contract_from_confis_meta(self):
        with open(self.confis_file, 'w', encoding='utf-8') as f_out:
            f_out.write("\"\"\"Parties\"\"\"\n\n")
            for party in self.confis_meta["parties"]:
                f_out.write(party.to_string())
            f_out.write("\"\"\"Things\"\"\"\n\n")
            for thing in self.confis_meta["things"]:
                f_out.write(thing.to_string())
            f_out.write("\"\"\"Actions\"\"\"\n\n")
            for action in self.confis_meta["actions"]:
                f_out.write(action.to_string())
            f_out.write("\"\"\"Clauses\"\"\"\n\n")

            clause_counter = 0
            for clause in self.confis_meta["clauses"]:
                clause_counter += 1
                f_out.write("\"\"\"" + str(clause_counter) + "\"\"\"" + "\n")
                f_out.write(clause.to_string())

    """This goes from nlp-pre-hitl to nlp-post-hitl"""

    def get_parties_from_txt_yes_hitl(self, txt):
        return self.get_parties_from_txt_no_hitl(txt)

    """This goes from txt to nlp-pre-hitl"""

    def get_parties_from_txt_no_hitl(self, txt):
        doc = self.nlp(txt)
        parties = []
        unique_propn_chunk = []
        party_vals = []
        for token in doc.noun_chunks:
            # if token.text[0].isalpha():
            if token.text not in unique_propn_chunk:
                str = self.nlp(token.text)
                if str[0].pos_ == "NOUN" or str[0].pos_ == "PROPN":
                    party_val = token.text.split()[0].lower()
                elif len(token.text.split()) == 2:
                    party_val = token.text.split()[1].lower()
                else:
                    party_val = token.text.split()[0].lower()
                unique_propn_chunk.append(token.text)
                party_vals.append(party_val)

        for i, chunk in enumerate(unique_propn_chunk):
            party = Party(party_vals[i], self.remove_non_alphanumeric_characters_from_string(chunk))
            parties.append(party)

        return parties

    def get_nsubj_chunks_from_txt_no_hitl(self, txt):
        doc = self.nlp(txt)
        sentences = []

        for sent in doc.sents:
            sent_no_ws = re.sub('\n', '', sent.text)

            sentence_doc = self.nlp(sent_no_ws)

            new_sentences = []
            string = ""
            for token in sentence_doc:
                if token.dep_ == "nsubj" and string == "":
                    string += token.text + " "
                elif token.dep_ == "nsubj":
                    new_sentences.append(string)
                    string = token.text + " "
                elif token.is_sent_end:
                    string += token.text + " "
                    new_sentences.append(string)
                else:
                    string += token.text + " "

            for sentence in new_sentences:
                sentences.append([sentence, "type"])

            self.get_spacy_visualisation_from_sentences_object(sentences)

        return sentences

    def get_properly_split_text_into_roots_circumstances_and_untranslatable(self, txt):
        sentences = []
        sentences = self.get_nsubj_chunks_from_txt_no_hitl(txt)
        self.label_sentences(sentences)
        return sentences

    def get_spacy_visualisation_from_sentences_object(self, sentences):
        sentences_as_docs = []
        for sentence, type in sentences:
            sentences_as_docs.append(self.nlp(sentence))

        textfile = open("testing-materials/dependency.html", "w")
        options = {"compact": True, "color": "blue", "fine_grained": True}
        html = displacy.render(sentences_as_docs, style="dep", page=True, options=options)
        a = textfile.write(html)
        textfile.close()

    def label_sentences(self, sentences):
        clause_matcher = self.get_clause_matcher_2()
        circumstance_matcher = self.get_circumstance_matcher_1()
        for i, sentence in enumerate(sentences):
            doc = self.nlp(sentence[0])
            clause_matches = []
            circumstance_matches = []
            clause_matches = clause_matcher(doc)
            circumstance_matches = circumstance_matcher(doc)
            if len(clause_matches) != 0:
                if len(circumstance_matches) != 0:
                    sentences[i][1] = "clauseroot-circumstance"
                else:
                    sentences[i][1] = "clauseroot"
            elif len(circumstance_matches) != 0:
                sentences[i][1] = "circumstance"
            else:
                sentences[i][1] = "unknown type"

        return sentences

    # DEFUNCT METHOD MAYBE USE FOR ANALYSIS
    def get_sentences_from_txt_no_hitl(self, txt):
        doc = self.nlp(txt)
        sentences = []
        for sent in doc.sents:
            sent_no_ws = re.sub('\n', '', sent.text)
            sentences.append(sent_no_ws)
        return sentences

    def get_actions_from_txt_no_hitl(self, txt):
        doc = self.nlp(txt)
        actions = []
        unique_verb = []
        for token in doc:
            if token.pos_ == "VERB":
                if token.text[0].isalpha():
                    if token.text not in unique_verb:
                        unique_verb.append(token.text)

        for verb in unique_verb:
            action = Action(verb.split()[0].lower(), verb)
            actions.append(action)

        return actions

    """Method is defunct now - this was only POS matching"""

    def get_clause_matcher_1(self):
        matcher = Matcher(self.nlp.vocab)

        """Gets all clauses in geophys.confis.kts.meta """
        """Pattern to get cases where object is just a noun"""
        patterntwo = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"POS": "AUX", "OP": "*"},
                      {"POS": "PART", "OP": "*"},
                      {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "NOUN"}]
        matcher.add("clausetwo", [patterntwo], greedy='LONGEST')

        """Pattern to get cases where object is proper noun"""
        patternthree = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"POS": "AUX", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "PROPN"}]
        matcher.add("clausethree", [patternthree], greedy='LONGEST')

        """Pattern to get verb like "copy or adapt" for now only single "or" """
        patternfour = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"POS": "AUX", "OP": "*"},
                       {"POS": "PART", "OP": "*"},
                       {"POS": "VERB"}, {"POS": "CCONJ"}, {"POS": "VERB"}]
        matcher.add("clausefour", [patternfour], greedy='LONGEST')
        #
        # """Pattern to get complex 'parties' - a bit hacky because it only works at beggining of sentence """
        # patternfive = [{"IS_SENT_START":True}, {"IS_ALPHA": True, "OP":"*"}, {"POS": "AUX", "OP":"*"}, {"POS": "PART", "OP":"*"},
        #               {"POS": "VERB"}]
        # matcher.add("clausefive", [patternfive], greedy='LONGEST')

        return matcher

    def get_clause_matcher_2(self):
        matcher = Matcher(self.nlp.vocab)

        """Gets all clauses in geophys.confis.kts.meta """
        """Pattern to get cases where object is just a noun"""
        patterntwo = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"TAG": "MD", "OP": "*"},
                      {"POS": "PART", "OP": "*"},
                      {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "NOUN"}]
        matcher.add("clausetwo", [patterntwo], greedy='LONGEST')

        """Pattern to get cases where object is proper noun"""
        patternthree = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"TAG": "MD", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "PROPN"}]
        matcher.add("clausethree", [patternthree], greedy='LONGEST')

        """Pattern to get verb like "copy or adapt" for now only single "or" """
        patternfour = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"TAG": "MD", "OP": "*"},
                       {"POS": "PART", "OP": "*"},
                       {"POS": "VERB"}, {"POS": "CCONJ"}, {"POS": "VERB"}]
        matcher.add("clausefour", [patternfour], greedy='LONGEST')

        return matcher

    def get_circumstance_matcher_1(self):
        matcher = Matcher(self.nlp.vocab)

        """Pattern to get time instant"""
        patternone = [{"ENT_TYPE": "DATE", "OP": "*"}]
        matcher.add("time_instant_one", [patternone], greedy='LONGEST')

        """Pattern to get time instant"""
        patterntwo = [{"TEXT": {"REGEX": "^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$"}}]
        matcher.add("time_instant_two", [patterntwo], greedy='LONGEST')

        """Pattern to past actions"""
        patternthree = [{"POS": "DET", "OP": "?"}, {"POS": "PROPN"}, {"TAG": "VBD", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "PROPN"}]
        matcher.add("clausethree", [patternthree], greedy='LONGEST')

        return matcher

    def get_confis_clauses_from_txt_no_hitl(self, txt):
        clause_matcher_output = self.confis_meta["clause_matcher_output"]
        clause_objects = []
        for clause_and_dependents in clause_matcher_output:
            '''Populating most of the clause object constructor arguments'''
            argument_list = {"party_val": " ",
                             "modal_verb": " ",
                             "action_val": " ",
                             "object_thing_or_party_val": " ",
                             "string_id": clause_and_dependents[0][1],
                             "start": clause_and_dependents[0][2],
                             "end": clause_and_dependents[0][3],
                             "text": clause_and_dependents[0][0],
                             }

            '''Populating the conditions field iff there are conditions'''
            if len(clause_and_dependents) >= 2:
                argument_list["conditions"] = clause_and_dependents[1:]
            else:
                argument_list["conditions"] = []

            str = self.nlp(argument_list["text"])

            for token in str:
                if (token.pos_ == "PROPN" or token.pos_ == "NOUN"):
                    """TODO: This is mistakenly assuming that the first PROPN or NOUN will be the party"""
                    if argument_list["party_val"] == " ":
                        argument_list["party_val"] = token.text
                    else:
                        argument_list["object_thing_or_party_val"] = token.text
                elif token.pos_ == "AUX":
                    if token.nbor().pos_ == "PART":
                        particle = token.nbor().text
                        particle = particle[0].upper() + particle[1:len(particle)]
                        argument_list["modal_verb"] = token.text + particle
                    else:
                        argument_list["modal_verb"] = token.text
                elif token.pos_ == "VERB":
                    argument_list["action_val"] = token.text
                else:
                    pass

            clause_objects.append(Clause(**argument_list))
        return clause_objects

    def get_confis_clauses_well_defined(self, txt):
        """This function looks over what grammatically is a clause and then fiters out only clauses with defined
        PARTY, ACTION, and THING"""

    def get_things_from_txt_no_hitl(self, txt):
        doc = self.nlp(txt)
        things = []
        unique_propn_chunk = []
        thing_vals = []
        for token in doc.noun_chunks:
            # if token.text[0].isalpha():
            if token.text not in unique_propn_chunk:
                str = self.nlp(token.text)
                if str[0].pos_ == "NOUN" or str[0].pos_ == "PROPN":
                    thing_val = token.text.split()[0].lower()
                elif len(token.text.split()) == 2:
                    thing_val = token.text.split()[1].lower()
                else:
                    thing_val = token.text.split()[0].lower()
                unique_propn_chunk.append(token.text)
                thing_vals.append(thing_val)

        for i, chunk in enumerate(unique_propn_chunk):
            thing = Thing(thing_vals[i], self.remove_non_alphanumeric_characters_from_string(chunk))
            things.append(thing)

        return things

    """UTILS"""

    def remove_non_alphanumeric_characters_from_string(self, str):
        regexp = re.compile('[^a-zA-Z]')
        return regexp.sub(' ', str)

    # def get_matches_for_testing(self):
    #
    def print_sentences(self):

        for sentence in self.confis_meta["sentences"]:
            print(sentence)


class PartyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
