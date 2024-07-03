
import click

#TODO: add the rest of the scorecard principles 

#print FAIR principles and the number of principles that are met

def print_f1_principle(expected, standard):
    """
    Description :
    print message that belongs to f1 principle 

    params:
    expected(int): from f1_unique_identifier function output - 'f1_found' which is the number of search words that are found in the data from ['unique identifier','DOI','zenodo','badge']
    standard(int): from f1_unique_identifier function output - 'f1_searched' which is the number of search words that are listed in the search_words list ['unique identifier','DOI','zenodo','badge']

    returns:
    None
    """
    #print the FAIR principles based on the expected and standard 
    if expected == standard:
        click.echo(click.style(f'✔ F1. Software is assigned a globally unique and persistent identifier - DOI or SWHID was FOUND', fg='green'))
    else:
        click.echo(click.style(f'✘ F1. Software is NOT assigned a globally unique and persistent identifier- A DOI or SWHID was NOT FOUND', fg='red'))

def print_f1_plus_principle(expected, standard):
    """
    Description :
    Print message that belongs to f1+ principle

    params:
    expected(str): the repository name that is being searched for. Note - this is not the url . Format : owner/repo_name

    standard(str): the repository name that is being searched for. Note - this is not the url . Format : owner/repo_name

    returns:
    None
    
    """
    #print the FAIR principles based on the expected and standard 
    if expected == standard:
        click.echo(click.style(f'✔ F1+ Software uses a version control program . repository name = {expected}', fg='green'))
    else:
        click.echo(click.style(f'✘ F1+ Software does NOT use a version control program ', fg='red'))

def print_f1_1principle(expected, standard):
    """
    Description :
    Print message that belongs to f1.1 principle

    params:
    """
    #print the FAIR principles based on the expected and standard 
    if expected == standard:
        click.echo(click.style(f'✔ F1.1. Components of the software representing levels of granularity are assigned distinct identifiers.({expected}/{standard})', fg='green'))
    else:
        click.echo(click.style(f'✘ F1.1. Components of the software representing levels of granularity are NOT assigned distinct identifiers.({expected}/{standard})', fg='red'))

def print_f1_2principle(expected, standard,duplicates):
    """
    Description :
    Print message that belongs to f1.2 principle

    params:
    expected(int): the number of formatted via semantic versioning that are found in the data
    standard(int): the number of versions that are found in the data
    duplicates(int): the number of duplicates that are found in the data

    returns:
    None
    """



    #print the FAIR principles based on the expected and standard 
    if expected ==standard and duplicates <0:
        click.echo(click.style(f'✔ F1.2. Different versions of the software are assigned distinct identifiers. Total versions found using semantic versioning {expected}/{standard}. No duplicates found ', fg='green'))
    elif standard ==0:
        click.echo(click.style(f'✘ F1.2. Different versions of the software are NOT assigned distinct identifiers. No VERSIONING FOUND', fg='red'))
    else:
        click.echo(click.style(f'✘ F1.2. Different versions of the software are NOT assigned distinct identifiers. Total versions found using semantic versioning {expected}/{standard}. Duplicates found {duplicates}', fg='red'))


def print_f2_plus_principle(expected, standard,found_sections):
    """
    Description :
    Print message that belongs to f2+ principle

    params:
    expected(int): the number of sections that are found in the readme data
    standard(int): the number of sections that are expected in the readme data 
    found_sections(list): the sections that are found in the readme data 

    returns:
    None
    
    """


    #print the FAIR principles based on the expected and standard 
    if expected == standard:
        click.echo(click.style(f'✔ F2+.README file includes descriptive documentation.The following sections were found {found_sections}. ({expected}/{standard})', fg='green'))
    if expected >0 :
        click.echo(click.style(f'✘ F2+.README file includes SOME descriptive documentation.The following sections were found {found_sections}. ({expected}/{standard})', fg='yellow'))

    else:
        click.echo(click.style(f'✘ F2+.README file DOES NOT include descriptive documentation.The following sections were found {found_sections}. ({expected}/{standard})', fg='red'))