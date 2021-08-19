# SOMEF [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)
Software Metadata Extraction Framework: A command line interface for automatically extracting relevant information from readme files.

**Authors:** Daniel Garijo, Allen Mao, Haripriya Dharmala, Vedant Diwanji, Jiaying Wang and Aidan Kelley.

## Features
Given a readme file (or a GitHub repository) SOMEF will extract the following categories (if present):

- **Name**: Name identifying a software component
- **Full name**: Name + owner (owner/name)
- **Full title**: If the repository is a short name, we will attempt to extract the longer version of the repository  name
- **Description**: A description of what the software does.
- **Citation**: Preferred citation (usually in `.bib` form) as the authors have stated in their readme file.
- **Installation instructions**: A set of instructions that indicate how to install a target repository
- **Invocation**: Execution command(s) needed to run a scientific software component
- **Usage examples**: Assumptions and considerations recorded by the authors when executing a software component, or examples on how to use it.
- **Documentation**: Where to find additional documentation about a software component.
- **Requirements**: Pre-requisites and dependencies needed to execute a software component.
- **Contributors**: Contributors to a software component
- **FAQ**: Frequently asked questions about a software component
- **Support**: Guidelines and links of where to obtain support for a software component
- **License**: License and usage terms of a software component
- **Contact**: Contact person responsible for maintaining a software component
- **Download URL**: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- **DOI**: Digital Object Identifier associated with the software (if any)
- **DockerFile**: Build file to create a Docker image for the target software
- **Notebooks**: Jupyter notebooks included in a repository
- **Executable notebooks**: Jupyter notebooks ready for execution (e.g., through myBinder)
- **Owner**: Name of the user or organization in charge of the repository
- **Keywords**: set of terms used to commonly identify a software component
- **Source code**: Link to the source code (typically the repository where the readme can be found)
- **Releases**: Pointer to the available versions of a software component
- **Changelog**: Description of the changes between versions
- **Issue tracker**: Link where to open issues for the target repository
- **Programming languages**: Languages used in the repository
- **Acknowledgements**: People or institutions that the authors would like to acknowledge in their software component

We use different supervised classifiers, header analysis, regular expressions and the GitHub API to retrieve all these fields (more than one technique may be used for each field)

## Documentation
See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)

## Requirements

- Python 3.6

SOMEF has also been tested on Python 3.7 and 3.8.

## Install from GitHub
To run SOMEF, please follow the next steps:

Clone this GitHub repository

```
git clone https://github.com/KnowledgeCaptureAndDiscovery/somef.git
```

Install somef (you should be in the folder that you just cloned). Note that for Python 3.7 and 3.8 the module Cython should be installed in advanced (through the command: `pip install Cython`). 

```
cd somef
pip install -e .
```

Test SOMEF installation

```bash
somef --help
```

If everything goes fine, you should see:

```bash
Usage: somef [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  configure  Configure credentials
  describe   Running the Command Line Interface
  version    Show somef version.
```

## Installing through Docker
We provide a Docker image with SOMEF already installed. To run through Docker, you may build the Dockerfile provided in the repository by running:

```bash
docker build -t somef .
```
Or just use the Docker image already built in [DockerHub](https://hub.docker.com/r/kcapd/somef):

```bash
docker pull kcapd/somef
```

Then, to run your image just type:

```bash
docker run -it kcapd/somef /bin/bash
```

And you will be ready to use SOMEF (see section below). If you want to have access to the results we recommend [mounting a volume](https://docs.docker.com/storage/volumes/). For example, the following command will mount the current directory as the `out` folder in the Docker image:

```bash 
docker run -it --rm -v $PWD/:/out kcapd/somef /bin/bash
```
If you move any files produced by somef into `/out`, then you will be able to see them in your current directory.


## Usage 

### Configure
Before running SOMEF, you must configure it appropriately. Run

```bash
somef configure
```

And you will be asked to provide the following: 

- A GitHub authentication token [**optional, leave blank if not used**], which SOMEF uses to retrieve metadata from GitHub. If you don't include an authentication token, you can still use SOMEF. However, you may be limited to a series of requests per hour. For more information, see [https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) 
- The path to the trained classifiers (pickle files). If you have your own classifiers, you can provide them here. Otherwise, you can leave it blank

If you want somef to be automatically configured (without GitHUb authentication key and using the default classifiers) just type:

```bash
somef configure -a
```

### Run SOMEF

```bash
$ somef describe --help
  SOMEF Command Line Interface
Usage: somef describe [OPTIONS]

  Running the Command Line Interface

Options:
  -t, --threshold FLOAT           Threshold to classify the text  [required]
  Input: [mutually_exclusive, required]
    -r, --repo_url URL            Github Repository URL
    -d, --doc_src PATH            Path to the README file source
    -i, --in_file PATH            A file of newline separated links to GitHub
                                  repositories

  Output: [required_any]
    -o, --output PATH             Path to the output file. If supplied, the
                                  output will be in JSON

    -g, --graph_out PATH          Path to the output Knowledge Graph file. If
                                  supplied, the output will be a Knowledge
                                  Graph, in the format given in the --format
                                  option
    -c, --codemeta_out PATH       Path to an output codemeta file (in JSON-LD)

  -f, --graph_format [turtle|json-ld]
                                  If the --graph_out option is given, this is
                                  the format that the graph will be stored in

  -h, --help                      Show this message and exit.
```

## Usage example:
The following command extracts all metadata available from [https://github.com/dgarijo/Widoco/](https://github.com/dgarijo/Widoco/). 

```bash
somef describe -r https://github.com/dgarijo/Widoco/ -o test.json -t 0.8
```

Try SOMEF in Binder with our sample notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)

### Add/Remove a Category:

If the user wants to run the classifier for an additional category or wants to remove an existing category, corresponding path entry in the config.json should be provided and the category type should be added/removed in the category variable in cli.py

## Contribute:

If you want to contribute with a pull request, please do so by submitting it to the `dev` branch.

## Cite SOMEF:
```
@INPROCEEDINGS{9006447, 
author={A. {Mao} and D. {Garijo} and S. {Fakhraei}}, 
booktitle={2019 IEEE International Conference on Big Data (Big Data)}, 
title={SoMEF: A Framework for Capturing Scientific Software Metadata from its Documentation}, 
year={2019}, 
url={http://dgarijo.com/papers/SoMEF.pdf},
pages={3032-3037}
} 
```

## Next features:
To see upcoming features, please have a look at our [open issues](https://github.com/KnowledgeCaptureAndDiscovery/somef/issues) and [milestones](https://github.com/KnowledgeCaptureAndDiscovery/somef/milestones)
