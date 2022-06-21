#!/bin/bash
echo Running unit tests
python -m pytest --html=tests/unittests/reports/run/report.html --cov=ska_sdc --cov-report html:tests/unittests/reports/cov tests/unittests