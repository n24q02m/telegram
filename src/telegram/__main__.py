"""telegram entry point (``python -m telegram``)."""

from telegram.cli import main as _cli_main


def _cli() -> int:
    """Dispatch argv through the hull consumer CLI builder.

    Bare invocation and any leading-dash argv (e.g. --http) start the
    server; a leading positional argv[0] routes to a subcommand instead.
    """
    return _cli_main()


if __name__ == "__main__":
    raise SystemExit(_cli())
