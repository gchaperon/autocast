import typing as tp

from autocast import becomes, coerces


def test_noop() -> None:
    @coerces
    def fun(x: int) -> int:
        assert not isinstance(x, int)
        return x

    fun("5")
    fun(x=5.0)


def test_simple_coercion() -> None:
    @coerces
    def fun(x: becomes[int]) -> None:
        assert isinstance(x, int)

    fun("5")
    fun(x=5.0)


def test_called_with_options() -> None:
    @coerces("none")
    def fun1(x: becomes[int]) -> None:
        assert not isinstance(x, int)

    fun1("0")

    @coerces("some")
    def fun2(x: becomes[int], y: int) -> None:
        assert isinstance(x, int)
        assert not isinstance(y, int)

    fun2("0", "0")

    @coerces("all")
    def fun3(x: int, y: float) -> None:
        assert isinstance(x, int)
        assert isinstance(y, float)

    fun3("1", "1")


def test_doesnt_cast_with_other_annotated() -> None:
    @coerces
    def fun(x: tp.Annotated[int, "some other annotation"]) -> None:
        assert not isinstance(x, int)

    fun("0")


def test_handles_complex_signatures() -> None:
    @coerces
    def fun(
        po1: int,
        po2: becomes[int],
        /,
        pk1: int,
        pk2: becomes[int],
        *,
        ko1: int,
        ko2: becomes[int],
    ) -> None:
        assert not isinstance(po1, int)
        assert isinstance(po2, int)
        assert not isinstance(pk1, int)
        assert isinstance(pk2, int)
        assert not isinstance(ko1, int)
        assert isinstance(ko2, int)

    fun("1", "1", ko1="1", pk1="1", ko2="1", pk2="1")
    fun("1", "1", "1", ko2="1", ko1="1", pk2="1")


def test_handles_custom_type() -> None:
    class MyInt(int):
        pass

    @coerces
    def fun(x: becomes[MyInt]) -> None:
        assert isinstance(x, MyInt)

    fun("123")


def test_handles_forward_ref() -> None:
    @coerces
    def fun(x: becomes["MyInt"]) -> None:
        assert isinstance(x, MyInt)
        pass

    class MyInt(int):
        pass

    fun("123")
