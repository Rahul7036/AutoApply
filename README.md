# Naukri Auto Apply

An automated job application system for Naukri.com that helps you automatically apply to jobs based on your keywords.

## Setup

1. Install Python 3.8 or higher
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Naukri credentials:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your Naukri email and password

## Usage

Run the application:
```bash
python auto_apply.py
```

The application will:
1. Log in to your Naukri account
2. Search for jobs based on your keyword
3. Automatically apply to matching jobs

## Features

- Automated login to Naukri.com
- Job search based on keywords
- Automatic job application
- Secure credential management using environment variables

## Note

Please use this tool responsibly and in accordance with Naukri.com's terms of service. Excessive automated applications might be detected and could affect your account status.