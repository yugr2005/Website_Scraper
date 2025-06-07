# Website Scraper

This is a Python application that recursively scrapes a website and all its subpages using `requests` and `BeautifulSoup` and represents it's data in a clean and good way.

---

## What It Does

- You enter the URL of a website (for example, a blog homepage)
- Visits that page, extracts the data using get function from <requests>, and then separate them out with the help of find_all function from <BeautifulSoup> on the basis of:
  - Main headings (`<h1>`)
  - Subheadings (`<h2>`, `<h3>`)
  - Paragraphs (`<p>`)
- Follows internal links within the same website (subpages) by finding all the `<a>` tags from the data (html format) and repeats the same process recursively
- This method gets stop when the subpage has no other link (a-tag) to visit further or if the link is already visited before
- Displays the scraped content in a simple and organized way, section by section

---

## Libraries Used

- [`requests`] – To make HTTP requests to the link provided by the user
- [`beautifulsoup4`] – To parse and extract HTML elements 
- [`urllib.parse`] – To handle URL joining and parsing to get domain of the website and visit all the subpages

---

## 📝 Why I Built This

I created this project to:

- Understand web scraping
- Practice how to scrape interlinks of the given website and avoiding revisiting the same pages
- Know how to represent raw data and pull out specific tags from HTML

This helped me gain hands-on experience with **web scraping, HTML parsing, and recursive crawling** using Python.

---

## How to Use

1. Install dependencies:
   ```bash
   poetry install
