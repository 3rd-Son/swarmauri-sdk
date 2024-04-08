# SwarmaURI SDK
This repository includes core interfaces, standard ABCs, and standard concrete references of the SwarmaURI Framework.

## Steps to compile python package from source
```bash
git clone https://github.com/cobycloud/swarmauri
cd swarmauri
python -m build
pip install ./dist/swarmauri-0.1.10.tar.gz[full] --force-reinstall
```
## ./combined
This includes convenience outputs to enable conversations with GPTs.

## ./dist
This includes SwarmaURI python package builds. This will eventually be excluded from this directory in favor of pypi.

## ./scripts
This includes convenience scripts that are nother included with the SwarmaURI SDK.
#### /scripts/combine_files.py
```bash
#This script generates the convenience outputs found in ./combined
python ./combine_files.py
```

## ./swamauri
This includes the libaries for the SwarmaURI python package.

## ./tests
This includes test cases for the SwarmaURI python  package.