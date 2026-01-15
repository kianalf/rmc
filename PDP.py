def run_PDP():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from io import StringIO

    st.set_page_config(layout="wide")
    st.title("Potentiodynamic Polarization")

    # ---------------------------
    # File uploader (MULTIPLE)
    # ---------------------------
    uploaded_files = st.file_uploader(
        "Upload one or more EC-Lab ASCII files",
        type=["txt", "csv"],
        accept_multiple_files=True
    )

    @st.cache_data
    def load_file(file):
        raw = file.read().decode("latin1").splitlines()

        header_row = None
        for i, line in enumerate(raw):
            if line.lower().startswith("mode"):
                header_row = i
                break

        if header_row is None:
            return None

        data_text = "\n".join(raw[header_row:])
        df = pd.read_csv(StringIO(data_text), sep="\t")

        # Convert numeric columns
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df


    # ---------------------------
    # Load all files
    # ---------------------------
    datasets = {}

    if uploaded_files:
        for file in uploaded_files:
            df = load_file(file)
            if df is not None:
                datasets[file.name] = df
            else:
                st.warning(f"Could not parse {file.name}")

    if not datasets:
        st.info("Upload one or more files to begin.")
        st.stop()

    # ---------------------------
    # Column selection (GLOBAL)
    # ---------------------------
    all_columns = list(next(iter(datasets.values())).columns)

    default_x = "Ewe/V" if "Ewe/V" in all_columns else all_columns[0]
    default_y = "<I>/mA" if "<I>/mA in all_columns" else all_columns[1]

    st.sidebar.header("Plot Controls")

    x_col = st.sidebar.selectbox(
        "X Variable",
        all_columns,
        index=all_columns.index(default_x)
    )

    y_col = st.sidebar.selectbox(
        "Y Variable",
        all_columns,
        index=all_columns.index(default_y)
    )

    y2_col = st.sidebar.selectbox(
        "Y2 Variable (optional)",
        ["None"] + all_columns
    )

    log_x  = st.sidebar.checkbox("Log X axis", value=False)
    log_y  = st.sidebar.checkbox("Log Y axis", value=False)
    log_y2 = st.sidebar.checkbox("Log Y2 axis", value=False)

    # ---------------------------
    # Axis bounds + title
    # ---------------------------
    st.sidebar.subheader("Axis Bounds & Title")

    plot_title = st.sidebar.text_input(
        "Plot Title",
        value="Ewe/V vs log10(|I/mA|)"
    )

    x_min = st.sidebar.text_input("X min (blank = auto)", "")
    x_max = st.sidebar.text_input("X max (blank = auto)", "")
    y_min = st.sidebar.text_input("Y min (blank = auto)", "")
    y_max = st.sidebar.text_input("Y max (blank = auto)", "")

    def parse_bound(value):
        try:
            return float(value)
        except:
            return None


    x_min = parse_bound(x_min)
    x_max = parse_bound(x_max)
    y_min = parse_bound(y_min)
    y_max = parse_bound(y_max)

    # ---------------------------
    # Helper function
    # ---------------------------
    def prepare_y(series, colname):
        """
        Automatically apply log10(|I|) for current,
        otherwise return raw data.
        """
        if colname.lower().startswith("<i>") or "i" in colname.lower():
            return np.log10(np.abs(series)), f"log10(|{colname}|)"
        else:
            return series, colname


    def apply_bounds(ax):
        if x_min is not None or x_max is not None:
            ax.set_xlim(left=x_min, right=x_max)

        if y_min is not None or y_max is not None:
            ax.set_ylim(bottom=y_min, top=y_max)


    # ---------------------------
    # Tabs
    # ---------------------------
    tab_overlay, tab_individual = st.tabs(
        ["📊 Overlay All Files", "📁 Individual File Plots"]
    )

    # ==========================================================
    # TAB 1 — OVERLAY PLOT
    # ==========================================================
    with tab_overlay:
        st.subheader("Overlay Plot")

        fig, ax = plt.subplots(figsize=(11, 6))

        for name, df in datasets.items():
            x = df[x_col]
            y_raw = df[y_col]
            y, y_label = prepare_y(y_raw, y_col)

            ax.plot(x, y, label=name)

        ax.set_xlabel(x_col)
        ax.set_ylabel(y_label)
        ax.set_title(plot_title)
        ax.grid(True)

        if log_x:
            ax.set_xscale("log")
        if log_y:
            ax.set_yscale("log")

        apply_bounds(ax)

        # Optional Y2 overlay
        if y2_col != "None":
            ax2 = ax.twinx()
            for name, df in datasets.items():
                ax2.plot(df[x_col], df[y2_col], linestyle="--", alpha=0.7)
            ax2.set_ylabel(y2_col)
            if log_y2:
                ax2.set_yscale("log")

        ax.legend()
        st.pyplot(fig)


    # ==========================================================
    # TAB 2 — INDIVIDUAL PLOTS
    # ==========================================================
    with tab_individual:
        st.subheader("Individual File Plots")

        for name, df in datasets.items():
            st.markdown(f"### {name}")

            fig, ax = plt.subplots(figsize=(10, 5))

            x = df[x_col]
            y_raw = df[y_col]
            y, y_label = prepare_y(y_raw, y_col)

            ax.plot(x, y, label=y_label)

            ax.set_xlabel(x_col)
            ax.set_ylabel(y_label)
            ax.set_title(plot_title)
            ax.grid(True)

            if log_x:
                ax.set_xscale("log")
            if log_y:
                ax.set_yscale("log")

            apply_bounds(ax)

            # Optional Y2 per file
            if y2_col != "None":
                ax2 = ax.twinx()
                ax2.plot(x, df[y2_col], linestyle="--", label=y2_col)
                ax2.set_ylabel(y2_col)
                if log_y2:
                    ax2.set_yscale("log")

            ax.legend()
            st.pyplot(fig)

            with st.expander("Show data"):
                st.dataframe(df.head(300))
