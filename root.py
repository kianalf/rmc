import streamlit as st
from H2 import run_H2
from IGF import run_IGF
from ICP import run_ICP
from PDP import run_PDP

st.set_page_config(layout="wide")

st.sidebar.title("Select Tool")

choice = st.sidebar.radio(
    "Go to:",
    ["H2", "IGF", "ICP", "PDP"]
)

if choice == "H2":
    run_H2()

elif choice == "IGF":
    run_IGF()

elif choice == "ICP":
    run_ICP()
#
elif choice == "PDP":
    run_PDP()