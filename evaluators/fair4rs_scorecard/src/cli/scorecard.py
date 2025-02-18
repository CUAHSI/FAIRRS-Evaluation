from src.utils.compare import get_repo_info, f1_1_components_unique_identifier,f1_unique_identifier, f1_2_versions_unique_identifier, f_2_plus_readme_contents

from src.utils.messages import print_f1_principle, print_f1_plus_principle, print_f1_1principle, print_f1_2principle, print_f2_plus_principle
import click

# example command line usage: python -m src/cli/scorecard.py --repository NOAA-OWP/topmodel

@click.option('--repository', '-r', help='The repository name to search for', required=True, type=str)

@click.command()
def scorecard(repository):
    #f1_unique_identifier
    data=get_repo_info(repository, 'readme')
    f1_found,f1_searched = f1_unique_identifier(data)
    print_f1_principle(f1_found, f1_searched)

    #f1_plus_version_control_program
    #this is built on inspecting github repositories so meeting this principle is based on the fact that the repository is on github
    print_f1_plus_principle(repository,repository)

    #f1_1_components_unique_identifier
    #TODO: finish this function in compare.py and add here 

    #f1_2_versions_unique_identifier
    data=get_repo_info(repository, 'releases')
    len_formatted_versions, len_found, len_duplicates = f1_2_versions_unique_identifier(data)
    print_f1_2principle(len_formatted_versions, len_found, len_duplicates)

    #f2_plus_readme_contents
    data=get_repo_info(repository, 'readme')
    len_found_readme, len_search_words_readme,found_sections = f_2_plus_readme_contents(data)
    print_f2_plus_principle(len_found_readme, len_search_words_readme,found_sections)





if __name__ == "__main__":
    scorecard()