

import spacy

nlp = spacy.load("en_core_web_sm")
print(spacy.explain("pobj"))
print(spacy.explain("NNP"))
print(spacy.explain("CD"))
print(spacy.explain("VBD"))
print(nlp.get_pipe("tagger").labels)
for label in nlp.get_pipe("tagger").labels:
    print(label + " " + spacy.explain(label))

for label in nlp.get_pipe("parser").labels:
    if type(spacy.explain(label)) == type(None):
        print(label + " & " + "no explanation" + " \\\\")
    else:
        print(label + " & " + spacy.explain(label) + " \\\\")


print(spacy.explain("advmod"))