#!/bin/bash
rm spacey.db
FLASK_APP=vulnapp FLASK_DEBUG=1 flask run --host 127.0.0.1 --port 8085
