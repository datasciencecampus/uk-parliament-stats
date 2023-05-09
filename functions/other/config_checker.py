import config
import re 

def config_checker(config):
    """
    Check the parameters in the config file

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if any of the subsequent checks fail
    """
    config_checks = [check_config_data_type,
                     check_config_download_data,
                     check_config_file_size,
                     check_config_sections,
                     check_config_date_start,
                     check_config_date_end,
                     check_config_use_proxies,
                     check_config_verbose,
                     check_config_search_what]

    for check in config_checks:
        check(config)

def check_config_data_type(config):
    """
    Check the data type is 'RDS' or 'XML'

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if data_type is not 'RDS' or 'XML'
    """
    if config.data_type not in ['RDS','XML']:
        raise ValueError("Error: data_type in config.py should either be 'RDS' or 'XML'")
    
def check_config_download_data(config):
    """
    Check the download data argument is a boolean

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if download_data argument is not a boolean
    """
    if config.download_data not in [True, False]:
        raise ValueError("Error: download_data in config.py should either be True or False")
    
def check_config_file_size(config):
    """
    Check the file size is not in ['All','1000','10000','100000']

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if file size invalid i.e. within ['All','1000','10000','100000']
    """
    if config.file_size not in ['All','1000','10000','100000']:
        raise ValueError("Error: file_size in config.py should either be 'All', '1000', '10000', or '100000'")
    
def check_config_sections(config):
    """
    Check the section is a valid argument one of ['debates','divisionsonly','future','london-mayors-questions',
    'lordsdivisionsonly','lordspages','ni','regmem','sp-motions','sp-new','sp-questions','sp-written','sp',
    'standing','westminhall']

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if section is not in required selection
    """
    for section in config.sections:
        if section not in ['debates','divisionsonly','future','london-mayors-questions','lordsdivisionsonly','lordspages',
                           'ni','regmem','sp-motions','sp-new','sp-questions','sp-written','sp','standing','westminhall']:
            raise ValueError(f"Error: section {section} in config.py is not valid.")

def check_config_date_start(config):
    """
    Check start date is in correct date format (dd/mm/yyyy)

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if start date has incorrect format
    """
    if  re.search(r'\d{2}/\d{2}/\d{4}', config.date_start) is None:
        raise ValueError("Error: date_start in config.py should be in dd/mm/yyyy format")
    
def check_config_date_end(config):
    """
    Check end date is in correct date format (dd/mm/yyyy)

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        if end date has incorrect format
    """
    if  re.search(r'\d{2}/\d{2}/\d{4}', config.date_end) is None:
        raise ValueError("Error: date_end in config.py should be in dd/mm/yyyy format")
    
def check_config_use_proxies(config):
    """
    Check use proxies is Boolean

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        use proxies is not a boolean
    """
    if config.use_proxies not in [True,False]:
        raise ValueError("Error: use_proxies in config.py should either be True or False")
    
def check_config_verbose(config):
    """
    Check verbose is Boolean

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        verbose is not a boolean
    """   
    if config.verbose not in [True,False]:
        raise ValueError("Error: verbose in config.py should either be True or False")
    
def check_config_search_what(config):
    """
    Check search what argument is one of ['Both','Text','Agenda']

    parameters
    ----------
    config : module
        configuration settings file

    Raises
    ------
    ValueError
        search what is not in selection
    """
    if config.search_what not in ['Both','Text','Agenda']:
        raise ValueError("Error: search_what in config.py should either be Both, Text or Agenda")