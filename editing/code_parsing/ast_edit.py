#!/usr/bin/python3
"""Module for ast_remove_annotation."""

import ast


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover.

    Attributes:
        __vips: set of special Typing classes to skip.
    """

    __vips: set[str] = set({"NamedTuple", "TypedDict"})

    def visit_arg(self, node: ast.arg) -> ast.AST:  # noqa: N802
        """Remove function parameter annotations.

        Args:
            node: an arg node

        Returns:
            The modified node.
        """
        node.annotation = None
        return self.generic_visit(node)

    def visit_FunctionDef(self,  # noqa: N802
                          node: ast.FunctionDef) -> ast.AST:
        """Remove returns type annotation.

        Args:
            node: a FunctionDef node.

        Returns:
            The modified node
        """
        node.returns = None
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:  # noqa: N802
        """Protect assign annotations in certain class defitions.

        If node inherits from certain typing classes, annotaitons for its
        attributes will not be stripped.

        Args:
            node: a ClassDef node.

        Returns:
            The modified node.
        """
        node_backup: list[tuple[int, ast.AnnAssign]] = []
        for b in node.bases:
            if ((isinstance(b, ast.Name) and b.id in self.__vips) or
                (isinstance(b, ast.Constant) and b.value in self.__vips) or
                    (isinstance(b, ast.Attribute) and b.attr in self.__vips)):
                for pos, itm in enumerate(node.body[:]):
                    if isinstance(itm, ast.AnnAssign):
                        node_backup.append((pos, itm))
                        del node.body[pos]
                else:
                    break

        node = self.generic_visit(node)  # type: ignore
        if isinstance(node, ast.ClassDef):
            for pos, itm in node_backup:
                node.body.insert(pos, itm)

        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:  # noqa: N802
        """Remove type annotations from assign statements.

        Args:
            node: a AnnAssign node.

        Returns:
            The modified node.
        """
        assign_kwargs: dict[str, list[ast.AST] | ast.AST] = {}
        for k, v in node.__dict__.items():
            if k == "annotation":
                continue
            elif k == "target":
                assign_kwargs["targets"] = [v]
            else:
                assign_kwargs[k] = v

        return self.generic_visit(ast.Assign(**assign_kwargs))


if __name__ == "__main__":
    code1: str = """@decorator1
@decorator2
def f1(pos1: int, pos2, /, a: 'annotation', b, c: dict[str, tuple], d=1,
      *args: int, key1, key2: bool, key3='default', **kwargs
      ) -> Iterator[float]:
   yield 1.0
   yield 2.6
   yield 5.8
"""
    code2: str = """from typing import NamedTuple

class Employee(NamedTuple):
    \"\"\"Represents an employee.\"\"\"
    name: str
    id: int = 3
    age

    def __repr__(self) -> str:
            return f'<Employee {self.name}, id={self.id}>'
"""
    code3: str = """from collections import namedtuple

class Employee(NamedTuple):
    name: str = "John"
    id: int


Employee2 = collections.namedtuple('Employee2', ['name', 'id'])
"""
    code4: str = "class Insane('Crazy', Woah, typing.namedtuple, *bases, metaclass=Meta, huh='wild', eight=8, **kwargs):..."
    code5: str = """class Employee():
    name: str = "John"
"""
    print(code4)
    tree = ast.parse(code4)
    print("BEFORE\n------\n", ast.dump(tree, indent=2), end="\n\n")
    new = TypeHintsRemover().visit(tree)
    print("AFTER\n-----\n", ast.dump(new, indent=2), end="\n\n")
    print(ast.unparse(new))
