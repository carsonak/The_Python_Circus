#!/usr/bin/env python3

class A:

    soh = 10

    def __init__(self):
        self.lah = 20
        self.ti = 30
        self.__doh = 40

    @property
    def ti(self):
        return self._ti

    @ti.setter
    def ti(self, value):
        self._ti = value

    def update(self, *args):
        attributes = ["lah", "_ti", "_A__doh"]
        for i, v in enumerate(args):
            if i < len(attributes):
                self.__dict__[attributes[i]] = v
            else:
                break


if __name__ == "__main__":
    def main():
        a = A()
        print(A.__dict__, end="\n\n")
        print(a.__dict__)

    main()
