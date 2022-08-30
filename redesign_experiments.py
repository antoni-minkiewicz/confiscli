from spacy import displacy
from spacy.matcher import DependencyMatcher

from contractprocessor import ContractProcessor
from script_for_experimentation_with_clauses import nlp
from textprocessor import TextProcessor


def print_sentences(sentences):
    for sentence in sentences:
        print("\"" + sentence + "\"")


def get_sentences_from_txt_file(filename, start_index=0, end_index=0):
    txt = ContractProcessor.get_txt_from_file(filename)

    textprocessor = TextProcessor()

    sentences = textprocessor.get_sentences_from_txt_no_hitl(txt)

    if end_index == 0:
        end_index = len(sentences)

    return sentences[start_index:end_index]


def generate_dependency_document_from_sentences(sentences):
    print("GENERATING DEPENDECIES \n\n\n\n\n")
    doc_sentences = []
    for sentence in sentences:
        doc_sentences.append(nlp(sentence))

    html = displacy.render(doc_sentences, style="dep", page=True)

    textfile = open("test_dependency.html", "w")
    a = textfile.write(html)
    textfile.close()

    print("FINISHED GENERATING DEPENDECIES \n\n\n\n\n")


def main():
    # sentences = get_sentences_from_txt_file("./testing-materials/simple.confis.kts.txt", 0, 10)
    sentences = ["Alice must pay Bob :   * from 01/06/2022 to 07/06/2022 inclusive "]
    dependency_pattern = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                          {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition", "RIGHT_ATTRS": {"DEP": "prep"}}]
    dependency_pattern2 = [{"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                          {"LEFT_ID": "verb", "REL_OP": '>', "RIGHT_ID": "preposition", "RIGHT_ATTRS": {"DEP": "prep"}},
                          {"LEFT_ID": "preposition", "REL_OP": '>', "RIGHT_ID": "preposition2", "RIGHT_ATTRS": {"DEP": "pobj"}}]
    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("verb-with-preposition", [dependency_pattern2])
    txt = nlp(sentences[0])
    matches = matcher(txt)

    for match_id, span_indexes in matches:
        span = txt[span_indexes[0]:span_indexes[1]+1]
        print(span.text)

    generate_dependency_document_from_sentences(sentences)
    print_sentences(sentences)


if __name__ == "__main__":
    main()
