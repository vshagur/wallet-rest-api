#! /bin/bash
coverage run --source='.'  manage.py test tests
coverage report
