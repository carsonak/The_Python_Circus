#!/usr/bin/python3
"""Module for type_hints_remover."""

import ast


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # remove the return type defintion
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        return node

    def visit_Import(self, node: ast.Import) -> ast.Import | None:
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom | None:
        return node if node.module != 'typing' else None
