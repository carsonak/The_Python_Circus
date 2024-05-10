#!/usr/bin/python3
"""Module for ast_remove_annotation."""

import ast


class TypeHintsRemover(ast.NodeTransformer):
    """Type Annotation Remover."""

    def visit_arg(self, node: ast.arg) -> ast.AST:
        """Remove function arguments annotations."""
        node.annotation = None
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        """Remove function return type annotations."""
        node.returns = None
        return self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:
        """Remove type annotations from assign statements."""
        assign_kwargs: dict[str, list[ast.AST] | ast.AST] = {}
        for k, v in node.__dict__.items():
            if k == "annotation":
                continue
            elif k == "target":
                assign_kwargs["targets"] = [v]
            else:
                assign_kwargs[k] = v

        return self.generic_visit(ast.Assign(**assign_kwargs))

    def visit_Import(self, node: ast.Import) -> ast.AST | None:
        """Remove typing module imports from `import` statements."""
        node.names = [module for module in node.names
                      if not module.name.startswith("typing")]
        return self.generic_visit(node) if node.names else None

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST | None:
        """Remove typing module imports from `from ... import` statements."""
        module_name: str | None = node.module
        if module_name and module_name.startswith("typing"):
            return None
        else:
            return self.generic_visit(node)


if __name__ == "__main__":
    code: str = """@decorator1
@decorator2
def f1(pos1: int, pos2, /, a: 'annotation', b, c: dict[str, tuple], d=1,
      *args: int, key1, key2: bool, key3='default', **kwargs
      ) -> Iterator[float]:
   yield 1.0
   yield 2.6
   yield 5.8
"""
    print(code)
    tree = ast.parse(code)
    print("BEFORE\n------\n", ast.dump(tree, indent=2), end="\n\n")
    new = TypeHintsRemover().visit(tree)
    print("AFTER\n-----\n", ast.dump(new, indent=2), end="\n\n")
    print(ast.unparse(new))
