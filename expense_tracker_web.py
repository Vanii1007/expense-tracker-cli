import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

st.title("💰 Expense Tracker")

# Load data
df = pd.read_csv("expenses.csv")

# Add new expense
st.subheader("➕ Add New Expense")
with st.form("expense_form"):
    date = st.date_input("Date", datetime.now())
    category = st.text_input("Category (e.g., Food, Transport)")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = {"date": date, "category": category, "amount": amount, "note": note}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("expenses.csv", index=False)
        st.success("Expense added successfully!")

# View expenses
st.subheader("📋 All Expenses")
st.dataframe(df)

# Summary
st.subheader("📊 Summary by Category")
summary = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
st.table(summary)

st.metric("💸 Total Spent", f"₹ {df['amount'].sum():,.2f}")
