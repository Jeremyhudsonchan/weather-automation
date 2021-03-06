# Automation Program to retrieve monthly temperature data

## Data collected from

- weather.com

## Installing python

Install python latest version from official website

- python.org/downloads/

Or

Update python using Homebrew

```cmd
brew install python3
```

Check python version

```cmd
python3 --version
```

## Setting up venv

- Creating virtual environment

```cmd
python3 -m venv venv
```

- Enter venv

```cmd
source venv/bin/activate
```

- Install modules

```cmd
pip3 install -r requirements.txt
```

## Running the program

```cmd
python3 get_monthly_temperature.py
```

### Enter the following information

- Desired Location
- File Name
- Desired Month
- Data Directory

## Data

- Data will be saved inside the selected directory
  - i.e. /data

## Checking data collected

- python unittest on csv file

```cmd
python3 test_case.py
```
