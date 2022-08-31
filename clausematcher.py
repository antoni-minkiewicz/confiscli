import re

import spacy
from spacy import displacy
from spacy.matcher import Matcher, DependencyMatcher

import utils
from utils import get_txt_from_file, find_and_replace_in_text_phrase_one_with_phrase_two


class ClauseMatcher:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except BaseException as e:
            print("You need to download \"en_core_web_sm\" ")
            raise e

    """IO Methods"""

    def get_matches(self, txt):
        doc = self.nlp(txt)
        matcher = self.get_clause_matcher_2()
        matches = matcher(doc)

        """Circumstance Matching"""
        matcher2 = self.get_circumstance_matcher_2()
        matches.extend(self.dependency_matches_to_normal_matches(matcher2(doc)))
        matcher3 = self.get_circumstance_matcher_1()
        matches.extend(matcher3(doc))

        return matches

    def get_matches_from_given_matcher(self, txt, matcher):
        doc = self.nlp(txt)
        matches = matcher(doc)
        return matches


    """Matcher Methods"""

    def get_spacy_visualisation_from_sentences_object(self, sentences):
        sentences_as_docs = []
        for sentence, type in sentences:
            sentences_as_docs.append(self.nlp(sentence))

        textfile = open("testing-materials/dependency.html", "w")
        options = {"compact": True, "color": "blue", "fine_grained": True}
        html = displacy.render(sentences_as_docs, style="dep", page=True, options=options)
        a = textfile.write(html)
        textfile.close()

    def get_spacy_visualisation_from_list_of_matches_object(self, list_of_matches):
        sentences_as_docs = []
        for sentence, type, start, end in list_of_matches:
            sentences_as_docs.append(self.nlp(sentence))

        textfile = open("testing-materials/dependency.html", "w")
        options = {"compact": True, "color": "blue", "fine_grained": True}
        html = displacy.render(sentences_as_docs, style="dep", page=True, options=options)
        a = textfile.write(html)
        textfile.close()

    def get_spacy_visualisation_from_txt(self, txt):
        textfile = open("testing-materials/dependency.html", "w")
        options = {"compact": True, "color": "blue", "fine_grained": True}
        html = displacy.render(self.nlp(txt), style="dep", page=True, options=options)
        a = textfile.write(html)
        textfile.close()

    def get_clause_matcher_2(self):
        matcher = Matcher(self.nlp.vocab)

        """Gets all clauses in geophys.confis.kts.meta """
        """Pattern to get cases where object is just a noun"""
        patterntwo = [{"POS": "DET", "OP": "?"},
                        {"POS": "PROPN"},
                        {"TAG": "MD", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"},
                        {"POS": "DET", "OP": "*"},
                        {"POS": "NOUN"}]
        matcher.add("clausetwo", [patterntwo], greedy='LONGEST')

        """Pattern to get cases where object is proper noun"""
        patternthree = [{"POS": "DET", "OP": "?"},
                        {"POS": "PROPN"},
                        {"TAG": "MD", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"},
                        {"POS": "DET", "OP": "*"},
                        {"POS": "PROPN"}]
        matcher.add("clausethree", [patternthree], greedy='LONGEST')

        """Pattern to get verb like "copy or adapt" for now only single "or" """
        patternfour = [{"POS": "DET", "OP": "?"},
                       {"POS": "PROPN"},
                       {"TAG": "MD", "OP": "*"},
                       {"POS": "PART", "OP": "*"},
                       {"POS": "VERB"},
                       {"POS": "CCONJ"},
                       {"POS": "VERB"}]
        matcher.add("clausefour", [patternfour], greedy='LONGEST')

        """Pattern to get cases where object is proper noun"""
        patternfive = [{"POS": "DET", "OP": "?"},
                        {"POS": "PROPN"},
                        {"TAG": "MD", "OP": "*"},
                        {"POS": "PART", "OP": "*"},
                        {"POS": "VERB"},
                        {"POS": "DET", "OP": "*"},
                        {"POS": "PROPN"}]
        matcher.add("clausefive", [patternfive], greedy='LONGEST')

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
        matcher.add("past_action", [patternthree], greedy='LONGEST')

        return matcher

    def get_circumstance_matcher_2(self):
        matcher = DependencyMatcher(self.nlp.vocab)

        dependency_pattern = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                              {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition",
                               "RIGHT_ATTRS": {"DEP": "prep"}}]
        dependency_pattern2 = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                               {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition",
                                "RIGHT_ATTRS": {"DEP": "prep"}},
                               {"LEFT_ID": "preposition", "REL_OP": '>', "RIGHT_ID": "pobj1",
                                "RIGHT_ATTRS": {"DEP": "pobj"}}]
        dependency_pattern3 = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                               {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition",
                                "RIGHT_ATTRS": {"DEP": "prep"}},
                               {"LEFT_ID": "preposition", "REL_OP": '>', "RIGHT_ID": "preposition2",
                                "RIGHT_ATTRS": {"DEP": "prep"}}]
        dependency_pattern4 = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                               {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition",
                                "RIGHT_ATTRS": {"DEP": "prep"}},
                               {"LEFT_ID": "preposition", "REL_OP": '>', "RIGHT_ID": "preposition2",
                                "RIGHT_ATTRS": {"DEP": "prep"}},
                               {"LEFT_ID": "preposition2", "REL_OP": '>', "RIGHT_ID": "pobj2",
                                "RIGHT_ATTRS": {"DEP": "pobj"}}]
        matcher.add("verb-with-preposition", [dependency_pattern])
        matcher.add("verb-with-preposition-and-pobj", [dependency_pattern2])
        matcher.add("verb-with-preposition-chain", [dependency_pattern3])
        matcher.add("verb-with-preposition-chain-and-pobj", [dependency_pattern4])
        return matcher

    def get_matcher_prepositional_phrases_attached_to_verb(self):

        matcher = DependencyMatcher(self.nlp.vocab)

        dependency_pattern = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                              {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition",
                               "RIGHT_ATTRS": {"DEP": "prep"}},
                              {"LEFT_ID": "preposition", "REL_OP": '>>', "RIGHT_ID": "any",
                               "RIGHT_ATTRS": {"IS_ALPHA": True}}
                              ]

        dependency_pattern2 = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                              {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "adverbialclausemodifier",
                               "RIGHT_ATTRS": {"DEP": "advcl"}},
                              {"LEFT_ID": "adverbialclausemodifier", "REL_OP": '>', "RIGHT_ID": "adverbialmodifier",
                               "RIGHT_ATTRS": {"DEP": "advmod"}},
                               {"LEFT_ID": "adverbialclausemodifier", "REL_OP": '>>', "RIGHT_ID": "any",
                                "RIGHT_ATTRS": {"IS_ALPHA": True}}
                              ]

        matcher.add("verb-with-preposition-chain", [dependency_pattern])

        matcher.add("verb-with-advcl-chain", [dependency_pattern2])


        return matcher

    def print_string_prepositional_phrases(self, matches, txt):
        doc = self.nlp(txt)
        for match_id, tokens in matches:
            string_id = self.nlp.vocab.strings[match_id]
            if string_id == "verb-with-preposition-chain":
                span_verb = doc[tokens[0]]
                span_prepositional_phrase = doc[tokens[1]:tokens[2]+1]
                print(span_verb.text + " " + span_prepositional_phrase.text, tokens, " --- " + string_id)
            elif string_id == "verb-with-advcl-chain":
                span_verb = doc[tokens[0]]
                span_prepositional_phrase = doc[tokens[2]:tokens[3]+1]
                print(span_verb.text + " " + span_prepositional_phrase.text, tokens, " --- " + string_id)

    def filted_syntactic_matches(self, matches):
        return matches

    def test_syntactic_matcher(self, txt, matcher):
        matches = self.get_matches_from_given_matcher(txt, matcher)
        matches_filtered = self.filted_syntactic_matches(matches)
        self.print_string_prepositional_phrases(matches_filtered, txt)

    def test_matcher_on_a_text(self, txt, matcher):
        matches = self.get_matches_from_given_matcher(txt, matcher)
        self.print_string_prepositional_phrases(matches, txt)

    """UTILS"""

    def remove_non_alphanumeric_characters_from_string(self, str):
        regexp = re.compile('[^a-zA-Z]')
        return regexp.sub(' ', str)

    def print_matches(self, matches, txt):
        doc = self.nlp(txt)
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(span.text, string_id)

    def matches_to_list(self, matches, txt):
        doc = self.nlp(txt)
        list = []
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            list.append((span.text, string_id, start, end))
        return list

    def sort_matches(self, matches):
        matches.sort(key=lambda y: y[1])
        return matches

    def matches_to_file(self, matches, txt, file_name):
        doc = self.nlp(txt)
        file = open(file_name, "w")
        matches = self.sort_matches(matches)

        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            file.write(''.join([str(start), " ", str(end), " ", span.text, " --- ", string_id]) + " --- \n")

        readout = self.get_readout_of_which_matches_overlap(matches)
        if len(readout) != 0:
            for comparison in readout:
                file.write(comparison)
        file.close()


    """This might becomre problematic all of a sudden"""
    def dependency_matches_to_normal_matches(self, dependency_matches):
        normal_matches = []
        for match_id, token_ids in dependency_matches:
            normal_matches.append((match_id, token_ids[0], token_ids[-1] + 1))
        return normal_matches

    def are_two_matches_overlapping(self, matches, index_1, index_2):
        if matches[index_1][1] <= matches[index_2][1]:
            if matches[index_1][2] > matches[index_2][1]:
                return True
        elif matches[index_1][1] <= matches[index_2][2]:
            if matches[index_1][2] <= matches[index_2][2]:
                return True
        else:
            return False

    def is_match_one_a_subset_of_two(self, matches, index_1, index_2):
        if matches[index_1][1] >= matches[index_2][1]:
            if matches[index_1][2] < matches[index_2][2]:
                return True
        else:
            return False

    def get_readout_of_which_matches_overlap(self, matches):
        readout = []
        for index, match in enumerate(matches):
            if self.are_two_matches_overlapping(matches, index, index - 1):
                readout.append("True")
            else:
                readout.append("False")
        return readout

    def get_matches_with_sub_matches_removed(self, matches):
        new_matches = []
        for index, match in enumerate(matches):
            for index_two, match_two in enumerate(matches):
                if self.is_match_one_a_subset_of_two(matches, index, index_two):
                    if index != index_two:
                        new_matches.append((0, 0, 0))
                        break
                elif index_two == len(matches) - 1:
                    new_matches.append(match)

        new_new_matches = []
        for index, match in enumerate(new_matches):
            if match == (0, 0, 0):
                continue
            else:
                new_new_matches.append(match)
        return new_new_matches

    def extraction_to_file_filtered(self, filename):
        txt = get_txt_from_file(filename)
        new_matches = self.get_matches(txt)
        new_matches = self.get_matches_with_sub_matches_removed(new_matches)
        self.matches_to_file(new_matches, txt, "testing-materials/matches.txt")

    def extraction_to_file_unfiltered(self, filename):
        txt = get_txt_from_file(filename)
        new_matches = self.get_matches(txt)
        self.matches_to_file(new_matches, txt, "testing-materials/matches_all.txt")

    def extraction_to_list_from_txt(self, txt):
        matches = self.get_matches(txt)
        matches = self.get_matches_with_sub_matches_removed(matches)
        matches = self.sort_matches(matches)
        return self.matches_to_list(matches, txt)

    def extraction_to_list_from_file(self, filename):
        txt = get_txt_from_file(filename)
        return self.extraction_to_list_from_txt(txt)

    def extraction_to_hierarchical_json_from_txt(self, txt):
        list_of_matches = self.extraction_to_list_from_txt(txt)
        json_of_matches = self.get_clauses_with_dependencies(list_of_matches)
        return json_of_matches

    def extraction_to_hierarchical_json_from_file(self, filename):
        list_of_matches = self.extraction_to_list_from_file(filename)
        json_of_matches = self.get_clauses_with_dependencies(list_of_matches)
        return json_of_matches

    def get_clauses_with_dependencies(self, list_of_matches):
        json_of_matches = []
        current_clause = 0
        for match in list_of_matches:
            if bool(re.search(r"clause", match[1])):
                json_of_matches.append([match])
                current_clause += 1
            elif current_clause > 0:
                json_of_matches[current_clause - 1].append(match)
        return json_of_matches

    def clauses_with_dependencies_to_file(self, json_of_matches):
        file = open('testing-materials/matches_dependencies', "w")
        for clause in json_of_matches:
            if len(clause) > 1:
                file.write(str(clause[0]) + "\n")
                for match in clause[1:]:
                    file.write("\t" + str(match) + "\n")
            else:
                file.write(str(clause[0]) + "\n")
        file.close()

if __name__ == "__main__":
    """For testing the pipeline"""
    clausematcher = ClauseMatcher()
    # filename = "testing-materials/geop-confiscli-outputs/geophys.confis.kts.txt"
    # clausematcher.extraction_to_file_filtered(filename)
    # clausematcher.extraction_to_file_unfiltered(filename)
    # matches = clausematcher.extraction_to_list_from_file(filename)
    # list_of_matches = utils.convert_list_of_list_of_tuples_to_list_of_lists(clausematcher.extraction_to_hierarchical_json_from_file(filename))
    # clausematcher.get_spacy_visualisation_from_list_of_matches_object(matches)
    # clausematcher.clauses_with_dependencies_to_file(list_of_matches)
    # for match in list_of_matches:
    #     print(match)


    """For Testing Individual Matchers"""
    txt1 = "the Buyer may not pay for the Goods to the Seller except under the following circumstances:"
    txt = "the Seller must deliver the Goods to the Buyer: • only after the Buyer did pay for the Goods to the Buyer • from 15/06/2022 to 25/06/2022 inclusive"
    clausematcher.get_spacy_visualisation_from_txt(txt)
    clausematcher.test_syntactic_matcher(txt, clausematcher.get_matcher_prepositional_phrases_attached_to_verb())
