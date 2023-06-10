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
