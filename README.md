README for jci-interview-problem
================================

jci-interview-problem provides a solution for the problem described in PROBLEM.txt

Development is hosted on GitHub: https://github.com/shaines1/jci-interview-problem

Install
-------

jci-interview-problem requires Python 3.6.7 or greater. Lower versions of
Python 3 *may* be supported, but are untested. Python can be downloaded
[here](https://www.python.org/downloads/).

jci-interview-problem does not require any additional software packages and runs requires with a standard version of Python.

Running
-------

jci-interview-problem can be run with ::

    python3 main.py

Logging information can be found in .jci_interview_problem.log

Examples
--------
View command line help ::

    python3 main.py -h

Run a sample message parsing with segment filter ::

    python3 main.py --file <messages_file.txt> --segment NAM --limit 100

Run unit tests ::

    python3 -m unittest discover