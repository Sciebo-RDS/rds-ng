import time
import typing


def attempt(
    callback: typing.Callable[..., typing.Any],
    *args,
    cb_retry: typing.Callable[..., None] | None = None,
    cb_fail: typing.Callable[[Exception], None] | None = None,
    attempts: int = 1,
    delay: float = 3.0,
    **kwargs,
) -> (bool, typing.Any):
    """
    Attempts to execute a callback function up to a certain number of times. If no attempt succeeds either the `fail_callback` is called or the
    exception is re-raised.

    Args:
        callback: The callback to attempt.
        cb_retry: An optional callback called on each retry.
        cb_fail: An optional callback in case of a failure.
        attempts: The number of attempts.
        delay: The delay (in seconds) between attempts.
        args: Arbitrary positional arguments, passed to the callback.
        kwargs: Arbitrary keyword arguments, passed to the callback.

    Returns:
        A tuple containing the success of the attempt and the return value of the callback.
    """
    for i in range(max(1, attempts)):
        try:
            result = callback(*args, **kwargs)
            return True, result
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if i < attempts - 1:
                time.sleep(delay)
                if callable(cb_retry):
                    cb_retry(*args, **kwargs)
            else:
                if callable(cb_fail):
                    cb_fail(exc)
                else:
                    raise exc

    return False, None
