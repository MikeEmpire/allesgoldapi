# Flask API

Using Flask to build a Restful API Server with Swagger document.

Integration with Flask-restplus, Flask-Cors, Flask-Testing, Flask-SQLalchemy,and Flask-OAuth extensions.

## Overview

Production URL: https://allesgoldapi.afam.app

## Getting Started

Create a virtual environment

```sh
python3 -m venv .venv
```

Activate virtual environment

```sh
source ./.venv/bin/activate
```

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Run Flask

### Run flask for develop

```
$ python app.py
```

In flask, Default port is `5000`

Swagger document page: `http://127.0.0.1:5000/api`

### Run flask for production

** Run with gunicorn **

In webapp/

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

- -w : number of worker
- -b : Socket to bind

## Unittest

```
$ nosetests webapp/ --with-cov --cover-html --cover-package=app
```

- --with-cov : test with coverage
- --cover-html: coverage report in html format

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restplus](http://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)
- [gunicorn](http://gunicorn.org/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)

[Wiki Page](https://github.com/tsungtwu/flask-example/wiki)

## Changelog

- Version 1.0 : Basic initialization with 4 routes for newsletters
