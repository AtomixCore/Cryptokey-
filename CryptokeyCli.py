import click
from pathlib import Path
import tomli
import sys

from src.cryptokey import Cryptokey

def validate_input_extension(ctx, param, value):
    path = Path(value)
    if not path.suffix == ".esc" or not path.name.endswith(".ac.esc"):
        raise click.BadParameter("Input file must have a `.ac.esc` extension and contain valid TOML.")
    return value


def validate_output_extension(ctx, param, value):
    path = Path(value)
    if not path.suffix == ".es" or not path.name.endswith(".ac.es"):
        raise click.BadParameter("Output file must have a `.ac.es` extension.")
    return value


@click.command()
@click.option(
    "-x", "--input",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    required=True,
    callback=validate_input_extension,
    help="Path to the input TOML config file (.ac.esc). Must contain valid TOML content."
)
@click.option(
    "-o", "--output",
    type=click.Path(writable=True),
    required=True,
    callback=validate_output_extension,
    help="Path to the encrypted output file (.ac.es)."
)
@click.option(
    "-p", "--password",
    type=str,
    required=False,
    help="Password used to encrypt the file."
)
@click.option(
    "--gen-pass", is_flag=True,
    help="Generate a strong random password instead of providing one manually."
)
def cli(input, output, password, gen_pass):
    """
    Encrypt a TOML configuration file (.ac.esc) into a secure binary format (.ac.es).

    The input file must end with `.ac.esc` and contain valid TOML code.
    """
    # Step 1: Read and validate TOML content
    try:
        with open(input, "r", encoding="utf-8") as f:
            toml_code = f.read()
            tomli.loads(toml_code)  # Validation only
    except (OSError, tomli.TOMLDecodeError) as e:
        click.secho("Error: Failed to read or parse the input file. Make sure it contains valid TOML.", fg="red")
        click.echo(f"Details: {str(e)}")
        sys.exit(1)

    # Step 2: Handle password generation
    if gen_pass:
        tmp = Cryptokey(password="", toml_code="", file_name="")
        password = tmp.generate_password()
        click.secho("Generated Password:", fg="green")
        click.echo(password)

    if not password:
        click.secho("Error: A password is required. Use --gen-pass to generate one automatically.", fg="red")
        sys.exit(1)

    # Step 3: Perform encryption
    try:
        crypter = Cryptokey(password, toml_code, output)
        crypter.generate()
        click.secho(f"Encryption successful! Output saved to: {output}", fg="green")
    except Exception as e:
        click.secho("Encryption failed due to an unexpected error.", fg="red")
        click.echo(f"Details: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
