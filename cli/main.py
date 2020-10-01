from cli import banner, option

NEWLINE = "\n"


def build_option_list():
    option_list = option.OptionList()
    options = [
        option.Option("Add book", "Add a new book to your reading list", None),
        option.Option("Update book", "Update your reading progress", None),
        option.Option("New goal", "Start a new book reading goal", None),
    ]
    for opt in options:
        option_list.add_option(opt)
    return option_list


def main():
    print(banner.welcome_message())
    print(NEWLINE)
    option_list = build_option_list()
    print(option_list)


if __name__ == "__main__":
    main()
