# Measuring e-Commerce Metric Changes in Online Experiments

Codebase for the above titled paper, to appear in TheWebConf (neé WWW) 2023.

**Abstract**: Digital technology organizations routinely use online experiments (e.g. A/B tests) to guide their product and business decisions. In e-commerce, we often measure changes to transaction- or item-based business metrics such as Average Basket Value (ABV), Average Basket Size (ABS), and Average Selling Price (ASP); yet it remains a common pitfall to ignore the dependency between the value/size of transactions/items during experiment design and analysis. We present empirical evidence on such dependency, its impact on measurement uncertainty, and practical implications on A/B test outcomes if left unmitigated. By making the evidence available, we hope to drive awareness of the pitfall among experimenters in e-commerce and hence encourage the adoption of established mitigation approaches. We also share lessons learned when incorporating selected mitigation approaches into our experimentation analysis platform currently in production.

If you find the code useful for your work, please consider citing with the following BibTeX entry.

```BibTeX
@inproceedings{liu2023measuringecommerce,
author = {Liu, C. H. Bryan and McCoy, Emma J.},
title = {Measuring e-Commerce Metric Changes in Online Experiments},
year = {2023},
isbn = {978145039419},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3543873.3584654},
doi = {10.1145/3543873.3584654},
booktitle = {Companion Proceedings of the ACM Web Conference 2023},
location = {Austin, TX, USA},
series = {WWW '23 Companion}
}
```

## Setup
This file assumes you have access to a \*nix-like machine (both MacOS or
Linux would do). If you have a Windows machine, the notebook should still work
provided you have the right Python packages installed, but it is not tested.

This project uses `pyenv` and `poetry` for package management.
Before you start, please ensure you have `gcc`, `make`, and `pip` installed.

### Installing `pyenv`

For Linux (together with other required libraries):

``` bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
wget -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

chmod u+x pyenv-installer
./pyenv-installer
```

For OS X:
```
brew install pyenv
brew install pyenv-virtualenv
```

We then need to configure the PATHs:
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

...and install the right Python version for our environment:
```
pyenv install 3.9.10
```

### Installing `poetry`
See https://python-poetry.org/docs/#installation for the installation instructions.

### Download the repository and sync the environment
```
git clone https://github.com/liuchbryan/oce-ecomm-abv-calculation.git
cd oce-ecomm-abv-calculation  

# Switch to Python 3.9.10 for pyenv
pyenv local 3.9.10
poetry env use ~/.pyenv/versions/3.9.10/bin/python
poetry install
```

### Run the Jupyter notebooks  
```
poetry shell
```

Within the newly spawn up virtualenv shell, run
```
jupyter notebook
```

Once you are done, terminate the Jupyter server using Ctrl+C, and type `exit` to exit the virtualenv shell.


## Notebooks

This repo contain several notebooks that run the experiments, organise the results, and generate the tables and figures featured in the paper.

Experiments:
* `E01 - Vanilla and One-way Bootstrap.ipynb` runs experiments that calculates the vanilla sample standard error (SE) and their re-estimates using one-way bootstrap.
* `E02 - Two-way Bootstrap.ipynb` runs experiments that re-estimates the SE for the average selling price (ASP) metric using two-way bootstrap.

Figures:
* `F01 - Response vs Next Response.ipynb` plots Figure 1 of the paper + the same data in other graph representations / a different scale.
* `F02-03 - Vanilla vs Oneway Bootstrap SE.ipynb` plots Figures 2 and 3 of the paper. It also shows different way to plot the same set of data comparing the vanilla sample SEs to one-way bootstrap estimates.
* `F04 - Actual Power and CI Coverage.ipynb` plots Figures 4 of the paper.

Tables:
* `T01 - Dataset Summary.ipynb` generates the summary of the two public datasets used in the paper, which is included in Table 1 of the paper.
* `T02 - One-way Two-way Bootstrap Comparison (ASP).ipynb` extracts the experiment data that goes in Table 2 of the paper.