import streamlit as st
from H2 import run_H2
from QM import run_QM
from line import run_line
from IGF import run_IGF
from ICP import run_ICP
from PDP import run_PDP

st.set_page_config(layout="wide")

st.sidebar.title("Select Tool")

choice = st.sidebar.radio(
    "Go to:",
    ["H2", "QM", "Custom Line Graph", "IGF", "ICP", "PDP"]
)

if choice == "H2":
    run_H2()

elif choice == "QM":
    run_QM()

elif choice == "Custom Line Graph":
    run_line()

elif choice == "IGF":
    run_IGF()

elif choice == "ICP":
    run_ICP()
#
elif choice == "PDP":
    run_PDP()