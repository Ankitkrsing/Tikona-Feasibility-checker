import streamlit as st
import pandas as pd
from math import radians, sin, cos, atan2
from io import BytesIO
import re

# ---------------------------
# Helpers
# ---------------------------
def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (sin(dlat/2)**2) + (cos(lat1) * cos(lat2) * (sin(dlon/2)**2))
    c = 2 * atan2(a**0.5, (1-a)**0.5)
    return R * c

def to_numeric_series(series):
    return pd.to_numeric(series, errors="coerce")

def safe_suffix(name: str) -> str:
    s = re.sub(r"\s+", "_", str(name).strip())
    s = re.sub(r"[^0-9A-Za-z_]", "", s)
    return s

# ---------------------------
# App Config
# ---------------------------
st.set_page_config(page_title="Tikona Feasibility Checker", layout="wide")
st.title("📍 Tikona Feasibility Checker")

st.markdown(
    "Upload **Customer** and **BN/BTS** files, set RF/Fiber bandwidth & distance rules, "
    "Fiber min bandwidth & distance, and number of BTS/BN to include. Output = Results + Summary."
)

# ---------------------------
# Upload Customer File
# ---------------------------
customer_file = st.file_uploader("Upload Customer File (Excel/CSV)", type=["xlsx", "csv"])
customer_df = None
if customer_file:
    if customer_file.name.endswith(".xlsx"):
        xls = pd.ExcelFile(customer_file)
        cust_sheet = st.selectbox("Select Customer Sheet", xls.sheet_names, key="cust_sheet")
        customer_df = pd.read_excel(customer_file, sheet_name=cust_sheet)
    else:
        try:
            customer_df = pd.read_csv(customer_file)
        except UnicodeDecodeError:
            customer_df = pd.read_csv(customer_file, encoding="latin1")

    st.success("Customer file loaded")
    st.dataframe(customer_df.head())

# Customer column mapping
if isinstance(customer_df, pd.DataFrame) and not customer_df.empty:
    cust_lat_col = st.selectbox("Customer Latitude Column", customer_df.columns)
    cust_lon_col = st.selectbox("Customer Longitude Column", customer_df.columns)
    cust_bandwidth_col = st.selectbox("Customer Bandwidth Column", customer_df.columns)
    cust_output_cols = st.multiselect(
        "Customer Columns to include in Output",
        list(customer_df.columns),
        default=list(customer_df.columns)
    )

# ---------------------------
# Upload BN/BTS File
# ---------------------------
bn_file = st.file_uploader("Upload BN/BTS File (Excel/CSV)", type=["xlsx", "csv"])
bn_df = None
if bn_file:
    if bn_file.name.endswith(".xlsx"):
        xls_bn = pd.ExcelFile(bn_file)
        bn_sheet = st.selectbox("Select BN/BTS Sheet", xls_bn.sheet_names, key="bn_sheet")
        bn_df = pd.read_excel(bn_file, sheet_name=bn_sheet)
    else:
        try:
            bn_df = pd.read_csv(bn_file)
        except UnicodeDecodeError:
            bn_df = pd.read_csv(bn_file, encoding="latin1")

    st.success("BN/BTS file loaded")
    st.dataframe(bn_df.head())

# BN column mapping + detail selection
bn_lat_col = bn_lon_col = None
bn_detail_cols = []
if isinstance(bn_df, pd.DataFrame) and not bn_df.empty:
    bn_lat_col = st.selectbox("BN/BTS Latitude Column", bn_df.columns)
    bn_lon_col = st.selectbox("BN/BTS Longitude Column", bn_df.columns)
    candidates = [c for c in bn_df.columns if c not in {bn_lat_col, bn_lon_col}]
    bn_detail_cols = st.multiselect(
        "Select BN/BTS Detail Columns (optional)",
        candidates,
        default=["BN Name", "BN ID"] if "BN Name" in candidates and "BN ID" in candidates else []
    )

# ---------------------------
# User Parameters
# ---------------------------
if isinstance(customer_df, pd.DataFrame) and isinstance(bn_df, pd.DataFrame):
    col1, col2 = st.columns(2)
    with col1:
        y_bts = st.number_input("Max BTS per Customer (Y)", min_value=1, max_value=20, value=3, step=1)
    with col2:
        rf_min_bw = st.number_input("RF/Fiber Min Bandwidth (Mbps)", min_value=1, max_value=1000, value=50)
        rf_max_bw = st.number_input("RF/Fiber Max Bandwidth (Mbps)", min_value=1, max_value=1000, value=200)
        rf_dist_threshold = st.number_input("RF/Fiber Max Distance (km)", min_value=0.5, max_value=20.0, value=1.5, step=0.1)

        fiber_min_bw = st.number_input("Fiber Min Bandwidth (Mbps)", min_value=1, max_value=1000, value=201)
        fiber_dist_threshold = st.number_input("Fiber Max Distance (km)", min_value=0.5, max_value=50.0, value=5.0, step=0.1)

    start = st.button("🚀 Start Mapping")

    if start:
        bn_df[bn_lat_col] = to_numeric_series(bn_df[bn_lat_col])
        bn_df[bn_lon_col] = to_numeric_series(bn_df[bn_lon_col])

        rows = []
        total_customers = len(customer_df)
        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, cust in customer_df.iterrows():
            cust_lat = pd.to_numeric(cust[cust_lat_col], errors="coerce")
            cust_lon = pd.to_numeric(cust[cust_lon_col], errors="coerce")
            cust_bw = pd.to_numeric(cust[cust_bandwidth_col], errors="coerce")

            if pd.isna(cust_lat) or pd.isna(cust_lon):
                continue

            bn_valid = bn_df.dropna(subset=[bn_lat_col, bn_lon_col]).copy()
            bn_valid["Distance_km"] = bn_valid.apply(
                lambda r: haversine(cust_lat, cust_lon, r[bn_lat_col], r[bn_lon_col]),
                axis=1
            )

            nearby = bn_valid.sort_values("Distance_km").head(int(y_bts)).reset_index(drop=True)

            row = {col: cust[col] for col in cust_output_cols}

            for i, r in nearby.iterrows():
                prefix = "Closest_BTS" if i == 0 else f"BTS_{i+1}"
                row[f"{prefix}_Distance_km"] = round(float(r["Distance_km"]), 3)
                for detail in bn_detail_cols:
                    row[f"{prefix}_{safe_suffix(detail)}"] = r.get(detail, "")

            if not nearby.empty and not pd.isna(cust_bw):
                closest_dist = float(nearby.iloc[0]["Distance_km"])
                if rf_min_bw <= cust_bw <= rf_max_bw and closest_dist <= rf_dist_threshold:
                    row["Feasibility_Status"] = "RF/Fiber"
                elif cust_bw >= fiber_min_bw and closest_dist <= fiber_dist_threshold:
                    row["Feasibility_Status"] = "Fiber"
                else:
                    row["Feasibility_Status"] = "Not Feasible"
            else:
                row["Feasibility_Status"] = "Not Feasible"

            rows.append(row)

            progress = int((idx + 1) / total_customers * 100)
            progress_bar.progress(progress)
            status_text.text(f"Processing {idx+1}/{total_customers} customers...")

        if rows:
            result_df = pd.DataFrame(rows)
            st.success("✅ Mapping Completed")
            st.dataframe(result_df)

            # 📊 Summary Section
            st.subheader("📊 Summary")
            total_cases = len(result_df)
            st.write(f"**Total Cases:** {total_cases}")

            summary = result_df.groupby([cust_bandwidth_col, "Feasibility_Status"]).size().reset_index(name="Count")

            summary_pivot = summary.pivot_table(
                index=cust_bandwidth_col,
                columns="Feasibility_Status",
                values="Count",
                fill_value=0
            ).reset_index()

            # Fix Total column (only sum feasibility columns)
            feasibility_cols = [c for c in summary_pivot.columns if c != cust_bandwidth_col]
            summary_pivot["Total"] = summary_pivot[feasibility_cols].sum(axis=1)

            # Convert bandwidth column to string to allow "Grand Total"
            summary_pivot[cust_bandwidth_col] = summary_pivot[cust_bandwidth_col].astype(str)

            # Add Grand Total row
            grand_totals = {col: summary_pivot[col].sum() if col != cust_bandwidth_col else "Grand Total"
                            for col in summary_pivot.columns}
            summary_pivot = pd.concat([summary_pivot, pd.DataFrame([grand_totals])], ignore_index=True)

            st.write("**Bandwidth-wise Feasibility Summary:**")
            st.dataframe(summary_pivot)

            status_summary = result_df["Feasibility_Status"].value_counts().reset_index()
            status_summary.columns = ["Status", "Count"]
            st.write("**Overall Status Summary:**")
            st.dataframe(status_summary)

            # Download Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False, sheet_name="Results")
                summary_pivot.to_excel(writer, index=False, sheet_name="Bandwidth_Feasibility")
                status_summary.to_excel(writer, index=False, sheet_name="Status_Summary")

            st.download_button(
                label="📥 Download Results & Summary",
                data=output.getvalue(),
                file_name="tikona_feasibility_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
