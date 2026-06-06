"""Pandora CLI entry point."""

import sys


def main():
    """Main entry point for python -m pandora."""
    from pandora.cli import app
    app()


if __name__ == "__main__":
    main()
