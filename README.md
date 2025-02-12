## Selenium Project

## Features

- Login to LinkedIn
- connection with cookies
- save cookies  

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