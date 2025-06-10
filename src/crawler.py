import requests as re
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

def get_sitemap(base_url):
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        response = re.get(sitemap_url)
        response.raise_for_status()
        return response.text
    except re.exceptions.RequestException:
        return None
    
def parse_sitemap(sitemap):
    url_list = []
    try:
        root = ET.fromstring(sitemap)
        for loc_tag in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = loc_tag.text.strip()
            url_list.append(url)
    except ET.ParseError:
        return []
    return url_list

def normalize_url(url):
    parsed = urlparse(url)
    return parsed._replace(path=parsed.path.rstrip('/')).geturl()

def crawl_sitemap_urls(url_list, domain, max_pages):
    visited = set()
    count = [0]
    all_content = []
    for url in url_list:
        if count[0] >= max_pages:
            break
        parsed = urlparse(url)
        if parsed.netloc != domain:
            continue
        content = crawl_page(url, domain, visited, max_pages, count)
        all_content.extend(content)
    return all_content

def crawl_page(url, domain, visited, max_pages, count):
    if count[0] >= max_pages:
        return []

    normalized_url = normalize_url(url)
    if normalized_url in visited:
        return []

    visited.add(normalized_url)
    count[0] += 1

    try:
        response = re.get(normalized_url)
        response.raise_for_status()
    except re.exceptions.RequestException:
        return []

    html = response.text
    page_content = extract_content_from_html(html)

    soup = BeautifulSoup(html, 'html.parser')
    for link_tag in soup.find_all('a'):
        if count[0] >= max_pages:
            break

        href = link_tag.get('href')
        if not href or href.startswith('#'):
            continue

        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        if parsed.netloc != domain:
            continue

        page_content.extend(crawl_page(full_url, domain, visited, max_pages, count))

    return page_content

def extract_content_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
        tag_type = tag.name
        text = tag.get_text(strip=True)
        content.append((tag_type, text))
    return content