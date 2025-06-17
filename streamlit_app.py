import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Analyzer", layout="wide")

st.title("📊 Enhanced Excel File Analysis App")

# Sidebar navigation
page = st.sidebar.radio("📁 Choose a page:", ["Data Explorer", "Dashboard"])

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")

    if page == "Data Explorer":
        # DATA EXPLORER PAGE
        st.header("🔍 Data Explorer")

        st.subheader("📄 Top 5 Rows")
        st.dataframe(df.head(), use_container_width=True)

        st.subheader("🧾 Column Names")
        st.write(df.columns.tolist())

        # Choose column to analyze
        column_to_analyze = st.selectbox("🔍 Select a column to analyze", df.columns)

        if column_to_analyze:
            st.subheader(f"📈 Analysis of '{column_to_analyze}'")

            if pd.api.types.is_numeric_dtype(df[column_to_analyze]):
                st.write("📊 Histogram (Distribution)")
                st.bar_chart(df[column_to_analyze].dropna().value_counts().sort_index())

                st.write("📉 Basic Statistics")
                st.write(df[column_to_analyze].describe())

            elif pd.api.types.is_object_dtype(df[column_to_analyze]) or pd.api.types.is_categorical_dtype(df[column_to_analyze]):
                st.write("📊 Bar Chart (Category Frequency)")

                value_counts = df[column_to_analyze].value_counts().reset_index()
                value_counts.columns = [column_to_analyze, "Count"]

                # Optional filtering (top N)
                top_n = st.slider("🔢 Show Top N categories", 1, min(20, len(value_counts)), 10)
                top_counts = value_counts.head(top_n)

                st.bar_chart(data=top_counts.set_index(column_to_analyze))

                st.write("🧾 Category Counts")
                st.dataframe(top_counts)

            else:
                st.warning("⚠️ Unsupported data type for this column.")

        # Summary for all numeric columns
        st.subheader("📊 Summary Statistics (All Numeric Columns)")
        st.write(df.describe())

    elif page == "Dashboard":
        # DASHBOARD PAGE
        st.header("📊 Dashboard Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("🧮 Rows", df.shape[0])
        col2.metric("📐 Columns", df.shape[1])
        col3.metric("🕳️ Missing Values", df.isnull().sum().sum())

        st.subheader("🧾 Null Values per Column")
        st.dataframe(df.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}))

        st.subheader("🔢 Top Numeric Columns (Preview)")
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            st.dataframe(df[num_cols].head())

        st.subheader("🔤 Top Categorical Columns (Preview)")
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if cat_cols:
            st.dataframe(df[cat_cols].head())

else:
    st.info("📂 Please upload an Excel file to begin.")
