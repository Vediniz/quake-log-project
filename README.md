# Quake Log

A QuakeLog is a log file that records events such as player deaths, match statistics, and weapon usage for analysis and tracking purposes.

The project aims to separate specific data, such as players involved in each match and their statuses, like the number of deaths and kills, as well as the abilities used.

# Requirements

- Python 3

To run tests, you must install Robot Framework.

If you want to run tests in a controlled environment, use a virtual environment (venv):

    python -m venv .venv 

To activate the virtual environment:

    Linux: source .venv/bin/activate
    Windows: .venv\Scripts\activate.ps1

If there is an issue with the PowerShell policy, use the following command and then activate the .venv again:

    Set-ExecutionPolicy RemoteSigned

With the virtual environment activated, install Robot Framework. Navigate to the tests folder:

    cd tests
    pip install -r requirements.txt

# How to Execute the Project

In the project folder (quake-log-project), to execute the general report:

    Linux: python3 main.py /data/qgames.log game_statistics
    Windows: py main.py /data/qgames.log game_statistics

To execute the "Kill by Means" report:

    Linux: python3 main.py /data/qgames.log death_statistics
    Windows: py main.py /data/qgames.log death_statistics

# How to Execute Tests

In the test folder (quake-log-project/tests), run the following command:

    robot -d ./results -L Trace quake_log_tests.robot 

This command will create a results folder with logs. Open log.html to view the details of the test execution.
