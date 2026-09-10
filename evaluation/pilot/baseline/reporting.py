"""Small, dependency-free reporting task used only by the evaluation pilot."""


def render_report(entries: list[dict[str, object]]) -> str:
    """Return one line per entry and a final total line.

    Each entry has ``name`` (a non-empty string) and ``amount`` (an integer).
    Names must be sorted alphabetically. The final line is ``TOTAL: <sum>``.
    Invalid entries raise ``ValueError``. Amounts may be negative.
    """
    # The predecessor created the public API and validation intent, but was
    # interrupted before implementing the function.
    raise NotImplementedError("report rendering is unfinished")
