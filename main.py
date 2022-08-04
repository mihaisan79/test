__version__ = "Alpha 1.0.0"

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from morse_trans import *


class MainGUI(GridLayout):
    text_output_str = StringProperty("")
    reverse_conv = False  # Control the translating mode

    def main_func(self, text):
        encode_keys = MORSE_ENCODE.keys()
        decode_keys = MORSE_DECODE.keys()
        invalid_input = []  # Store invalid input(s)

        try:
            if not self.reverse_conv:  # eng -> morse
                self.text_output_str = encode(text)
            else:  # morse -> eng
                self.text_output_str = decode(text)

        except KeyError:
            print("ERROR")
            if not self.reverse_conv:
                for i in text:
                    if i.upper() not in encode_keys:
                        invalid_input.append(i)  # Scan and find invalid input(s) to display later

            else:
                text = text.replace("\n", " \n ")  # If not, this
                for i in text.split(" "):
                    if i not in decode_keys:
                        invalid_input.append(i)

            for j in invalid_input:
                if j not in text:
                    invalid_input.remove(j)  # Check and remove element(s) in invalid_input that isn't/aren't in text

            # This part is to display output accurately when 'enter' in mode morse -> eng
            # since 'enter' in this mode will always cause an exception (exp: '.--.\n', not in decode_keys)
            # which always result in an error warning
            # With how the input text is split, the invalid_input sometimes has no element
            # resulting in some error messages with no invalid value indicated
            if len(invalid_input) > 0:
                self.text_output_str = f"*Invalid input(s): {' ,'.join(invalid_input)}*"
            else:  # Display decoded input with 'enter' and no invalid value
                self.text_output_str = decode(text)

    def toggle_button(self, widget):  # Controlling translating mode
        if widget.state == "normal":
            widget.text = "Text to Morse code"
            self.reverse_conv = False
        else:
            widget.text = "Morse code to text"
            self.reverse_conv = True

    def delete_all(self):  # Reset all to the initial state
        self.ids.tp1.text = ""
        self.text_output_str = ""

# Skip this
"""
class RoundedButton(Button):
    changed_color = ListProperty([48 / 225, 84 / 225, 150 / 225, 1])

    def change_color(self):
        self.changed_color = [1, 1, 0, 1]

    def init_color(self):
        self.changed_color = [48 / 225, 84 / 225, 150 / 225, 1]
"""


class MorseApp(App):
    def build(self):
        Window.color = (78, 71, 74, .8)  # (240/255, 240/255, 240/255, 240/255)
        return MainGUI()


if __name__ == "__main__":
    MorseApp().run()
