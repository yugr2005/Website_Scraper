# Website Scraper

This is a Python application that scrapes a website and all its subpages using `requests`, `BeautifulSoup`, `xml.etree.ElementTree`, and `urllib.parse` and represents it's data in a clean and good way.

---

## What It Does

- You enter the URL of a website (for example, a blog homepage)
- Checks for a `sitemap.xml` file and parses it (if found) to extract all listed URLs `<loc>` for structured crawling
- Visits each url from the list, extracts the data using get function from <requests>, and then separate them out with the help of find_all function from <BeautifulSoup> on the basis of:
  - Main headings (`<h1>`)
  - Subheadings (`<h2>`, `<h3>`)
  - Paragraphs (`<p>`)
- - If a sitemap is not found, it falls back to crawling the root page and all internal links found through `<a>` tags recursively.
- Normalizes URLs (e.g: treats `https://example.com` and `https://example.com/` as the same) to avoid visiting duplicate links.
- Ensures pages are not revisited by maintaining a set of already visited normalized URLs.
- This method gets stop when the subpage has no other link (a-tag) to visit further or if the link is already visited before
- Displays the scraped content in a simple and organized way, section by section

---

## Libraries Used

- [`requests`] – To make HTTP requests to the link provided by the user
- [`beautifulsoup4`] – To parse and extract HTML elements 
- [`urllib.parse`] – To handle URL joining and parsing to get domain of the website and visit all the subpages
- [`xml.etree.ElementTree`] – To parse the `sitemap.xml` if it exists.

---

## Why I Built This

I created this project to:

- Deepen my understanding of web scraping.
- Learn how to crawl interlinked pages efficiently using sitemap-first crawling.
- Prevent redundant visits through proper URL normalization.
- Know how to represent raw data and pull out specific tags from HTML

---

## How to Use

1. Install dependencies:
   ```bash
   poetry install
