import requests as re
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, urljoin

def main():

    url = input("Enter URL here: ").strip()

    parsed = urlparse(url)

    domain = parsed.netloc
    visited = set()
    
    crawlPage(url, domain, visited)

    print(f"\nTotal pages visited: {len(visited)}")

def crawlPage(url, domain, visited):

    if url in visited:      #Checks if the url is already visited
        return
    
    visited.add(url)        #if not already visited then add to visited set
    print(f"\n📄Visiting: {url}")

    #Getting response from that url
    try:
        response = re.get(url)
        response.raise_for_status

    except re.exceptions.RequestException as e:
        print(e)

    #Coverting html into simple text format
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)

    print("\nScrapped data from url: ", text[:300])

    print("=" * 120)

    for linkTag in soup.find_all('a'):
        href = linkTag.get('href')
        if href is None or href.startswith('#'):
            continue

        fullUrl = urljoin(url, href)

        parsedUrl = urlparse(fullUrl)

        if parsedUrl.netloc != domain:
            continue

        crawlPage(fullUrl, domain, visited)

    # url = input("Enter URL here: ").strip()
    # # print("You enetered: ", url)

    # try:
    #     response = re.get(url)
    #     print(response.raise_for_status)
    #     htmlContent = response.text        # Raw HTML of the page

    #     soup = BeautifulSoup(htmlContent, 'html.parser')    #parses html content into tree format

    #     pageText = soup.get_text(separator='\n', strip=True)    #return data in text form

    #     print("Scraped data: ", pageText)

    #     parsedBaseUrl = urlparse(url)
    #     domain = parsedBaseUrl.netloc       #gives just the domain of the link

    #     allLinks = set()        #To store links and avoid duplication through set

    #     for linkTag in soup.find_all('a'):      #finds all the <a> tags from the html
    #         href = linkTag.get('href')      #stores the href from all <a> tags

    #         if href is None or href.startswith('#'):
    #             continue        # skip empty or same-page links (#)

    #         fullUrl = urljoin(url, href)        #this will join our given url with the subpage url ("https://example.com/about")

    #         parsedUrl = urlparse(fullUrl)

    #         if parsedUrl.netloc == domain:      #Checks if the url we just formed is from the same domain or not 
    #             allLinks.add(fullUrl)       #Add to the set

    #     print("All links:")
    #     for link in allLinks:
    #         print(link)

    # except re.exceptions.RequestException as e:
    #     print(e)


if __name__ == "__main__":
    main()
