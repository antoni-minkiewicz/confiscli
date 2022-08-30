import os
import sys

from cli import CLI
from ocr_to_text import OcrToText
from textprocessor import TextProcessor
from textprocessorinterface import TextProcessorInterface
from utils import get_txt_from_file


class ContractProcessor:
    def __init__(self, text_processor, source_file='', target=''):
        if not isinstance(text_processor, TextProcessorInterface):
            raise ValueError('Text_processor parameter is not instance of TextProcessorInterface')
        self.dir_path = os.path.dirname(source_file)
        self.source_file = source_file
        self.source_filename, self.source_extension = os.path.splitext(os.path.basename(self.source_file))
        self.dir_output_name = self.source_filename[:4] + "-confiscli-outputs/"
        self.dir_output = os.path.join(self.dir_path, self.dir_output_name)
        os.makedirs(self.dir_output, exist_ok = True)
        self.txt_of_source_file = os.path.join(self.dir_output,  self.source_filename + ".txt")
        self.confis_meta_file = os.path.join(self.dir_output , self.source_filename + ".meta")
        self.confis_file = os.path.join(self.dir_output , self.source_filename)
        self._pdf_to_confis(text_processor)

    def _pdf_to_confis(self, textprocessor):
        txt = ""
        if self.source_extension == ".pdf":
            print("Extracting from pdf source-file: " + self.source_file)
            self.txt_of_source_file = self.extract_text_from_pdf(self.source_file, self.txt_of_source_file)
        elif self.source_extension == ".txt":
            print("Extracting from txt source-file:" + self.source_file)
            self.txt_of_source_file = self.source_file

        txt = get_txt_from_file(self.txt_of_source_file)
        textprocessor.run_full_extraction(txt, self.confis_meta_file, self.confis_file)

    """This method gets txt from pdf at source file and creates txt version at destination file"""
    def extract_text_from_pdf(self, source_file, txt_of_source_file):
        ocr_to_text_converter = OcrToText()
        return ocr_to_text_converter.conversion(source_file, txt_of_source_file)

    @staticmethod
    def main():
        argument_parser = CLI()
        argument_parser.parse_arguments(sys.argv[1:])

        if argument_parser.args.guide is None:
            contract = ContractProcessor(TextProcessor(), argument_parser.args.source, argument_parser.args.target)
        if argument_parser.args.guide:
            print(argument_parser.args.guide)

if __name__ == "__main__":
    ContractProcessor.main()
