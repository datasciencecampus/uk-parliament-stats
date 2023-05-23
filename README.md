<img src="https://github.com/datasciencecampus/awesome-campus/blob/master/ons_dsc_logo.png">

# parlmentions
[![Stability](https://img.shields.io/badge/stability-experimental-orange.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#experimental)
[![codecov](https://codecov.io/gh/datasciencecampus/uk-parliament-stats/branch/main/graph/badge.svg?token=N8f9f7nbOs)](https://codecov.io/gh/datasciencecampus/uk-parliament-stats)
[![Twitter](https://img.shields.io/twitter/url?label=Follow%20%40DataSciCampus&style=social&url=https%3A%2F%2Ftwitter.com%2FDataSciCampus)](https://twitter.com/DataSciCampus)

## About
Identifying frequency and sentiment of mentions of an organisation and classifying debates from UK Parliament transcripts (Hansard)

## Installation

To clone the repo, use:

`git clone https://github.com/datasciencecampus/uk-parliament-stats.git`

See `requirements.txt` for the required packages. Package versions haven't been extensively tested so other versions might be suitable if the suggested versions aren't available.

The spaCy language model `en_core_web_md` is also required. This can be downloaded using:

`python -m spacy download en_core_web_md`

If you have difficulties with this, a `.whl` for the model can be [manually downloaded from GitHub](https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.5.0/en_core_web_md-3.5.0-py3-none-any.whl), which can then be installed using `pip` (i.e. `pip install <downloaded-file-name>.whl`).

### Proxy Setup

The package includes functions to overcome difficulties that arise when using organisational proxy servers. The `config.py` has an option to turn this functionality on, `use_proxies`, as well as the filepath to look for a `proxies.json` file containing a list of possible proxies, `proxy_list_fp`. ONS colleagues can find a working copy of this file on [SharePoint](https://officenationalstatistics.sharepoint.com/sites/dscdsc/_layouts/15/download.aspx?UniqueId=042aa1d3ef804668aeb1200720dc683e&e=3crWBs). It is recommended to then put this file in a folder at the highest level of the repo called `/secrets/`.

**NOTE:** we have not tested this functionality from within departments other than ONS, so results may vary depending on the permissiveness of the environment.

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
Once pre-commits are activated, whenever you commit to this repository a series of checks will be executed. The pre-commits include checking for security keys, large files and unresolved merge conflict headers.

## Workflow

The process has been modularised so that the user can either use historic data or download the latest data for specific dates. For more detailed information about the process and variables see `config.py`. In essence, it is split into three parts:

1. Data download and cleaning:
    - Data is either downloaded from a pre-made CSV file or a CSV file is created from online XML files from (https://www.theyworkforyou.com/pwdata/scrapedxml). If data is already downloaded, you can load in the CSV file instead.
2. Finding mentions of Organisations in text:
    - Any organisations listed in `config.py` will be searched for in the CSV file. In the output file the name of the organisation will be listed as well as contextual text either side where it is mentioned.
3. Classifying debates:
    - Each debate will then be classified using a `spaCy` model based on the configuration in `functions/model_rules/patterns.py`. This project has been tuned to work for Office for National Statistics purposes currently.

## Using

First, configure the `config.py` to align with the intended analysis, bearing in mind whether you are downloading data or analysing pre-downloaded data and if you are using proxy settings or not. Update the `organisations` list to search for different government organisations (these are ONS, OSR and UKSA by default).

Then run the analysis from the command line using:

`python parlmentions.py`

This produces a `.csv` containing all requested parliamentary speeches with metadata and a flag for whether the selected organisations are mentioned.

## Project Structure

`/data` location for downloaded files <br> <br>
`/outputs` location where outputs are saved <br> <br>
`/src` functions for the pipeline <br>
&nbsp; &nbsp; &nbsp; `/data_download` functions for downloading data <br>
&nbsp; &nbsp; &nbsp; `/data_processing` functions for processing data <br>
&nbsp; &nbsp; &nbsp; `/model_ML` functions for training the model <br>
&nbsp; &nbsp; &nbsp; `/model_rules` functions for model control <br>
&nbsp; &nbsp; &nbsp; `/other` functions with miscellaneous functionality <br> <br>
`/tests` tests for associated functions <br> <br>
`.gitignore` files to ignore when interacting with git <br> <br>
`.pre-commit-hooks.yaml` configuration for pre-commits <br> <br>
`README.md` important information about the repository <br> <br>
`config.py` - configuration settings for the pipeline<br> <br>
`parlmentions.py` - file to run the pipeline <br> <br>
`requirements.txt` - information about the package dependencies <br> <br>

## Maintenance

We are a small team and, while we aim to keep the package running, we have limited capacity for maintenance. If you come across any bugs or think of new features, consult the [contributing guidance](CONTRIBUTING.md) for how to best get involved.

## Acknowledgements

This repository was first developed by [Rory Corbett](https://github.com/rorycorbett), before being picked up by the Data Science Campus, ONS.

Data used to build and test this project comes from Harvard Dataverse (https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/L4OAKN/W2SVMF&version=1.0). Due to the reliance of `R` for RDS files, we have converted this file to a CSV file ourselves and hosted on a server.

```Rauh, Christian; Schwalbach, Jan, 2020, "Corp_HouseOfCommons_V2.rds", The ParlSpeech V2 data set: Full-text corpora of 6.3 million parliamentary speeches in the key legislative chambers of nine representative democracies, https://doi.org/10.7910/DVN/L4OAKN/W2SVMF, Harvard Dataverse, V1```
