import streamlit as st
import pandas as pd
from pathlib import Path
import requests
from bs4 import BeautifulSoup
st.set_page_config(page_title='Web Data Collector',page_icon='🕸️',layout='wide')
st.title('🕸️ Web Scraping and Data Collector')
st.caption('Scrape a permitted page, inspect results, and export a dataset.')
base=Path(__file__).parent; sample=pd.read_csv(base/'data/sample_products.csv')
url=st.text_input('Public page URL',placeholder='https://example.com')
if st.button('Fetch page',type='primary'):
    if not url.startswith(('http://','https://')): st.error('Enter a valid http or https URL.')
    else:
        try:
            response=requests.get(url,headers={'User-Agent':'CodeAlphaLearningBot/1.0'},timeout=15); response.raise_for_status()
            soup=BeautifulSoup(response.text,'html.parser')
            records=[{'title':x.get_text(' ',strip=True),'tag':x.name,'link':x.get('href','')} for x in soup.select('h1,h2,h3,a') if x.get_text(strip=True)]
            result=pd.DataFrame(records).drop_duplicates()
            if result.empty: st.warning('No headings or links found. Try another permitted page.')
            else:
                st.dataframe(result,use_container_width=True); st.download_button('Download scraped CSV',result.to_csv(index=False).encode(),file_name='scraped_page.csv',mime='text/csv')
        except requests.RequestException as e: st.error(f'Request failed: {e}')
st.subheader('Included sample dataset (100 rows)'); st.dataframe(sample,use_container_width=True)
st.download_button('Download sample products CSV',sample.to_csv(index=False).encode(),file_name='sample_products.csv',mime='text/csv')
st.info('Only scrape pages you are allowed to access. Respect website terms, robots.txt, rate limits and privacy rules. This demo extracts visible headings and links, not hidden or protected data.')
