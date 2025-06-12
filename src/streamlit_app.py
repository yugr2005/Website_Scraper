import streamlit as st
from crawler import get_sitemap, parse_sitemap, crawl_sitemap_urls, crawl_page
from urllib.parse import urlparse

#Function to update Progress Bar
def progress_callback(count, maxPages, progressBar):
    if isinstance(maxPages, int) and (maxPages > 0):
        progress = int((count[0] / maxPages) * 100)
        progressBar.progress(min(progress, 100))

# Set the page config (title, layout)
st.set_page_config(page_title="Web Crawler", layout="wide")

# --- Title Section ---
st.title("Website Content Crawler")
st.markdown("Enter a URL, choose crawl method, and fetch useful content from the web.")

# Input fields
url = st.text_input("Enter Website URL", placeholder = "https://example.com")
method = st.radio("Crawling Method", options = ["Sitemap-based", "Manual recursive"])
maxPages = st.text_input("Max Pages to Crawl and `all` to crawl whole website", placeholder = "e.g. 10 or all")

submit = st.button("Start Crawling")

if submit:
    if not url:
        print("Please enter url")
    else:
        parsed = urlparse(url)
        domain = parsed.netloc
        scheme = parsed.scheme

    if maxPages.lower() == "all":
        maxPages = float('inf')
    else:
        try:
            maxPages = int(maxPages)
        except ValueError:
            st.warning("Invalid max pages input. Defaulting to 10.")
            maxPages = 10
    
    st.success(f"Starting crawl on: {url}")
    st.info(f"Method: {method}, Max Pages: {maxPages if maxPages != float("inf") else "all"}")

    with st.spinner("Crawling in progress..."):

        count = [0]

        if method == "Sitemap-based":
            sitemap = get_sitemap(f"{scheme}://{domain}")

            if sitemap:
                urlList = parse_sitemap(sitemap)

                filteredUrls = [u for u in urlList if urlparse(u).netloc == domain]

                # Set true progress limit (for the bar)
                adjustedMax = min(len(filteredUrls), maxPages if isinstance(maxPages, int) else len(filteredUrls))

                # Set progress bar object
                progress_callback.progressBar = st.progress(0)
                content = crawl_sitemap_urls(filteredUrls, domain, adjustedMax, count, progress_callback=progress_callback)

            else:
                st.warning("Sitemap not found. Switching to manual crawl...")
                content = crawl_page(url, domain, set(), maxPages, count, progress_callback=progress_callback)

        else:
            adjustedMax = maxPages
            content = crawl_page(url, domain, set(), adjustedMax, count, progress_callback=progress_callback)
            
    for tag, text in content:
        if tag == 'h1':
            st.markdown(f"### {text}")
        elif tag == 'h2':
            st.markdown(f"#### {text}")
        elif tag == 'h3':
            st.markdown(f"##### {text}")
        elif tag == "p":
            st.markdown(f"📌 {text}")

    st.success("Crawling complete!")
    st.info(f"🔍 Total Pages Crawled: {count[0]}")



