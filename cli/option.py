import collections


class NoOptionsAvailableError(Exception):
    pass


class Option:
    def __init__(self, name, documentation, function):
        self.name = name
        self.documentation = documentation
        self.function = function


class OptionList(collections.abc.Sequence):
    def __init__(self):
        self.options = []

    def __str__(self):
        return self.indexed_list()

    def __getitem__(self, item):
        if item > 0:
            return self.options[item - 1]
        else:
            raise IndexError

    def __len__(self):
        return len(self.options)

    def _check_if_options_available(self):
        if not self.options_available:
            raise NoOptionsAvailableError(
                "There are no options in OptionsList."
            )

    @property
    def options_available(self):
        return len(self) > 0

    def add_option(self, option):
        self.options.append(option)

    def indexed_list(self):
        self._check_if_options_available()

        list = ""
        for index, option in enumerate(self.options):
            list += f"[{index + 1}] {option.name}"
            list += '\n'
        return list
