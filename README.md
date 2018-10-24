# Store-Manager

[![Build Status](https://travis-ci.org/Qadriyah/store-manager.svg?branch=api-v1)](https://travis-ci.org/Qadriyah/store-manager) [![Maintainability](https://api.codeclimate.com/v1/badges/40a62aea724af677d9cb/maintainability)](https://codeclimate.com/github/Qadriyah/store-manager/maintainability) [![Coverage Status](https://coveralls.io/repos/github/Qadriyah/store-manager/badge.svg?branch=api-v1)](https://coveralls.io/github/Qadriyah/store-manager?branch=Feat-api-v1) [![codecov](https://codecov.io/gh/Qadriyah/store-manager/branch/api-v1/graph/badge.svg)](https://codecov.io/gh/Qadriyah/store-manager)

Store Manager is a web application that helps store owners manage sales and product inventory  records. This application is meant for use in a single store.

## Getting Started

These instrauctions will get you a copy of the project up and runnig on your local machine for development and testing purposes.

### Prerequisites

You need `git` to get started.
Download and install a copy of [ git ](https://git-scm.com/downloads) for your operating system

## Installation

Run the following commands from the terminal to install the project on your local machine

```
* git clone https://github.com/Qadriyah/store-manager.git
* pip install -r requirements.txt
```

### Production ready code for the UI

```
git checkout gh-pages
```

### Production ready code for the API endpoints

```
git checkout api-v1
```

## Runing the tests

The following command runs all tests of the API. the -p switch supresses any warnings

```
pytest -p no:warnings
```

## Running selective tests

Tests are separated into different modules, the following commands run tests selectively

```
pytest test/test_authentication.py -p no:warnings
pytest test/test_products.py -p no:warnings
pytest test/test_sales.py -p no:warnings
pytest test/test_validations.py -p no:warnings
```

## Built With

- HTML - The markup language
- CSS - Used to describe how html elements are displayed
- Javascript - The only true language for the web
- Python Flask - Framework used for the API endpoints

## Links

- [gh-pages](https://qadriyah.github.io/store-manager/UI/)
- [No documentation yet]()

## Usage

### Default admin login details

```
Username: admin
Password: admin
```

### Default attendant login details

```
Username:
Password:
```

## Author

```
Baker Sekitoleko
```

## Acknowledgements

- [The Andela Community](https://andela.com/)
- [w3schools](https://www.w3schools.com/css/css_intro.asp)
- All the bootcampers whose advise was so helpful
