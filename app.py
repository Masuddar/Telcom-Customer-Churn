import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Telco Customer Churn Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    
    # Convert TotalCharges to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    
    return df

df = load_data()

# Sidebar - Filters
st.sidebar.header("🔍 Filter Options")

# Churn filter
churn_filter = st.sidebar.radio("Filter by Churn Status:", ["All", "Yes", "No"], horizontal=True)
if churn_filter != "All":
    df = df[df["Churn"] == churn_filter]

# Monthly Charges filter
min_charge, max_charge = st.sidebar.slider(
    "Filter by Monthly Charges", float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max()), 
    (df["MonthlyCharges"].min(), df["MonthlyCharges"].max())
)
df = df[(df["MonthlyCharges"] >= min_charge) & (df["MonthlyCharges"] <= max_charge)]

# Sidebar - Project Details
st.sidebar.header("📌 Project Under:")
st.sidebar.markdown("### **Asit Barman**")
st.sidebar.markdown("#### Ph.D. in Technology")
st.sidebar.markdown("Assistant Professor at SIT, Siliguri")
st.sidebar.divider()
st.sidebar.header("📌 Student Details:")
st.sidebar.markdown("**Masuddar Rahaman**")
st.sidebar.markdown("*IT Department*")
st.sidebar.divider()

# UI Design - Main Page with CSS Styling
st.markdown("""
    <style>
        .css-18e3th9 {
            padding: 0rem;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
    <h1 style='text-align: center; color: #4A90E2;'>📊 Telco Customer Churn Analysis</h1>
    <hr style='border: 1px solid #4A90E2;'>
""", unsafe_allow_html=True)

# KPI Metrics
col1, col2, col3 = st.columns(3)
total_customers = len(df)
churn_rate = round((df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100), 2)
avg_tenure = round(df["tenure"].mean(), 2)

col1.metric("👥 Total Customers", total_customers)
col2.metric("📉 Churn Rate", f"{churn_rate}%", "Lower is better")
col3.metric("⏳ Average Tenure", f"{avg_tenure} months")

# Display dataset
st.write("### 📋 Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

# Visualization Row
st.write("### 🔍 Churn Analysis & Monthly Charges Distribution")
col1, col2 = st.columns(2)

# Churn Distribution Visualization
with col1:
    fig = px.histogram(df, x="Churn", color="Churn", barmode="group", title="Churn Distribution",
                       color_discrete_map={"Yes": "#FF6F61", "No": "#4A90E2"})
    st.plotly_chart(fig, use_container_width=True, key="churn_dist")

# Monthly Charges Distribution
with col2:
    fig = px.histogram(df, x="MonthlyCharges", nbins=30, title="Monthly Charges Distribution",
                       color_discrete_sequence=["#4A90E2"], marginal="box")
    st.plotly_chart(fig, use_container_width=True, key="monthly_charges")

# Heatmap & Additional Chart
st.write("### 📌 Correlation Heatmap & Additional Insights")
col1, col2 = st.columns([1, 1])  # Adjust column width ratio for better alignment

# Correlation Heatmap - Fixed for Numeric Columns Only
with col1:
    fig, ax = plt.subplots(figsize=(5,4))  # Reduced figure size for better layout
    numeric_df = df.select_dtypes(include=['number'])  # Select only numeric columns
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap", fontsize=12)
    st.pyplot(fig)

# Additional Plotly Chart
with col2:
    fig = px.box(df, x="Churn", y="TotalCharges", color="Churn", title="Total Charges Distribution by Churn",
                 color_discrete_map={"Yes": "#FF6F61", "No": "#4A90E2"})
    st.plotly_chart(fig, use_container_width=True, key="total_charges_boxplot")

# Additional Map Visualization at the Bottom
st.write("### 🌍 Customer Locations")
df_mock = pd.DataFrame({
    "Latitude": [22.5726, 28.7041, 19.0760, 13.0827, 23.2599],
    "Longitude": [88.3639, 77.1025, 72.8777, 80.2707, 77.4126],
    "City": ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bhopal"]
})
fig = px.scatter_mapbox(df_mock, lat="Latitude", lon="Longitude", text="City", zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig, use_container_width=True, key="customer_locations")

# Summary
st.write("### 📢 Key Takeaways")
st.markdown("""
✅ **Churn Rate:** Helps in understanding customer retention trends.  
✅ **Monthly Charges Insight:** Displays the distribution of customer billing amounts.  
✅ **Correlation Heatmap:** Identifies relationships between numeric variables.  
✅ **Total Charges Distribution:** Provides insights into billing patterns across churn groups.
""")

# Footer
st.markdown("""
    <hr style='border: 1px solid #4A90E2;'>
    <h4 style='text-align: center; color: #4A90E2;'>Developed by Masuddar Rahaman | IT Department</h4>
""", unsafe_allow_html=True)
