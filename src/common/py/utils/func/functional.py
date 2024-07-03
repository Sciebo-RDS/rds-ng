import time
import typing


def attempt(
    callback: typing.Callable[[...], None],
    *args,
    retry_callback: typing.Callable[[], None] | None = None,
    fail_callback: typing.Callable[[Exception], None] | None = None,
    attempts: int = 1,
    delay: float = 3.0,
    **kwargs,
) -> bool:
    """
    Attempts to execute a callback function up to a certain number of times. If no attempt succeeds either the `fail_callback` is called or the
    exception is re-raised.

    Args:
        callback: The callback to attempt.
        retry_callback: An optional callback called on each retry.
        fail_callback: An optional callback in case of a failure.
        attempts: The number of attempts.
        delay: The delay (in seconds) between attempts.
        args: Arbitrary positional arguments, passed to the callback.
        kwargs: Arbitrary keyword arguments, passed to the callback.

    Returns:
        Whether the attempt has succeeded.
    """
    for i in range(max(1, attempts)):
        try:
            callback(*args, **kwargs)
            return True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if i < attempts - 1:
                time.sleep(delay)
                if callable(retry_callback):
                    retry_callback()
            else:
                if callable(fail_callback):
                    fail_callback(exc)
                else:
                    raise exc

    return False
