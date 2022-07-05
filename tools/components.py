import hikari
from miru.ext import nav


class Back(nav.PrevButton):
    def __init__(self):
        super().__init__(style=hikari.ButtonStyle.SECONDARY, label="⟵", emoji=None)


class Forward(nav.NextButton):
    def __init__(self):
        super().__init__(style=hikari.ButtonStyle.SECONDARY, label="⟶", emoji=None)
