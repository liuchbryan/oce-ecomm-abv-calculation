# Measuring e-Commerce Metric Changes in Online Experiments


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
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
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