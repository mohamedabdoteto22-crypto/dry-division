import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

# إعدادات واجهة DRY_DIVISION
st.set_page_config(page_title="DRY_DIVISION", page_icon="⚡")

st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .stButton>button { width: 100%; background-color: #ffffff; color: #000000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("DRY_DIVISION ⚡")
st.subheader("M. ABDEL QADER PROTOCOLS")

menu = ["DASHBOARD", "LOG DATA", "PROGRESS"]
choice = st.sidebar.selectbox("MENU", menu)

if choice == "LOG DATA":
    weight = st.number_input("WEIGHT (KG)", value=95.0)
    cals = st.number_input("CALORIES", value=2000)
    if st.button("SAVE TO CLOUD"):
        with open("dry_log.csv", "a") as f:
            f.write(f"{date.today()},{weight},{cals}\n")
        st.success("DATA SECURED.")

elif choice == "PROGRESS":
    if os.path.exists("dry_log.csv"):
        df = pd.read_csv("dry_log.csv", names=["Date", "Weight", "Cals"])
        st.line_chart(df.set_index("Date")["Weight"])
    else:
        st.info("NO DATA YET.")
else:
    st.write("WELCOME TO THE DIVISION. STATUS: OPTIMIZED.")
