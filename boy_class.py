#!/usr/bin/python3

class Boy:
    """A simple classes attributes demo"""

    # "general" is a public attribute, changes will reflect for
    # every instance with an uninitialised attribute general
    general = "Joseph"

    def __init__(self, name):
        """Initialise name"""
        self.set_name(name)

    def get_names(self):
        """Return private instance attribute and public attribute"""
        return self.name, self.general

    def set_name(self, value):
        """Set private instance attribute"""
        if type(value) is str:
            # name is now a private instance attribute
            self.name = value
        else:
            self.name = self.general


if __name__ == "__main__":

    boy1 = Boy("Samuel")  # name=Samuel, general=Joseph
    boy2 = Boy("James")  # name=James, general=Joseph
    boy3 = Boy("Mike")  # name=Mike, general=Joseph
    boy4 = Boy(None)    # name=Joseph, general=Joseph
    Boy.general = "Daniels"  # "general" for boy1-4 has been updated

    Boy("Mbizi")    # This does nothing to my knowledge
    print(f"Boy: {Boy.__dict__}")
    boy2.general = "Ken"  # boy2 now has it's own private "general"
    print(f"boy1: {boy1.get_names()}\n")

    Boy.general = "Baba"  # "general" for boy1, boy3, boy4 has been updated
    print(f"boy2: {boy2.get_names()}")
    print(f"boy3: {boy3.get_names()}")
    print(f"boy4: {boy4.get_names()}\n")

    Boy.nickname = "Mbizi"  # class "Boy" now has a public attribute "nickname"
    print(f"Boy.nickname: {Boy.nickname}")
    print(f"boy1: {boy1.get_names()}")
    print(f"boy1.nickname: {boy1.nickname}")
