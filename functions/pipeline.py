from data_download.parliament_xml_download import download_xml_files
from data_download.parliament_rds_download import download_rds_file
from data_processing.parliament_xml_processing import process_xml_files

import config

def pipeline(config):
    if config.download_data is True:
        if config.data_type == 'XML':
            print('----------------Downloading xml files--------------')
            download_xml_files()
        elif config.data_type == 'RDS':
            print('----------------Downloading rds file--------------')
            download_rds_file()
    if config.process_files is True and config.data_type == 'XML':
        print('----------------Processing xml files--------------')
        process_xml_files()

pipeline(config)