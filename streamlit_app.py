import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set page config
st.set_page_config(page_title="Daily Sales Dashboard", layout="centered")

# Title
st.title("📊 Daily Sales Dashboard")

# Read Excel file
try:
    df = pd.read_excel("sales_data.xlsx")
except FileNotFoundError:
    st.error("❌ sales_data.xlsx not found. Submit some data first using the form.")
    st.stop()

# Format and sort data
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Show table
st.subheader("📋 Sales Data")
st.dataframe(df)

# Sales Trend Line Chart
st.subheader("📈 Sales Trend")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["Date"], df["Sales Amount"], marker='o', linestyle='-')
ax.set_xlabel("Date")
ax.set_ylabel("Sales Amount (₹)")
ax.set_title("Sales Over Time")
ax.grid(True)
st.pyplot(fig)

# Compare Today vs Yesterday
st.subheader("📅 Comparison")
if len(df) >= 2:
    today_sales = df["Sales Amount"].iloc[-1]
    yesterday_sales = df["Sales Amount"].iloc[-2]
    diff = today_sales - yesterday_sales
    percent = (diff / yesterday_sales) * 100 if yesterday_sales != 0 else 0

    st.metric(
        label="Today vs Yesterday",
        value=f"₹{today_sales:.2f}",
        delta=f"{diff:+.2f} ({percent:+.2f}%)"
    )
elif len(df) == 1:
    st.info("Only one entry available. Submit more data to compare.")
else:
    st.warning("No data available yet.")

# Optional note insights
if "Notes" in df.columns and df["Notes"].notnull().any():
    st.subheader("📝 Notes Summary")
    notes = df["Notes"].dropna().value_counts().head(5)
    st.write(notes)

# Footer
st.markdown("---")
st.caption("🔄 Data auto-refreshed from Excel file: `sales_data.xlsx`")
