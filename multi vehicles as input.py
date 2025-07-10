import streamlit as st
import pandas as pd
import plotly.express as px

# ——— Page config —————————————————————————————
st.set_page_config(
    page_title="Vehicle Fuel Efficiency Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 KMPL vs Estimated Fuel Consumed Explorer")
st.markdown(
    """
    Select one or more **Vehicle Numbers** to see how their fuel consumption 
    (Est_fuel_Consumed) varies with kilometers‑per‑liter (Last_Tnx_Kmpl).
    """
)

# ——— Load & clean data ——————————————————————————
@st.cache_data
def load_data(path="task1.xlsx"):
    df = pd.read_excel(path)
    df["Est_fuel_Consumed"] = pd.to_numeric(df["Est_fuel_Consumed"], errors="coerce")
    df["Last_Tnx_Kmpl"] = pd.to_numeric(df["Last_Tnx_Kmpl"], errors="coerce")
    df = df.dropna(subset=["Vehicle_no", "Est_fuel_Consumed", "Last_Tnx_Kmpl"])
    df["Vehicle_no"] = df["Vehicle_no"].str.upper().str.strip()
    if "Created_date" in df.columns:
        df["Created_date"] = pd.to_datetime(df["Created_date"], errors="coerce")
    return df

df = load_data()

# ——— Sidebar input ————————————————————————————
vehicle_options = sorted(df["Vehicle_no"].unique())
selected_vehicles = st.multiselect("Select Vehicle Numbers", vehicle_options)

# ——— Plotting ———————————————————————————————
if selected_vehicles:
    vdf = df[df["Vehicle_no"].isin(selected_vehicles)]

    if vdf.empty:
        st.error("No records found for the selected vehicles.")
    else:
        if "Created_date" in vdf.columns:
            vdf = vdf.sort_values(["Vehicle_no", "Created_date"])

        fig = px.line(
            vdf,
            x="Last_Tnx_Kmpl",
            y="Est_fuel_Consumed",
            color="Vehicle_no",
            markers=True,
            title="KMPL vs Estimated Fuel Consumed for Selected Vehicles",
            labels={
                "Last_Tnx_Kmpl": "Last Transaction (KMPL)",
                "Est_fuel_Consumed": "Estimated Fuel Consumed",
                "Vehicle_no": "Vehicle Number"
            },
            hover_data={
                "Last_Tnx_Kmpl": ":.2f",
                "Est_fuel_Consumed": ":.2f"
            }
        )
        fig.update_layout(
            hovermode="closest",
            margin=dict(l=40, r=40, t=80, b=40),
            legend_title_text="Vehicle"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Underlying Data")
        st.dataframe(
            vdf[["Vehicle_no", "Last_Tnx_Kmpl", "Est_fuel_Consumed", "Created_date"]]
            .reset_index(drop=True)
        )
else:
    st.info("🔎 Select one or more vehicle numbers from the sidebar to get started.")
