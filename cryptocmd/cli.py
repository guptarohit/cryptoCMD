import click
from cryptocmd import CmcScraper, __version__
from datetime import datetime
from halo import Halo
from cryptocmd.utils import InvalidCoinCode


def validate_date(ctx, param, value):
    if value is None:
        return value
    try:
        datetime.strptime(value, "%d-%m-%Y")
    except ValueError:
        raise click.BadParameter("Incorrect date format, should be like: dd-mm-YYYY.")
    return value


spinner = Halo(spinner="dots")


@click.command()
@click.argument("coin_code")
@click.option("--start_date", "-s", callback=validate_date, help="Start date of data.")
@click.option("--end_date", "-e", callback=validate_date, help="End date of data.")
@click.option("--csv_name", "-n", help="Name of csv.")
@click.option(
    "--csv_path",
    "-p",
    default=".",
    type=click.Path(exists=True),
    help="Path to store csv.",
)
@click.version_option(
    __version__, "--version", "-v", prog_name=click.style("cryptocmd", fg="green")
)
def cli(coin_code, start_date, end_date, csv_name, csv_path):
    """Cryptocurrency historical market price data scraper 🐍.\n
        Basic usage:\n
        >>> cryptocmd BTC -s 1-1-2017 -e 1-10-2018
    """

    # verify start date is less than equal to end date
    if start_date and end_date:
        if start_date.split("-")[::-1] > end_date.split("-")[::-1]:
            raise click.BadParameter(
                "start_date cannot be greater than end_date.",
                param_hint=["--start_date", "--end_date"],
            )

    try:
        cmcs = CmcScraper(coin_code, start_date=start_date, end_date=end_date)
        spinner.start("Downloading data of {} coin 📊".format(coin_code.upper()))
        cmcs.get_data()
        spinner.succeed("Downloaded data of {} coin 📊".format(coin_code.upper()))
        spinner.start("Exporting data to CSV file 📄")
        cmcs.export_csv(csv_name, csv_path)
        spinner.succeed("Exported data to CSV file 📄\n🍰 ✨".encode("utf-8"))
    except InvalidCoinCode:
        spinner.fail("Invalid Coin Code")
    except (KeyboardInterrupt, SystemExit):
        spinner.stop_and_persist(symbol="🍰".encode("utf-8"), text="bye.")
