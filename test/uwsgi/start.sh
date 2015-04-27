#!/usr/bin/env bash

uwsgi --plugin python,http --http :9090 --wsgi-file test.py
