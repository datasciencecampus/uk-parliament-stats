<img src="https://github.com/datasciencecampus/awesome-campus/blob/master/ons_dsc_logo.png">

# parlmentions

[![Twitter](https://img.shields.io/twitter/url?label=Follow%20%40DataSciCampus&style=social&url=https%3A%2F%2Ftwitter.com%2FDataSciCampus)](https://twitter.com/DataSciCampus)

## About
Identifying frequency and sentiment of mentions of an organisation and classifying debates from UK Parliament transcripts (Hansard)

## Installation

### Pre-commit actions
This repository contains a configuration of pre-commit hooks. These are language agnostic and focussed on repository security (such as detection of passwords and API keys). If approaching this project as a developer, you are encouraged to install and enable `pre-commits` by running the following in your shell:
   1. Install `pre-commit`:

      ```
      pip install pre-commit
      ```
   2. Enable `pre-commit`:

      ```
      pre-commit install
      ```
Once pre-commits are activated, whenever you commit to this repository a series of checks will be executed. The pre-commits include checking for security keys, large files and unresolved merge conflict headers. The use of active pre-commits are highly encouraged and the given hooks can be expanded with Python or R specific hooks that can automate the code style and linting. For example, the `flake8` and `black` hooks are useful for maintaining consistent Python code formatting.

**NOTE:** Pre-commit hooks execute Python, so it expects a working Python build.

## Workflow

The process has been modularised so that the user can either use historic data or download the latest data for specific dates. For more detailed information about the process and variables see `config.py`. In essence, it is split into three parts:

1. Data download and cleaning:
    - Data is either downloaded from a pre-made CSV file or a CSV file is created from online XML files from (https://www.theyworkforyou.com/pwdata/scrapedxml). If data is already downloaded, you can load in the CSV file instead.
2. Finding mentions of Organisations in text:
    - Any organisations listed in `config.py` will be searched for in the CSV file. In the output file the name of the organisation will be listed as well as contextual text either side where it is mentioned.
3. Classifying debates:
    - Each debate will then be classified using a `spaCy` model based on the configuration in `functions/model_rules/patterns.py`. This project has been tuned to work for Office for National Statistics purposes currently.

## Using

To clone the repo, use:

`git clone https://github.com/rozzahh/uk-parliament-stats.git`

See `requirements.txt` for the required packages.

To run the code run `parlmentions.py`. Requires spaCy `en_core_web_md`:

` python -m spacy download en_core_web_md`

## Project Structure

### parlmentions.py

The main python file to call.

### config.py

The main configuration file for the parlmentions.py pipeline.

### /raw-data 

Where the downloaded XML or RDS files are saved.

### /outputs

Where the output files are saved.

### /user-engagement

Files used in user/stakeholder engagement.

### /functions

Functions to download, parse and analyse the data.

##### /functions/data_download/parliament_xml_download.py

Python script for downloading XML files of Hansard from https://www.theyworkforyou.com/pwdata/scrapedxml/ using variables from `config.py`. 

#### /functions/data_download/parliament_rds_download.py

Python script for downloading the Harvard RDS file as a CSV. Use `config.py` to specify if you want to download the entire dataset (2.2 GB) or random cuts.

#### /functions/data_processing/parliament_xml_processing.py

Python script for processing the downloaded XML files and saving to a CSV file. 

#### /functions/data_processing/df_prep.py

Python script for preparing the saved CSV file for analysis.

#### /functions/model_rules/patterns.py

A configuration file holding labelled classification rules.

#### /functions/model_rules/topic_classification.py

Python script that runs a spaCy model to classify topics.

#### /functions/other/config_checker.py

Python script that makes sure the config file is ok.

#### /functions/other/ons_network.py

Python script that calls proxies from the ONS network.

^ To be removed if made public.

## Acknowledgements

Data used to build and test this project comes from Harvard Dataverse (https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/L4OAKN/W2SVMF&version=1.0). Due to the reliance of `R` for RDS files, we have converted this file to a CSV file ourselves and hosted on a server.

```Rauh, Christian; Schwalbach, Jan, 2020, "Corp_HouseOfCommons_V2.rds", The ParlSpeech V2 data set: Full-text corpora of 6.3 million parliamentary speeches in the key legislative chambers of nine representative democracies, https://doi.org/10.7910/DVN/L4OAKN/W2SVMF, Harvard Dataverse, V1```
