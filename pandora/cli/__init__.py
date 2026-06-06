"""Pandora CLI - Command line interface."""

import typer

app = typer.Typer(
    name="pandora",
    help="Pandora — Autonomous AI Red Team Framework",
)


@app.command()
def onboard():
    """Run the onboarding wizard to configure Pandora."""
    import os
    from pathlib import Path

    config_dir = Path.home() / ".pandora"
    config_dir.mkdir(exist_ok=True)

    env_file = config_dir / ".env"
    project_env = Path(__file__).parent.parent.parent / ".env"

    if env_file.exists():
        typer.echo(f"Configuration already exists at {env_file}")
        if not typer.confirm("Overwrite?"):
            return

    if project_env.exists():
        typer.echo(f"Copying .env from {project_env}")
        import shutil
        shutil.copy(project_env, env_file)
    else:
        typer.echo("No .env found. Creating default configuration...")
        default_env = """# Pandora Configuration
ANTHROPIC_API_KEY=your-anthropic-key-here
OPENAI_API_KEY=your-openai-key-here
"""
        env_file.write_text(default_env)

    typer.echo(f"\nConfiguration saved to {env_file}")
    typer.echo("Edit it with your API keys, then run: pandora")


@app.command()
def version():
    """Show Pandora version."""
    from pandora import __version__
    typer.echo(f"Pandora v{__version__}")


if __name__ == "__main__":
    app()
