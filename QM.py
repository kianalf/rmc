def run_QM():

    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from io import StringIO

    st.set_page_config(layout="centered")
    st.title("QM")

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
            filename = uploaded_file.name

            # Decode file text
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
        # Color pickers (safe keys)
        # -----------------------------
        st.sidebar.subheader("Curve Colors")

        for i, curve in enumerate(all_curves):
            curve["color"] = st.sidebar.color_picker(
                f"{curve['name']}",
                value="#1f77b4",
                key=f"color_{i}"
            )

        # -----------------------------
        # Global bounds across all files
        # -----------------------------
        all_x = pd.concat([c["x"] for c in all_curves])
        all_y = pd.concat([c["y"] for c in all_curves])

        xmin, xmax = float(all_x.min()), float(all_x.max())
        ymin, ymax = float(all_y.min()), float(all_y.max())

        # Prevent slider crash if min == max
        if xmin == xmax:
            xmax = xmin + 1e-6
        if ymin == ymax:
            ymax = ymin + 1e-6

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

        # -----------------------------
        # Charge + M calculation
        # -----------------------------
        st.subheader("Integrated Charge and M Calculation")

        F = 96485        # C/mol
        MW_H2 = 2.02     # g/mol
        n = 2            # electrons

        for curve in all_curves:
            x = curve["x"].values
            y_mA = curve["y"].values

            # Area under curve relative to y = 0
            Q_mC = abs(np.trapezoid(y_mA, x))    # mA·s = mC (signed)
            Q_C  = Q_mC * 0.001           # convert mC → C

            # M calculation
            M = ((Q_C * MW_H2)*1000) / (n * F)

            st.write(
                f"**{curve['name']}**  \n"
                f"Q = {Q_C:.4f} mC  \n"
                f"M = {M:.4f}"
            )

    else:
        st.info("Upload one or more files to plot.")
