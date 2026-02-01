def run_line():
    import streamlit as st
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    st.set_page_config(page_title="Dual Y-Axis Line Plotter", layout="centered")
    st.title("📈 Dual Y-Axis Streamlit Line Plotter")

    # ------------------------
    # Data Inputs
    # ------------------------
    x_vals = st.text_input("X-axis values", "0,1,2,3,4")
    y1_vals = st.text_input("Y1 values (Left Axis)", "1,2,3,2,1")
    y2_vals = st.text_input("Y2 values (Right Axis)", "10,20,30,20,10")

    def parse_values(val):
        return [float(v.strip()) for v in val.split(",") if v.strip()]

    try:
        x = parse_values(x_vals)
        y1 = parse_values(y1_vals)
        y2 = parse_values(y2_vals)
    except ValueError:
        st.error("Please enter valid numeric values.")
        st.stop()

    # ------------------------
    # Labels
    # ------------------------
    title = st.text_input("Plot Title", "Dual Y-Axis Plot")
    x_label = st.text_input("X-axis Label", "X")
    y1_label = st.text_input("Y1 Axis Label (Left)", "Y1")
    y2_label = st.text_input("Y2 Axis Label (Right)", "Y2")

    line1_name = st.text_input("Line 1 Name (Y1)", "Line 1")
    line2_name = st.text_input("Line 2 Name (Y2)", "Line 2")

    # ------------------------
    # Styles
    # ------------------------
    marker_options = {
        "Circle": "circle",
        "Square": "square",
        "Triangle": "triangle-up",
        "Star": "star",
        "Diamond": "diamond"
    }

    line_styles = {
        "Solid": "solid",
        "Dashed": "dash",
        "Dotted": "dot",
        "Dash-dot": "dashdot"
    }

    col1, col2 = st.columns(2)

    with col1:
        marker1 = st.selectbox("Marker Shape (Y1)", marker_options.keys())
        color1 = st.color_picker("Line Color (Y1)", "#1f77b4")
        style1 = st.selectbox("Line Style (Y1)", line_styles.keys())

    with col2:
        marker2 = st.selectbox("Marker Shape (Y2)", marker_options.keys())
        color2 = st.color_picker("Line Color (Y2)", "#ff7f0e")
        style2 = st.selectbox("Line Style (Y2)", line_styles.keys())

    # ------------------------
    # Plot (CORRECT WAY)
    # ------------------------
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Line 1 → Left axis
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y1,
            name=line1_name,
            mode="lines+markers",
            marker=dict(symbol=marker_options[marker1]),
            line=dict(color=color1, dash=line_styles[style1])
        ),
        secondary_y=False
    )

    # Line 2 → Right axis
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y2,
            name=line2_name,
            mode="lines+markers",
            marker=dict(symbol=marker_options[marker2]),
            line=dict(color=color2, dash=line_styles[style2])
        ),
        secondary_y=True
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        legend_title="Legend",
        template="plotly_white"
    )

    fig.update_yaxes(title_text=y1_label, secondary_y=False)
    fig.update_yaxes(title_text=y2_label, secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
