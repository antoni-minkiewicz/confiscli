# confiscli
## About
This is a tool that uses rule-based NLP to aid in the translation of natrual language contracts to <a href="https://github.com/Cottand/Confis">Confis</a> contracts.
## Usage
### Installation
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_trf
```

### Translation
```
pyton contractprocessor.py source-file target-file
```
This will attempt to translate source-file (permissible formats: text and PDF) and outputs it to target-file into valid Confis code. If target-file is not given it creates a subdirectory in the same directory as the source-file where the outputs of the contractprocessor go.
