from src.utils.compare import get_repo_info, search_contents_readme
import click

# example command line usage: python -m src/cli/scorecard.py --repository NOAA-OWP/topmodel

@click.option('--repository', '-r', help='The repository name to search for', required=True, type=str)

@click.command()
def scorecard(repository):
    # get readme and compare
    data = get_repo_info(repository)
    found, total =search_contents_readme(data)

    if found == total:
        click.echo(click.style(f'✔ All sections found in the readme file! ({data}/{total})', fg='green'))
    else:
        click.echo(click.style(f'✘ Not all sections found in the readme file! ({found}/{total}) sections found', fg='red'))

    # get license and compare


if __name__ == "__main__":
    scorecard()