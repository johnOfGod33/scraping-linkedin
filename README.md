## Selenium Project

Example of a selenium project. dynamique scraping of jobs data on linkedin after login

## Features

- authentication (login + cookie management)
- dynamic scraping of jobs data 
- saving jobs data in a csv file

### Installation

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the root directory of the project and add the following variables:

```bash
LINKEDIN_USERNAME=your_username
LINKEDIN_PASSWORD=your_password
DRIVER_PATH=/path/to/chromedriver
```