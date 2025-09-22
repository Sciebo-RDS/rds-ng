import sys
import time


def enable_tracing() -> None:
    """
    Enables function call tracing.
    """
    depth = 0
    
    def tracefunc(frame, event, arg):
        nonlocal depth
        if not frame.f_code.co_name.startswith("__") and "lambda" not in frame.f_code.co_name and "component" in frame.f_code.co_filename:
            if event == "call":
                depth += 1
                print(
                    f">>> {' ' * depth}{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}: {frame.f_code.co_name} ({frame.f_code.co_filename}@{frame.f_code.co_firstlineno})",
                    file=sys.stderr,
                )
            elif event == "return":
                depth -= 1
            
        return tracefunc

    sys.setprofile(tracefunc)
