import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("Competitor Price Monitoring Dashboard (Auto URL Mode)")

def extract_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Get all text from page
        text = soup.get_text()

        # Regex to find price patterns
        prices = re.findall(r"\$?\d+(?:\.\d{2})?", text)

        if prices:
            # Convert to float
            clean_prices = []
            for p in prices:
                p = p.replace("$", "")
                try:
                    clean_prices.append(float(p))
                except:
                    pass

            # Return smallest reasonable price
            return min(clean_prices)
        else:
            return None

    except:
        return None


st.subheader("Enter Product URLs")

your_url = st.text_input("Your Product URL")
comp1_url = st.text_input("Competitor 1 URL")
comp2_url = st.text_input("Competitor 2 URL")
comp3_url = st.text_input("Competitor 3 URL")

if st.button("Fetch & Compare Prices"):

    your_price = extract_price(your_url)
    comp1_price = extract_price(comp1_url)
    comp2_price = extract_price(comp2_url)
    comp3_price = extract_price(comp3_url)

    prices = [p for p in [your_price, comp1_price, comp2_price, comp3_price] if p]

    if not prices:
        st.error("No prices detected. Some websites may block scraping.")
    else:
        lowest_price = min(prices)
        highest_price = max(prices)

        st.subheader("Results")

        # Your Price Highlight
        if your_price == lowest_price:
            st.markdown(f"<h3 style='color:green;'>Your Price: ${your_price} (BEST PRICE)</h3>", unsafe_allow_html=True)
        elif your_price == highest_price:
            st.markdown(f"<h3 style='color:red;'>Your Price: ${your_price} (HIGHEST PRICE)</h3>", unsafe_allow_html=True)
        else:
            st.write(f"Your Price: ${your_price}")

        st.write(f"Competitor 1: ${comp1_price}")
        st.write(f"Competitor 2: ${comp2_price}")
        st.write(f"Competitor 3: ${comp3_price}")
