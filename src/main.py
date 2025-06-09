import requests as re
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

def main():

    url = input("Enter URL here: ").strip()
    parsed = urlparse(url)
    domain = parsed.netloc      #gives just the domain of the link

    visited = set()     #To store visited links and avoid duplication through set

    sitemap = getSitemap(f"{parsed.scheme}://{domain}")
    
    #If the url has a sitemap
    if sitemap:
        print("\nSitemap XML Found!\n")

        urlList = parseSitemap(sitemap)     #get the list of urls from sitemap
        print(f"Total URLs found in sitemap: {len(urlList)}\n")

        for n in urlList:
            print(f"→ {n}")

        processSitemapUrls(urlList, domain, visited)    #crawls all pages of url and prints the content

    #if the url does not have a sitemap
    else:
        print("Starting manual crawl from the entered URL...")

        crawlPage(url, domain, visited)

def getSitemap(baseUrl):
    sitemapUrl = urljoin(baseUrl, '/sitemap.xml')       #URL of the sitemap  (baseUrl + /sitemap.xml)
    print(f"\nChecking for sitemap at: {sitemapUrl}")

    try:
        response = re.get(sitemapUrl)
        response.raise_for_status()
        return response.text
    
    except re.exceptions.RequestException as e:
        print(f"Error fetching sitemap {e}")
        return None
    
#Takes raw XML content from sitemap.xml and returns a list of all URLs found inside <loc> tags.
def parseSitemap(sitemap):   

    urlList = []

    try:
        root = ET.fromstring(sitemap)       #Parse the XML content into a tree structure

        for locTag in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):    #Loop through each <loc> tag in the document
            url = locTag.text.strip()   #gets the text from the <loc> and removes extra spaces

            urlList.append(url)     #adds the url into the list

        return urlList

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    
def processSitemapUrls(urlList, domain, visited):
    print(f"\nCrawling {len(urlList)} pages from sitemap...\n")

    for url in urlList:
        parsedUrl = urlparse(url)

        if parsedUrl.netloc != domain:
            continue  # Skip links outside the domain

        if url not in visited:
            crawlPage(url, domain, visited)

def normalizeUrl(url):
    parsed = urlparse(url)

    # Ensure consistent structure: scheme + netloc + path (with no trailing '/')
    normalized = parsed._replace(path=parsed.path.rstrip('/')).geturl()
    return normalized
    
def crawlPage(url, domain, visited):

    normalizedUrl = normalizeUrl(url)

    if normalizedUrl in visited:      #Checks if the url is already visited
        return
    
    visited.add(normalizedUrl)        #if not already visited then add to visited set

    print(f"\n📄Visiting: {normalizedUrl}")

    #Getting response from that url
    try:
        response = re.get(normalizedUrl)
        response.raise_for_status

    except re.exceptions.RequestException as e:
        print(e)

    #Coverting html into simple text format
    soup = BeautifulSoup(response.text, 'html.parser')      #parses html content into tree format

    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):

        if tag.name == 'h1':
            print(f"\n [Heading 1] {tag.get_text(strip=True)}\n")       #return data in text form

        elif tag.name == 'h2':
            print(f"\n [Heading 2] {tag.get_text(strip=True)}\n")

        elif tag.name == 'h3':
            print(f"    [Heading 3] {tag.get_text(strip=True)}\n")

        elif tag.name == 'p':
            print(f"  📌 [Paragraph] {tag.get_text(strip=True)}\n")

    print("=" * 120)

    for linkTag in soup.find_all('a'):      #finds all the <a> tags from the html
        href = linkTag.get('href')      #stores the href from all <a> tags
        if href is None or href.startswith('#'):
            continue        #skip empty or same-page links (#)

        fullUrl = urljoin(url, href)         #this will join our given url with the subpage url ("https://example.com/about")

        parsedUrl = urlparse(fullUrl)

        if parsedUrl.netloc != domain:      #Checks if the url we just formed is from the same domain or not
            continue

        crawlPage(fullUrl, domain, visited)

if __name__ == "__main__":
    main()

#optimized code by adding crawling through the sitemap and if not it crawls subpages manually