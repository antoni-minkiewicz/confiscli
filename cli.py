import argparse
import os


class CLI:
    
    def __init__(self):
        self.args = None

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(description='Converts Pdf format contracts to Confis Formalism')
        parser.add_argument('source', metavar='source-file', help='the pdf file input for processing')

        parser.add_argument('--target', metavar='target-file',
                            help='the target confis file output')

        parser.add_argument('--guide', '-g', metavar='guide-file', help='the input JSON to guide the model')

        self.args = parser.parse_args(args)

        
if __name__ == "__main__":
    argument_parser = CLI()

    argument_parser.parse_arguments()