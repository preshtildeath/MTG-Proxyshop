"""
CARD CREATOR TAB
"""
import os
import threading
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput
from proxyshop import core
cwd = os.getcwd()


"""
DISPLAY ELEMENTS
"""


class CreatorPanels(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            CreatorTabItem(CreatorNormalLayout, "normal", "Normal")
        )
        self.add_widget(CreatorTabItem(
            CreatorPlaneswalkerLayout, "planeswalker", "Planeswalker")
        )
        self.add_widget(
            CreatorTabItem(CreatorSagaLayout, "saga", "Saga")
        )
        self._tab_layout.padding = '0dp', '0dp', '0dp', '0dp'


class CreatorTabItem(TabbedPanelItem):
    def __init__(self, layout, c_type, name, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.add_widget(layout(c_type))


class CreatorLayout(GridLayout):
    def __init__(self, c_type, **kwargs):
        # Get our templates alphabetical
        self.selected_template = "Normal"
        temps_t = core.get_templates()[c_type]
        self.templates = ["Normal"]
        temps_t.pop("Normal")
        self.templates.extend(sorted(temps_t))
        del temps_t
        super().__init__(**kwargs)

    def select_template(self, spinner):
        self.selected_template = spinner.text
        print(self.selected_template)


class CreatorNormalLayout(CreatorLayout):
    def render(self, root):
        oracle_text = self.ids.oracle_text.text.replace("~", self.ids.name.text)
        flavor_text = self.ids.flavor_text.text.replace("~", self.ids.name.text)
        scryfall = {
            "layout": "normal",
            "set": self.ids.set.text,
            "name": self.ids.name.text,
            "oracle_text": oracle_text,
            "flavor_text": flavor_text,
            "power": self.ids.power.text,
            "artist": self.ids.artist.text,
            "mana_cost": self.ids.mana_cost.text,
            "type_line": self.ids.type_line.text,
            "toughness": self.ids.toughness.text,
            "rarity": self.ids.rarity.text.lower(),
            "card_count": self.ids.card_count.text,
            "keywords": self.ids.keywords.text.split(","),
            "collector_number": self.ids.collector_number.text,
            "color_identity": self.ids.color_identity.text.split()
        }
        temp = core.get_templates()["normal"][self.ids.template.text]
        self.ids.render_norm.disabled = True
        th = threading.Thread(target=root.render_custom, args=(temp, scryfall), daemon=True)
        th.start()
        th.join()
        self.ids.render_norm.disabled = False


class CreatorPlaneswalkerLayout(CreatorLayout):
    def render(self, root):
        rules_text = "\n".join([
            self.ids.line_1.text.replace("~", self.ids.name.text),
            self.ids.line_2.text.replace("~", self.ids.name.text),
            self.ids.line_3.text.replace("~", self.ids.name.text),
            self.ids.line_4.text.replace("~", self.ids.name.text)
        ])
        scryfall = {
            "layout": "normal",
            "set": self.ids.set.text,
            "name": self.ids.name.text,
            "artist": self.ids.artist.text,
            "loyalty": self.ids.loyalty.text,
            "mana_cost": self.ids.mana_cost.text,
            "type_line": self.ids.type_line.text,
            "rarity": self.ids.rarity.text.lower(),
            "card_count": self.ids.card_count.text,
            "oracle_text": rules_text,
            "flavor_text": "",
            "keywords": self.ids.keywords.text.split(","),
            "collector_number": self.ids.collector_number.text,
            "color_identity": self.ids.color_identity.text.split()
        }
        temp = core.get_templates()["planeswalker"][self.ids.template.text]
        self.ids.render_pw.disabled = True
        th = threading.Thread(target=root.render_custom, args=(temp, scryfall), daemon=True)
        th.start()
        th.join()
        self.ids.render_pw.disabled = True


class CreatorSagaLayout(CreatorLayout):
    def render(self, root):
        text_arr = []
        num_lines = "I"
        if self.ids.line_1.text != "":
            text_arr.append(f"{num_lines} — " + self.ids.line_1.text.replace("~", self.ids.name.text))
            num_lines+="I"
        if self.ids.line_2.text != "":
            text_arr.append(f"{num_lines} — " + self.ids.line_2.text.replace("~", self.ids.name.text))
            num_lines += "I"
        if self.ids.line_3.text != "":
            text_arr.append(f"{num_lines} — " + self.ids.line_3.text.replace("~", self.ids.name.text))
            if len(num_lines) == 3: num_lines = "IV"
            else: num_lines += "I"
        if self.ids.line_4.text != "":
            text_arr.append(f"{num_lines} — " + self.ids.line_4.text.replace("~", self.ids.name.text))
        text_arr.insert(0, f"Empty words.")
        rules_text = "\n".join(text_arr)
        print(rules_text)
        scryfall = {
            "layout": "saga",
            "flavor_text": "",
            "set": self.ids.set.text,
            "oracle_text": rules_text,
            "name": self.ids.name.text,
            "artist": self.ids.artist.text,
            "mana_cost": self.ids.mana_cost.text,
            "type_line": self.ids.type_line.text,
            "rarity": self.ids.rarity.text.lower(),
            "card_count": self.ids.card_count.text,
            "keywords": self.ids.keywords.text.split(","),
            "collector_number": self.ids.collector_number.text,
            "color_identity": self.ids.color_identity.text.split()
        }
        temp = core.get_templates()["saga"][self.ids.template.text]
        self.ids.render_saga.disabled = True
        th = threading.Thread(target=root.render_custom, args=(temp, scryfall), daemon=True)
        th.start()
        th.join()
        self.ids.render_saga.disabled = False


"""
CUSTOM FORM INPUTS
"""


class InputItem(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clicked = False
        self.original = self.text

    def _on_focus(self, instance, value, *largs):
        if not self.clicked:
            self.clicked = True
            self.original = self.text
        super()._on_focus(instance, value, *largs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """
        Enable tab to next or previous input
        """
        if keycode[1] == 'tab':  # deal with cycle
            if 'shift' in modifiers: nxt = self.get_focus_previous()
            else: nxt = self.get_focus_next()
            if nxt:
                self.focus = False
                nxt.focus = True
            return True
        if keycode[0] == 286:
            self.clicked = False
            self.text = self.original
        super().keyboard_on_key_down(window, keycode, text, modifiers)


class NoEnterInputItem(InputItem):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """
        Disable enter
        """
        if keycode[0] == 13:  # deal with cycle
            return False
        super().keyboard_on_key_down(window, keycode, text, modifiers)

class FourNumInput(InputItem):
    # Properties
    max_len = 4
    input_type = "number"

    def insert_text(self, substring, from_undo=False):
        """
        4 character max, numeric
        """
        if len(self.text) < self.max_len:
            if substring.isnumeric():
                return super().insert_text(substring, from_undo=from_undo)


class TwoNumInput(InputItem):
    # Properties
    max_len = 2
    input_type = "number"

    def insert_text(self, substring, from_undo=False):
        """
        2 character max, numeric
        """
        if len(self.text) < self.max_len:
            if substring.isnumeric():
                return super().insert_text(substring, from_undo=from_undo)


class FourCharInput(InputItem):
    # Properties
    max_len = 4

    def insert_text(self, substring, from_undo=False):
        """
        4 character max
        """
        if len(self.text) < self.max_len:
            return super().insert_text(substring.upper(), from_undo=from_undo)
