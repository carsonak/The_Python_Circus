#!/usr/bin/python3
"""Module for ast_remove_annotation."""

import ast


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover."""

    def visit_FunctionDef(self, node):
        # remove the return type definition
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        if node.value is None:
            return None
        return ast.Assign([node.target], node.value)

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != 'typing' else None
