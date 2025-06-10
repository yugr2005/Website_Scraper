import streamlit as st
from crawler import get_sitemap, parse_sitemap, crawl_sitemap_urls, crawl_page
from urllib.parse import urlparse


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
    # st.info(f"Max pages: {maxPages if maxPages != float("inf") else "all"}")

    with st.spinner("Crawling in progress..."):
        if method == "Sitemap-based":
            sitemap = get_sitemap(f"{scheme}://{domain}")

            if sitemap:
                urlList = parse_sitemap(sitemap)
                content = crawl_sitemap_urls(urlList, domain, maxPages)

            else:
                st.warning("Sitemap not found. Switching to manual crawl...")
                content = crawl_page(url, domain, set(), maxPages, [0])

        else:
            content = crawl_page(url, domain, set(), maxPages, [0])
            
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


