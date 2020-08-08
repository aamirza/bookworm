import os


class Prompt():
    def __init__(self, options=None):
        if options is None:
            options = []
        self.options = options

    def get_options(self):
        if len(self.options) == 0:
            return "You have no options!"
        message = ""
        for i, option in enumerate(self.options):
            message += "\n[{}] {}".format(i + 1, option[0])
        message += "\n"
        return message

    def input_index(self, message, _list):
        print(message)
        index = input("Type any non-integer to quit >>> ")
        try:
            choice = int(index) - 1
            if choice not in range(0, len(_list)):
                raise ValueError
            else:
                return _list[choice]
        except ValueError:
            return "quit"

    def run_option(self, index):
        return self.options[index][1]

    def clear(self):
        os.system("clear")
