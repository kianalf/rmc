def run_IGF():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    from io import StringIO

    st.set_page_config(layout="centered")
    st.title("I (mA) vs Time (s) — Multi-File Plotter")
    print ("igf")