# NYU MyTime CLI

This Python tool provides a command line interface for the NYU MyTime student employee time-tracking portal.
It is based on the Selenium library, which allows it to programmatically control a headless browser.

## Install

Download this repository.

```bash
git clone https://github.com/matteosandrin/nyu-mytime-cli
```

Enter the directory and install the Python package.

```bash
cd nyu-mytime-cli
pip install .
```

Download the `chromedriver` from [http://chromedriver.chromium.org](http://chromedriver.chromium.org/) and place it in `/usr/local/bin/` (This path can be modified in the configuration file).

```bash
wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
cp ./chromedriver /usr/local/bin/
```

## Usage

```bash
# Punch into work
nyu-mytime in 

# Punch out of work
nyu-mytime out

# Set a config variable
nyu-mytime config VARIABLE

# Verify configuration
nyu-mytime config
```
 