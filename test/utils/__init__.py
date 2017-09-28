"""Utils."""


class HiddenPrints:
    """Allows code to run in a closure without printing to stdout.

    Example:
        with HiddenPrints():
            print('This will not appear in stdout.')
    """

    def __enter__(self):
        import sys
        import os
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout = self._original_stdout
