import sys
from typing import Any, Callable, TypeVar

__all__ = [
    "Annotated",
    "Any",
    "Callable",
    "get_args",
    "get_type_hints",
    "Literal",
    "ParamSpec",
    "TypeGuard",
    "TypeVar",
]

if sys.version_info < (3, 8):
    from typing_extensions import Literal, get_args
else:
    from typing import Literal, get_args

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_type_hints
else:
    from typing import Annotated, get_type_hints

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec, TypeGuard
else:
    from typing import ParamSpec, TypeGuard
