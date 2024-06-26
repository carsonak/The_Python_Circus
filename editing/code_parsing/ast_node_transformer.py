#!/usr/bin/python3
"""Module for ast_remove_annotation."""

import ast
from typing import Union


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover.

    Attributes:
        __vip_bases: set of special Typing classes to skip.
        __vip_decorators: set of special decorators to skip.
    """

    __vip_bases: set[str] = {"NamedTuple", "TypedDict"}
    __vip_decorators: set[str] = {
        "no_type_check", "no_type_check_decorator",
        "type_check_only", "dataclass",
    }

    def save_unassigned_var_annotation(
        self, node: Union[
            ast.Module | ast.AsyncFunctionDef | ast.FunctionDef |
            ast.AsyncWith | ast.Interactive | ast.ClassDef | ast.For |
            ast.AsyncFor | ast.If | ast.While | ast.With | ast.ExceptHandler |
            ast.Try | ast.match_case
        ]
    ) -> ast.AST:
        """Remove unassigned type annotations from nodes with body nodes.

        Args:
            node: a node with a body node.

        Returns:
            The modified node with it's original unassigned variable
            annotations.
        """
        ann_backup: list[tuple[int, ast.AnnAssign]] = []
        for pos, item in enumerate(node.body[:]):
            if isinstance(item, ast.AnnAssign) and item.value is None:
                ann_backup.append((pos, item))
                node.body.remove(item)

        self.generic_visit(node)
        for pos, item in ann_backup:
            node.body.insert(pos, item)

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:  # noqa: N802,B906
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
                 d.id in self.__vip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vip_decorators)
            ):
                return node

        for b in node.bases:
            if (
                (isinstance(b, ast.Name) and
                 b.id in self.__vip_bases) or
                (isinstance(b, ast.Constant) and
                 b.value in self.__vip_bases) or
                (isinstance(b, ast.Attribute) and
                 b.attr in self.__vip_bases)
            ):
                return node

        return self.save_unassigned_var_annotation(node)

    def visit_FunctionDef(self,  # noqa: N802,B906
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
                 d.id in self.__vip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vip_decorators)
            ):
                return node

        node.returns = None
        return self.save_unassigned_var_annotation(node)

    def visit_AsyncFunctionDef(  # noqa: N802,B906
            self, node: ast.AsyncFunctionDef) -> ast.AST:
        """Protect unassigned type annotations.

        Args:
            node: an AsyncFunctionDef node.

        Returns:
            The modified node.
        """
        for d in node.decorator_list:
            if (
                (isinstance(d, ast.Name) and
                 d.id in self.__vip_decorators) or
                (isinstance(d, ast.Constant) and
                 d.value in self.__vip_decorators) or
                (isinstance(d, ast.Attribute) and
                 d.attr in self.__vip_decorators)
            ):
                return node

        node.returns = None
        return self.save_unassigned_var_annotation(node)

    def visit_AnnAssign(self, node: ast.AnnAssign,  # noqa: N802
                        ) -> ast.AST:
        """Remove type annotations from assign statements.

        Args:
            node: an AnnAssign node.

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

    def visit_arg(self, node: ast.arg) -> ast.AST:
        """Remove function parameter annotations.

        Args:
            node: an arg node

        Returns:
            The modified node.
        """
        node.annotation = None
        return self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: an AsyncFor node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_AsyncWith(self, node: ast.AsyncWith,  # noqa: N802,B906
                        ) -> ast.AST:
        """Protect unassigned type annotations.

        Args:
            node: an AsyncWith node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_ExceptHandler(  # noqa: N802,B906
            self, node: ast.ExceptHandler) -> ast.AST:
        """Protect unassigned type annotations.

        Args:
            node: an EsceptHandler node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_For(self, node: ast.For) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: a For node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_If(self, node: ast.If) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: an If node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_Interactive(  # noqa: N802,B906
            self, node: ast.Interactive) -> ast.AST:
        """Protect unassigned type annotations.

        Args:
            node: an Interactive node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_match_case(self, node: ast.match_case) -> ast.AST:  # noqa: B906
        """Protect unassigned type annotations.

        Args:
            node: a match_case node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_Module(self, node: ast.Module) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: a Module node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_Try(self, node: ast.Try) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: a Try node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_While(self, node: ast.While) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: a While node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)

    def visit_With(self, node: ast.With) -> ast.AST:  # noqa: N802,B906
        """Protect unassigned type annotations.

        Args:
            node: a With node.

        Returns:
            The modified node.
        """
        return self.save_unassigned_var_annotation(node)


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
