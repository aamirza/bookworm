class Option:
    def __init__(self, name, documentation, function):
        self.name = name
        self.documentation = documentation
        self.function = function


class OptionList:
    def __init__(self):
        self.options = []

    def __str__(self):
        return self.indexed_list()

    @property
    def options_available(self):
        return len(self.options) > 0

    def add_option(self, option):
        self.options.append(option)

    def indexed_list(self):
        list = ""
        for index, option in enumerate(self.options):
            list += f"{index + 1}) {option.name}"
            list += '\n'
        return list
