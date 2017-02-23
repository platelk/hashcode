# hashcode

## Requirement

This project use :

* python3
* pip
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Make sure you have this program installed and working

## Setup

To start working on the project:

  $> workon hashcode

This will setup the virtualenv for this project

Then install the deps

  $> pip install -r requirements.txt


### If you add a dependencices

  * First install the deps

  $> pip install <your_package>

  * Then save it for the others

  $> pip freeze > requirements.txt


## Run

To run the app

  $> python app/main.py FILE1 FILE2 ...