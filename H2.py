def run_H2():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    from io import StringIO

    st.set_page_config(layout="centered")
    st.title("H2")

    # -----------------------------
    # Upload multiple files
    # -----------------------------
    uploaded_files = st.file_uploader(
        "Upload one or more EC-Lab .txt files",
        type=["txt", "csv"],
        accept_multiple_files=True
    )

    if uploaded_files:

        all_curves = []

        for uploaded_file in uploaded_files:
            filename = os.path.splitext(uploaded_file.name)[0]

            text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            lines = text.splitlines()

            # Find header row
            header_idx = None
            for i, line in enumerate(lines):
                if line.lower().startswith("mode"):
                    header_idx = i
                    break

            if header_idx is None:
                st.warning(f"Skipping {filename}: no data header found.")
                continue

            data_str = "\n".join(lines[header_idx:])
            df = pd.read_csv(StringIO(data_str), sep="\t")

            if "time/s" not in df.columns or "I/mA" not in df.columns:
                st.warning(f"Skipping {filename}: required columns not found.")
                continue

            all_curves.append({
                "name": filename,
                "x": df["time/s"],
                "y": df["I/mA"],
            })

        if not all_curves:
            st.error("No valid files to plot.")
            st.stop()

        # -----------------------------
        # Sidebar controls
        # -----------------------------
        st.sidebar.header("Plot Controls")

        title = st.sidebar.text_input(
            "Plot title",
            value="I (mA) vs Time (s)"
        )

        show_legend = st.sidebar.checkbox("Show legend", value=True)

        # -----------------------------
        # Color pickers (one per file)
        # -----------------------------
        st.sidebar.subheader("Curve Colors")

        for curve in all_curves:
            default_color = "#1f77b4"  # matplotlib default blue
            curve["color"] = st.sidebar.color_picker(
                f"{curve['name']}",
                value=default_color,
                key=f"color_{curve['name']}"
            )

        # -----------------------------
        # Global bounds across all files
        # -----------------------------
        all_x = pd.concat([c["x"] for c in all_curves])
        all_y = pd.concat([c["y"] for c in all_curves])

        xmin, xmax = float(all_x.min()), float(all_x.max())
        ymin, ymax = float(all_y.min()), float(all_y.max())

        x_bounds = st.sidebar.slider(
            "X bounds (time, s)",
            min_value=xmin,
            max_value=xmax,
            value=(xmin, xmax)
        )

        y_bounds = st.sidebar.slider(
            "Y bounds (current, mA)",
            min_value=ymin,
            max_value=ymax,
            value=(ymin, ymax)
        )

        # -----------------------------
        # Plot
        # -----------------------------
        fig, ax = plt.subplots()

        for curve in all_curves:
            label = curve["name"] if show_legend else None
            ax.plot(
                curve["x"],
                curve["y"],
                label=label,
                color=curve["color"]
            )

        ax.set_title(title)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Current (mA)")
        ax.set_xlim(x_bounds)
        ax.set_ylim(y_bounds)

        if show_legend:
            ax.legend()

        st.pyplot(fig)

    else:
        st.info("Upload one or more files to plot.")
