#!/usr/bin/python3
"""Module for ast_remove_annotation."""

import ast


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover.

    Attributes:
        __vip_bases: set of special Typing classes to skip.
    """

    __vip_bases: set[str] = {"NamedTuple", "TypedDict"}
    __vip_decorators: set[str] = {"dataclass"}
    __vvip_decorators: set[str] = {
        "no_type_check", "no_type_check_decorator", "type_check_only"}

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
        for d in node.decorator_list:
            if (
                (isinstance(d, ast.Name) and
                 d.id in self.__vvip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vvip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vvip_decorators)
            ):
                return node

        node.returns = None
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:  # noqa: N802
        """Protect assign annotations in certain class defition scenarios.

        If node inherits from certain typing classes or has certain decorators
        annotations for its attributes will not be stripped or it may be
        skipped entirely.

        Args:
            node: a ClassDef node.

        Returns:
            The modified node.
        """
        for d in node.decorator_list:
            if (
                (isinstance(d, ast.Name) and
                 d.id in self.__vvip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vvip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vvip_decorators)
            ):
                return node

        node_backup: list[ast.AnnAssign] = []
        for b in node.bases:
            if (
                (isinstance(b, ast.Name) and
                 b.id in self.__vip_bases) or
                (isinstance(b, ast.Constant) and
                 b.value in self.__vip_bases) or
                (isinstance(b, ast.Attribute) and
                 b.attr in self.__vip_bases)
            ):
                for itm in node.body[:]:
                    if isinstance(itm, ast.AnnAssign):
                        node_backup.append(itm)
                        node.body.remove(itm)
                else:
                    break

        for d in node.decorator_list:
            if (
                (isinstance(d, ast.Name) and
                 d.id in self.__vip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vip_decorators)
            ):
                for itm in node.body[:]:
                    if isinstance(itm, ast.AnnAssign):
                        node_backup.append(itm)
                        node.body.remove(itm)
                else:
                    break

        node = self.generic_visit(node)  # type: ignore
        if node is not None:
            for itm in node_backup:
                node.body.insert(0, itm)

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
def f1(pos1: int, pos2, /, a: 'annotation', base, c: dict[str, tuple], d=1,
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
    code5: str = """import typing

@typing.simple.no_type_check
class Employee():
    name: str = "John"
    age = 54
    id
"""
    print(code5)
    tree = ast.parse(code5)
    print("BEFORE\n------\n", ast.dump(tree, indent=2), end="\n\n")
    new = TypeHintsRemover().visit(tree)
    print("AFTER\n-----\n", ast.dump(new, indent=2), end="\n\n")
    print(ast.unparse(new))
