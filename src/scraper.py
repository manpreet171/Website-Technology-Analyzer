import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from utils import tech_stack, tech_keywords
import streamlit as st

def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser'), response.headers
    except requests.RequestException as e:
        st.error(f"Error scraping {url}: {str(e)}")
        return None, None

def extract_meta_info(soup):
    meta_info = {}
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if 'name' in tag.attrs and 'content' in tag.attrs:
            meta_info[tag.attrs['name']] = tag.attrs['content']
        elif 'property' in tag.attrs and 'content' in tag.attrs:
            meta_info[tag.attrs['property']] = tag.attrs['content']
    
    title_tag = soup.find('title')
    if title_tag:
        meta_info['title'] = title_tag.string

    return meta_info

def extract_scripts_info(soup):
    scripts_info = []
    scripts = soup.find_all('script')
    for script in scripts:
        if script.has_attr('src'):
            scripts_info.append(script['src'])
    return scripts_info

def extract_stylesheets_info(soup):
    stylesheets_info = []
    stylesheets = soup.find_all('link', rel='stylesheet')
    for stylesheet in stylesheets:
        if stylesheet.has_attr('href'):
            stylesheets_info.append(stylesheet['href'])
    return stylesheets_info

def identify_technologies(soup, url, response_headers):
    technologies = tech_stack.copy()
    page_source = str(soup).lower()

    for category, keywords in tech_keywords.items():
        for keyword in keywords:
            if keyword.lower() in page_source:
                version_match = re.search(rf'{re.escape(keyword)}[^\d]*(\d+(?:\.\d+)*)', page_source)
                if version_match:
                    technologies[category].append(f"{keyword}({version_match.group(1)})")
                else:
                    technologies[category].append(keyword)

    if 'wordpress' in page_source:
        technologies['Page builders'].append('WordPress')
    if 'elementor' in page_source:
        technologies['Page builders'].append('Elementor')

    if 'woocommerce' in page_source:
        technologies['Web frameworks'].append('WooCommerce')

    if 'shopify' in url:
        technologies['Web frameworks'].append('Shopify')

    if 'react' in page_source:
        technologies['JavaScript frameworks'].append('React')
    if 'vue' in page_source:
        technologies['JavaScript frameworks'].append('Vue.js')
    if 'angular' in page_source:
        technologies['JavaScript frameworks'].append('Angular')

    if 'fonts.googleapis.com' in page_source:
        technologies['Font scripts'].append('Google Fonts')

    if 'cloudflare' in response_headers.get('Server', '').lower():
        technologies['CDN'].append('Cloudflare')
    
    if 'cf-ray' in response_headers:
        technologies['Performance'].append('Cloudflare Rocket Loader')
    
    if 'google-analytics.com' in page_source:
        technologies['Analytics'].append('Google Analytics')
        if 'ga4' in page_source:
            technologies['Analytics'][-1] += '(GA4)'

    if 'googletagmanager.com' in page_source:
        technologies['Tag managers'].append('Google Tag Manager')

    if 'facebook.com/tr?' in page_source:
        technologies['Advertising'].append('Facebook Pixel')

    if 'cdn.jsdelivr.net' in page_source:
        technologies['CDN'].append('jsDelivr')

    if 'ajax.googleapis.com' in page_source:
        technologies['CDN'].append('Google CDN')

    if '/wp-content/' in page_source:
        technologies['Web frameworks'].append('WordPress')
    if '/sites/default/' in page_source:
        technologies['Web frameworks'].append('Drupal')
    if 'magento' in page_source:
        technologies['Web frameworks'].append('Magento')

    technologies = {k: list(set(v)) for k, v in technologies.items() if v}

    return technologies

def extract_info(soup, url, response_headers):
    info = {
        'meta': extract_meta_info(soup),
        'scripts': extract_scripts_info(soup),
        'stylesheets': extract_stylesheets_info(soup),
        'technologies': identify_technologies(soup, url, response_headers)
    }
    return info

def crawl_website(start_url, max_pages=10):
    visited = set()
    to_visit = [start_url]
    all_info = {}
    page_count = 0

    while to_visit and page_count < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        
        st.text(f"Crawling: {current_url}")
        soup, response_headers = scrape_website(current_url)
        if soup:
            info = extract_info(soup, current_url, response_headers)
            all_info[current_url] = info
            
            visited.add(current_url)
            page_count += 1
            
            for link in soup.find_all('a', href=True):
                new_url = urljoin(start_url, link['href'])
                if new_url.startswith(start_url) and new_url not in visited:
                    to_visit.append(new_url)
    
    return all_info

def format_results(all_info):
    formatted_output = ""
    for page_url, info in all_info.items():
        formatted_output += f"**Website : {page_url}**\n"
        formatted_output += "**Technology stack**\n"
        
        for category, technologies in info['technologies'].items():
            if technologies:
                formatted_output += f"{category}\n\n"
                for tech in technologies:
                    formatted_output += f"- {tech}\n"
                formatted_output += "\n"
        
        formatted_output += "**Metadata**\n\n"
        if 'title' in info['meta']:
            formatted_output += f"Title\n{info['meta']['title']}\n\n"
        elif 'og:title' in info['meta']:
            formatted_output += f"Title\n{info['meta']['og:title']}\n\n"
        if 'description' in info['meta']:
            formatted_output += f"Description\n{info['meta']['description']}\n\n"
        elif 'og:description' in info['meta']:
            formatted_output += f"Description\n{info['meta']['og:description']}\n\n"
        
        formatted_output += "---\n\n"
    
    return formatted_output
