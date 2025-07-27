import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Energy Budgeting & Solar ROI Calculator")

# Predefined values (no user input required)
bill_amount = 5000.0  # ₹5000 monthly bill
price_per_unit = 8.0  # ₹8 per kWh
total_units = bill_amount / price_per_unit

# Step 1: Predefined Appliances
st.subheader("Appliance Energy Consumption")
appliances = [
    {"name": "Refrigerator", "watt": 150, "hours": 24},
    {"name": "Air Conditioner", "watt": 1200, "hours": 4},
    {"name": "LED TV", "watt": 100, "hours": 5},
    {"name": "Ceiling Fan", "watt": 75, "hours": 10},
    {"name": "Washing Machine", "watt": 500, "hours": 1}]

# Calculate and store appliance data
df_appliances = pd.DataFrame(appliances)
# Calculate monthly kWh for each appliance
df_appliances['monthly_kwh'] = (df_appliances['watt'] * df_appliances['hours'] * 30) / 1000
total_appliance_kwh = df_appliances['monthly_kwh'].sum()

# Visualizations for Appliances
if not df_appliances.empty:
    # Bar Chart: Appliance Consumption
    fig1 = px.bar(df_appliances, x='monthly_kwh', y='name', orientation='h',
                  title='Monthly Energy Consumption by Appliance',
                  labels={'monthly_kwh': 'Energy (kWh)', 'name': 'Appliance'})
    st.plotly_chart(fig1)

    # Pie Chart: Appliance Contribution
    fig2 = px.pie(df_appliances, values='monthly_kwh', names='name',
                  title='Appliance Contribution to Total Energy Consumption')
    st.plotly_chart(fig2)

    st.write(f"Total appliance estimated consumption: {total_appliance_kwh:.2f} kWh")
    st.write(f"Total monthly consumption: {total_units:.2f} kWh")
    st.write(f"Percentage of bill from appliances: {(total_appliance_kwh / total_units) * 100:.2f}%")

    # Savings from 10% Reduction
    st.subheader("Savings from 10% Usage Reduction")
    reduction_percent = 10
    df_appliances['reduced_kwh'] = df_appliances['monthly_kwh'] * (reduction_percent / 100)
    total_savings_kwh = df_appliances['reduced_kwh'].sum()
    monthly_savings_money = total_savings_kwh * price_per_unit
    yearly_savings_money = monthly_savings_money * 12

    # Grouped Bar Chart: Consumption vs. Savings
    fig3 = px.bar(df_appliances, x='name', y=['monthly_kwh', 'reduced_kwh'],
                  barmode='group', title='Energy Consumption vs. Savings (10% Reduction)',
                  labels={'value': 'Energy (kWh)', 'name': 'Appliance', 'variable': 'Category'})
    st.plotly_chart(fig3)

    st.write(f"Estimated monthly savings: ₹{monthly_savings_money:.2f}")
    st.write(f"Estimated yearly savings: ₹{yearly_savings_money:.2f} (~{total_savings_kwh * 12:.2f} kWh)")

# Step 2: Solar Simulation (with predefined values)
st.subheader("Solar Simulation")
surface_area = 100.0  # 100 sq.m rooftop
system_size_kw = round(surface_area / 9, 2)
installation_cost = system_size_kw * 50000
maintenance_cost_per_year = system_size_kw * 2000
daily_solar_gen = system_size_kw * 4.5
monthly_solar_gen = daily_solar_gen * 30
yearly_solar_gen = daily_solar_gen * 365
yearly_solar_savings = yearly_solar_gen * price_per_unit
payback_years = (installation_cost / (yearly_solar_savings - maintenance_cost_per_year)
                 if yearly_solar_savings > maintenance_cost_per_year else float('inf'))

# Solar Visualizations
st.write(f"Estimated solar system size: {system_size_kw} kW")
st.write(f"Solar installation cost: ₹{installation_cost:.2f}")
st.write(f"Annual maintenance cost: ₹{maintenance_cost_per_year:.2f}")
st.write(f"Yearly solar generation: {yearly_solar_gen:.2f} kWh")
st.write(f"Yearly savings: ₹{yearly_solar_savings:.2f}")

# Gauge for Payback Period
fig4 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=payback_years,
    title={'text': "Solar Payback Period (Years)"},
    gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "green"}}))
st.plotly_chart(fig4)

# Area Chart: Solar Generation vs. Consumption
df_comparison = pd.DataFrame({
    'Category': ['Total Consumption', 'Solar Generation'],
    'Energy (kWh)': [total_units, monthly_solar_gen]
})
fig5 = px.area(df_comparison, x='Category', y='Energy (kWh)',
               title='Monthly Energy Consumption vs. Solar Generation')
st.plotly_chart(fig5)

st.write("Thank you for using the calculator!")