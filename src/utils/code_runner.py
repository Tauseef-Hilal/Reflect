from io import StringIO
import sys


def run_code(code: str) -> str:
    """Run a code snippet

    Args:
        code (str): Code to run

    Returns:
        str: Output
    """

    # Set output stream
    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout

    # Execute the codeblock
    exec(code)

    # Get output from the new_stdout
    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output
