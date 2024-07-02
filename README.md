# Website Technology Analyzer

## Overview

The Website Technology Analyzer is a Streamlit-based application designed to analyze and extract the technology stack used by a website. The application scrapes the website, extracts meta information, and identifies technologies based on keywords and patterns in the page source. The results are displayed in a user-friendly format and can be downloaded as a markdown file.

## Features

- **Scraping websites:** Extracts meta information, scripts, stylesheets, and other resources from the website.
- **Identifying technologies:** Uses predefined keywords to detect various technologies and frameworks used by the website.
- **User-friendly interface:** Streamlit provides an easy-to-use interface for entering the URL and displaying results.
- **Downloadable results:** Users can download the analysis results in markdown format.

## Project Structure

project/
│
├── requirements.txt
├── README.md
└── src/
├── init.py
├── main.py
├── scraper.py
└── utils.py


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/website-technology-analyzer.git
    cd website-technology-analyzer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run src/main.py
    ```

2. Enter the website URL and the maximum number of pages to crawl.

3. Click on the "Analyze" button to start the analysis.

4. View the analysis results on the Streamlit interface.

5. Optionally, download the results as a markdown file.

## Libraries Used

- **requests:** For making HTTP requests to scrape website content.
- **BeautifulSoup:** For parsing HTML and extracting information.
- **re:** For regular expression operations used in technology identification.
- **urllib.parse:** For URL parsing and manipulation.
- **streamlit:** For creating the web application interface.
- **json:** For handling JSON data.

## Logic and Flow

1. **User Input:**
   - The user inputs a URL and the maximum number of pages to crawl.
   
2. **Scraping the Website:**
   - The `scrape_website` function makes an HTTP request to the provided URL.
   - The response is parsed using BeautifulSoup to extract the HTML content and headers.

3. **Extracting Information:**
   - **Meta Information:** Extracted using the `extract_meta_info` function which finds all meta tags and extracts their attributes.
   - **Scripts:** Extracted using the `extract_scripts_info` function which finds all script tags with a `src` attribute.
   - **Stylesheets:** Extracted using the `extract_stylesheets_info` function which finds all link tags with a `rel` attribute set to `stylesheet`.

4. **Identifying Technologies:**
   - The `identify_technologies` function searches the page source for predefined keywords to identify various technologies.
   - Additional checks are performed for specific technologies like WordPress, Elementor, React, Vue.js, etc.

5. **Crawling the Website:**
   - The `crawl_website` function manages the crawling process, visiting up to the specified maximum number of pages.
   - It keeps track of visited URLs and queues new URLs found on each page.

6. **Formatting Results:**
   - The `format_results` function formats the extracted information and identified technologies into a readable markdown format.

7. **Displaying and Downloading Results:**
   - The formatted results are displayed using Streamlit's markdown rendering.
   - Users can download the results as a markdown file using the download button.

## Example Output

Here's an example of what the analysis results might look like: