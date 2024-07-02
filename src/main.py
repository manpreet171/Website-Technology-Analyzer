
### src/main.py


import streamlit as st
from scraper import crawl_website, format_results

def main():
    st.title("Website Technology Analyzer")
    
    url = st.text_input("Enter website URL:")
    max_pages = st.number_input("Maximum number of pages to crawl:", min_value=1, max_value=100, value=1)
    
    if st.button("Analyze"):
        if not url.startswith('http'):
            url = 'https://' + url
        
        with st.spinner("Analyzing website..."):
            all_info = crawl_website(url, max_pages)
        
        st.success("Analysis complete!")
        
        formatted_results = format_results(all_info)
        st.markdown(formatted_results)
        
        st.download_button(
            label="Download Results",
            data=formatted_results,
            file_name="website_analysis.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
