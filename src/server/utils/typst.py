import subprocess
import sys
import tempfile


def typst_compile(source: str) -> bytes:
    """
    Compiles a Typst file into a PDF.

    Args:
        source: The Typst source.

    Returns:
        The compiled PDF data.
    """
    input_file = tempfile.NamedTemporaryFile(suffix=".typ")
    output_file = tempfile.NamedTemporaryFile(suffix=".pdf")

    input_file.write(source.encode())
    input_file.seek(0)

    subprocess.check_call(
        ["typst", "compile", input_file.name, output_file.name],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    output_file.seek(0)
    return output_file.read()
