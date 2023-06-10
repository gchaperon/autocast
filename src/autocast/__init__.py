# SPDX-FileCopyrightText: 2023-present Gabriel Chaperon <gabrielchaperonb@gmail.com>
#
# SPDX-License-Identifier: MIT
import functools
from typing import overload

from autocast import _typing as tp

__all__ = ["coerces", "becomes"]

sentinel = object()
T = tp.TypeVar("T")
P = tp.ParamSpec("P")

becomes = tp.Annotated[T, sentinel]

annotated_type_names = {"AnnotatedMeta", "_AnnotatedAlias"}
_CoercionOptT = tp.Literal["all", "some", "none"]


def should_convert(hint: tp.Any) -> bool:
    return type(hint).__name__ in annotated_type_names and sentinel in hint.__metadata__


@overload
def coerces(
    option: _CoercionOptT, /
) -> tp.Callable[[tp.Callable[P, T]], tp.Callable[P, T]]:
    ...


@overload
def coerces(fun: tp.Callable[P, T], /) -> tp.Callable[P, T]:
    ...


def coerces(
    option: _CoercionOptT | tp.Callable[P, T] = "some", /
) -> tp.Callable[[tp.Callable[P, T]], tp.Callable[P, T]] | tp.Callable[P, T]:
    if callable(option):
        fun = option
        return _coerces_wrapper("some", fun)

    return functools.partial(_coerces_wrapper, option)  # type: ignore[arg-type]


def _coerces_wrapper(
    option: _CoercionOptT, fun: tp.Callable[P, T]
) -> tp.Callable[P, T]:
    type_hints = tp.get_type_hints(fun, include_extras=True)

    @functools.wraps(fun)
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        updated_args: P.args = []
        updated_kwargs: P.kwargs = {}
        if option == "none":
            updated_args += args
            updated_kwargs.update(kwargs)
        elif option == "all":
            updated_args += [hint(arg) for arg, hint in zip(args, type_hints.values())]
            updated_kwargs.update({k: type_hints[k](arg) for k, arg in kwargs.items()})
        else:
            updated_args += [
                hint.__origin__(arg) if should_convert(hint) else arg
                for arg, hint in zip(args, type_hints.values())
            ]
            updated_kwargs.update(
                {
                    k: type_hints[k].__origin__(arg)
                    if should_convert(type_hints[k])
                    else arg
                    for k, arg in kwargs.items()
                }
            )

        return fun(*updated_args, **updated_kwargs)

    return inner
