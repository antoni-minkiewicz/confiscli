from abc import abstractmethod


class TextProcessorInterface():
    @abstractmethod
    def run_full_extraction(self, txt, contract_data_file, machine_readable_contract_file):
        pass