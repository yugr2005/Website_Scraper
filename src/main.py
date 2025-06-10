import requests as re
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

def main():

    url = input("Enter URL here: ").strip()
    parsed = urlparse(url)
    domain = parsed.netloc      #gives just the domain of the link

    visited = set()     #To store visited links and avoid duplication through set

    #Giver user a choice 
    print("\nChoose crawling method:")

    print("1. Sitemap-based crawling")
    print("2. Manual recursive crawling")

    choice = input("\nEnter 1 or 2: ").strip()

    count = [0]     #Counter to track how many pages have been crawled

    #Ask for max pages to crawl
    user_input = input("\nEnter the maximum number of pages to crawl (or 'all' to crawl the entire website): ").strip()

    #crawl whole website
    if user_input.lower() == 'all':
        maxPages = float('inf')
    
    else:
        try:
            maxPages = int(user_input)
        except ValueError:
            print("Invalid number. Defaulting to 10 pages.")
            maxPages = 10

    if choice == "1":
        sitemap = getSitemap(f"{parsed.scheme}://{domain}")
        
        #If the url has a sitemap
        if sitemap:
            print("\nSitemap XML Found!\n")

            urlList = parseSitemap(sitemap)     #get the list of urls from sitemap
            print(f"Total URLs found in sitemap: {len(urlList)}\n")

            # for n in urlList:
            #     print(f"→ {n}")

            processSitemapUrls(urlList, domain, visited, maxPages, count)    #crawls all pages of url and prints the content

        #if the url does not have a sitemap
        else:
            print("Sitemap not found. Switching to manual crawl...\n")

            crawlPage(url, domain, visited, maxPages, count)

    elif choice == "2":
        print("\nStarting manual crawl from the entered URL...")
        crawlPage(url, domain, visited, maxPages, count)

    else:
        print("Invalid choice.")

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
    
def processSitemapUrls(urlList, domain, visited, maxPages, count):
    print(f"\nCrawling {maxPages if maxPages != float('inf') else 'all'} pages from sitemap...\n")
    #ternary operator: <value_if_true> if <condition> else <value_if_false>

    for url in urlList:
        if count[0] >= maxPages:
            print("\nReached max page limit. Stopping crawl.")
            return
        
        parsedUrl = urlparse(url)

        if parsedUrl.netloc != domain:
            continue  # Skip links outside the domain

        if url not in visited:
            crawlPage(url, domain, visited, maxPages, count)

def normalizeUrl(url):
    parsed = urlparse(url)

    # Ensure consistent structure: scheme + netloc + path (with no trailing '/')
    normalized = parsed._replace(path=parsed.path.rstrip('/')).geturl()
    return normalized
    
def crawlPage(url, domain, visited, maxPages, count):

    if count[0] >= maxPages:
        return

    normalizedUrl = normalizeUrl(url)

    if normalizedUrl in visited:      #Checks if the url is already visited
        return
    
    visited.add(normalizedUrl)        #if not already visited then add to visited set

    count[0] += 1

    print(f"\n📄Visiting {count[0]}: {normalizedUrl}")

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

        if count[0] >= maxPages:
            return
        
        href = linkTag.get('href')      #stores the href from all <a> tags
        if href is None or href.startswith('#'):
            continue        #skip empty or same-page links (#)

        fullUrl = urljoin(url, href)         #this will join our given url with the subpage url ("https://example.com/about")

        parsedUrl = urlparse(fullUrl)

        if parsedUrl.netloc != domain:      #Checks if the url we just formed is from the same domain or not
            continue

        crawlPage(fullUrl, domain, visited, maxPages, count)

if __name__ == "__main__":
    main()
