# Get Papers List

## Description
A Python program to fetch and filter research papers from PubMed based on a user-specified query.

## Installation
1. Install Poetry:
   ```bash
   pip install poetry

   1.install  this cammand in powershellin te project terminal
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

    2. $env:Path += ";$env:APPDATA\Python\Scripts"
    to route path run tis command
    
    3.Then install poetry
    poetry install  run this command

    4.poetry --versionpoetry --version
    check te version it should show Poetry (version 2.1.1)

    5.pip install requests pandas run  this command to install pandav to save in csv file

    6. poetry run get-papers-list "diabetes" -f test.csv --debug run this command to fect the data from api and save the coomming data into csv file

    output will be in a csv format  u can see