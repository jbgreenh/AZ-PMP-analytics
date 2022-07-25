import streamlit as st
import csv

conversion_factors = {}

with open('data/conversion_factors.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    conversion_factors = {row[0]: row[1] for row in reader}

st.write(
    """
    # MME Calculator
    *Please select an opioid in the sidebar and fill in the strength, quantity, and days supply fields*
    """)

opioid = st.sidebar.selectbox(
    'Select an opioid',
    conversion_factors.keys())

cf = conversion_factors[opioid]
st.sidebar.write(f'`{opioid}` conversion factor: **{cf}**')

strength = float(st.sidebar.text_input('Strength/Unit', 50))
quantity = float(st.sidebar.text_input('Quantity', 30))
days_supply = float(st.sidebar.text_input('Days Supply', 30))
if cf == 'N/A':
    mme = 'N/A'
else:
    mme = strength * (quantity / days_supply) * float(cf)


f'### MME: {mme}'


