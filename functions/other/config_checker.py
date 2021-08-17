import re

import config

def config_checker():
    if config.data_type not in ['RDS','XML']:
        raise ValueError("Error: data_type in config.py should either be 'RDS' or 'XML'")
    if config.download_data not in [True,False]:
        raise ValueError("Error: download_data in config.py should either be True or False")
    if config.file_size not in ['All','1000','10000','100000']:
        raise ValueError("Error: file_size in config.py should either be 'All', '1000', '10000', or '100000'")
    for section in config.sections:
        if section not in ['debates','divisionsonly','future','london-mayors-questions','lordsdivisionsonly','lordspages',
                           'ni','regmem','sp-motions','sp-new','sp-questions','sp-written','sp','standing','westminhall']:
            raise ValueError(f"Error: section {section} in config.py is not valid.")
    if  re.search(r'\d{2}/\d{2}/\d{4}', config.date_start) is None:
        raise ValueError("Error: date_start in config.py should be in dd/mm/yyyy format")
    if  re.search(r'\d{2}/\d{2}/\d{4}', config.date_end) is None:
        raise ValueError("Error: date_end in config.py should be in dd/mm/yyyy format")
    if config.use_proxies not in [True,False]:
        raise ValueError("Error: use_proxies in config.py should either be True or False")
    if config.verbose not in [True,False]:
        raise ValueError("Error: verbose in config.py should either be True or False")