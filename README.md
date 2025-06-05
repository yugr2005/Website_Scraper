# Website Scraper

This is a Python application that recursively scrapes a website and all its subpages using `requests` and `BeautifulSoup`.

## Features

- Scrapes text from a URL and internal links
- Prevents duplicate visits
- Recursively follows subpages on same domain
- Outputs clean page-by-page terminal previews

## How to Use

1. Install dependencies:
   ```bash
   poetry install
