import unittest
import cli.banner as new_prompt


class PromptMessageTest(unittest.TestCase):

    def test_fullLine(self):
        self.assertEqual(new_prompt.full_line("*", chars_per_line=50),
                         "*" * 50)
        self.assertEqual(new_prompt.full_line("-", chars_per_line=55),
                         '-' * 55)

    def test_padded_message(self):
        message = "#" * 3 + " " * 21 + "HI" + " " * 21 + "#" * 3
        self.assertEqual(new_prompt.padded_message("HI"), message)

    def test_padded_odd_message(self):
        message = "#" * 3 + " " * 20 + "HEY" + " " * 21 + "#" * 3
        self.assertEqual(new_prompt.padded_message("HEY"), message)

    def test_custom_paddeed_message(self):
        message = "--- WOW ---"
        self.assertEqual(
            new_prompt.padded_message("WOW", pad_char="-", chars_per_line=11),
            message
        )

    def test_welcomeMessage(self):
        test_string = ""
        line1 = "#" * 50 + "\n"
        line2 = "#" * 3
        line2 += " " * 12
        line2 += "WELCOME TO BOOKWORM"
        line2 += " " * 13
        line2 += "#" * 3 + "\n"
        line3 = "#" * 50
        test_string = line1 + line2 + line3
        self.assertEqual(new_prompt.title_message("WELCOME TO BOOKWORM"),
                         test_string)


if __name__ == '__main__':
    unittest.main()