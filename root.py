import streamlit as st
from H2 import run_H2
#from code2 import run_code2
#from code3 import run_code3

st.set_page_config(layout="wide")

st.sidebar.title("Select Tool")

choice = st.sidebar.radio(
    "Go to:",
    ["H2 - I v. A", "Code 2", "Code 3"]
)

if choice == "H2 - I v. A":
    run_H2()

#elif choice == "Code 2":
   # run_code2()

#elif choice == "Code 3":
    #run_code3()
#