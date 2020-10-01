MAX_CHARS_PER_LINE = 50


def full_line(char="#", chars_per_line=MAX_CHARS_PER_LINE):
    return char * chars_per_line


def padded_message(message, pad_char="#", padding_size=3,
                   chars_per_line=MAX_CHARS_PER_LINE):
    num_chars_remaining = chars_per_line - len(message)
    num_chars_on_left = num_chars_on_right = int(num_chars_remaining / 2)
    num_chars_remaining_is_odd = num_chars_remaining % 2 != 0
    if num_chars_remaining_is_odd:
        num_chars_on_right += 1

    pad = pad_char * padding_size
    left_space = " " * (num_chars_on_left - padding_size)
    right_space = " " * (num_chars_on_right - padding_size)
    return f"{pad}{left_space}{message}{right_space}{pad}"


def title_message(message, pad_char="#", padding_size=3,
                  chars_per_line=MAX_CHARS_PER_LINE):
    first_line = third_line = full_line(pad_char, chars_per_line)
    second_line = padded_message(message,
                                 pad_char=pad_char,
                                 padding_size=padding_size,
                                 chars_per_line=chars_per_line)
    return f"{first_line}\n{second_line}\n{third_line}"


def welcome_message(chars_per_line=MAX_CHARS_PER_LINE):
    return title_message("WELCOME TO BOOKWORM", chars_per_line=chars_per_line)
