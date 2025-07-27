import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:5000"  # Change if Flask runs elsewhere

st.set_page_config(page_title="WattsWise", layout="wide", page_icon="⚡")

DEFAULT_APPLIANCES = [
    "Air Conditioner", "Geyser", "Refrigerator", "Washing Machine", "Microwave",
    "Ceiling Fan", "LED Bulb", "Television", "Computer"
]
APPLIANCE_WATTAGE = {
    "Air Conditioner": 1500,
    "Geyser": 2000,
    "Refrigerator": 150,
    "Washing Machine": 500,
    "Microwave": 1200,
    "Ceiling Fan": 75,
    "LED Bulb": 10,
    "Television": 120,
    "Computer": 200
}

# Session state for input persistence
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = {
        'bill_amount': 2000.0,
        'price_per_unit': 8.0,
        'appliance_data': []
    }

menu = st.sidebar.radio("Navigation", ["Home", "Calculator", "Graphs", "Solar Simulation"])

if menu == "Home":
    st.title("⚡ WattsWise: Smart Energy Dashboard")
    st.header("Welcome to WattsWise!")
    st.markdown("""
    **WattsWise** helps you:
    - Track and analyze your home energy usage
    - Get personalized energy-saving tips
    - Visualize your appliance consumption
    - Simulate solar installation and ROI
    
    Enter your details below to get started. Your input will be used across all features.
    """)
    with st.form("home_input_form"):
        bill_amount = st.number_input("Monthly Bill (₹)", min_value=0.0, value=st.session_state['user_input']['bill_amount'])
        price_per_unit = st.number_input("Price per Unit (₹/kWh)", min_value=0.0, value=st.session_state['user_input']['price_per_unit'])
        st.markdown("#### Appliances (up to 10)")
        appliance_data = []
        for i in range(1, 11):
            cols = st.columns(3)
            name = cols[0].selectbox(f"Name {i}", ["Select..."] + DEFAULT_APPLIANCES, key=f"home_name_{i}")
            if name != "Select...":
                default_watt = APPLIANCE_WATTAGE.get(name, 0)
            else:
                default_watt = 0
            watt = cols[1].number_input(f"Watt {i}", min_value=0.0, value=float(default_watt), key=f"home_watt_{i}")
            hours = cols[2].number_input(f"Hours/day {i}", min_value=0.0, key=f"home_hours_{i}")
            if name != "Select..." and watt and hours:
                appliance_data.append({"name": name, "watt": watt, "hours": hours})
        submitted = st.form_submit_button("Save Input")
    if submitted:
        st.session_state['user_input'] = {
            'bill_amount': bill_amount,
            'price_per_unit': price_per_unit,
            'appliance_data': appliance_data
        }
        st.success("Input saved! Now use the menu to explore Calculator, Graphs, or Solar Simulation.")

# Use saved input for all other pages
user_input = st.session_state['user_input']
bill_amount = user_input['bill_amount']
price_per_unit = user_input['price_per_unit']
appliance_data = user_input['appliance_data']

if menu == "Calculator":
    st.title("Calculator")
    if not appliance_data:
        st.warning("Please enter your details on the Home page first.")
    else:
        with st.spinner("Calculating..."):
            resp_calc = requests.post(f"{API_URL}/api/calculate", json={
                "bill_amount": bill_amount,
                "price_per_unit": price_per_unit,
                "appliances": appliance_data
            })
            if resp_calc.ok:
                results = resp_calc.json()
                st.subheader("Calculator Results")
                st.success(f"Estimated Monthly Consumption: {results['monthly_units']} kWh")
                for app in results['appliances']:
                    st.markdown(f"**{app['name']}**: {app['monthly_kwh']} kWh/month ({app['percent']}%)")
                    for tip in app['tips']:
                        st.write(f"- {tip}")
                st.info(f"Estimated Monthly Savings: ₹{results['saving_money']} (~{results['saving_kwh']} kWh)")
                st.info(f"Estimated Annual Savings: ₹{results['annual_saving_money']} (~{results['annual_saving_kwh']} kWh)")
            else:
                st.error("Calculation failed. Please check your input.")

if menu == "Graphs":
    st.title("Graphs & Energy Visualizations")
    if not appliance_data:
        st.warning("Please enter your details on the Home page first.")
    else:
        monthly_kwh = [(a['watt']*a['hours']*30)/1000 for a in appliance_data]
        appliance_names = [a['name'] for a in appliance_data]
        reduced_kwh = [round(kwh*0.10,2) for kwh in monthly_kwh]
        df = pd.DataFrame({
            'Appliance': appliance_names,
            'Monthly kWh': monthly_kwh,
            '10% Savings': reduced_kwh
        })
        st.markdown("**Monthly Energy Consumption by Appliance**")
        st.plotly_chart(px.bar(df, x='Monthly kWh', y='Appliance', orientation='h', color='Appliance'))
        st.markdown("**Appliance Contribution to Total Energy Consumption**")
        st.plotly_chart(px.pie(df, values='Monthly kWh', names='Appliance'))
        st.markdown("**Energy Consumption vs. Savings (10% Reduction)**")
        st.plotly_chart(px.bar(df, x='Appliance', y=['Monthly kWh', '10% Savings'], barmode='group'))

if menu == "Solar Simulation":
    st.title("Solar Simulation & Comparison")
    if not appliance_data:
        st.warning("Please enter your details on the Home page first.")
    else:
        monthly_kwh = [(a['watt']*a['hours']*30)/1000 for a in appliance_data]
        total_appliance_kwh = sum(monthly_kwh)
        total_units = bill_amount / price_per_unit if price_per_unit else 0
        surface_area = st.number_input("Available Rooftop Area (sq. meters)", min_value=0.0, value=100.0)
        system_size_kw = round(surface_area/9,2)
        installation_cost = int(system_size_kw*50000)
        maintenance_cost_per_year = int(system_size_kw*2000)
        daily_solar_gen = system_size_kw*4.5
        monthly_solar_gen = daily_solar_gen*30
        yearly_solar_gen = daily_solar_gen*365
        yearly_solar_savings = int(yearly_solar_gen*price_per_unit)
        payback_years = round(installation_cost/(yearly_solar_savings-maintenance_cost_per_year),1) if yearly_solar_savings>maintenance_cost_per_year else float('inf')
        st.write(f"Estimated solar system size: {system_size_kw} kW")
        st.write(f"Solar installation cost: ₹{installation_cost}")
        st.write(f"Annual maintenance cost: ₹{maintenance_cost_per_year}")
        st.write(f"Yearly solar generation: {yearly_solar_gen} kWh")
        st.write(f"Yearly savings: ₹{yearly_solar_savings}")
        st.write(f"Solar payback period: {payback_years} years")
        # Graph: Solar Generation vs. Consumption
        df_comp = pd.DataFrame({
            'Category': ['Total Consumption', 'Solar Generation'],
            'Energy (kWh)': [total_appliance_kwh, monthly_solar_gen]
        })
        st.markdown("**Monthly Energy Consumption vs. Solar Generation**")
        st.plotly_chart(px.bar(df_comp, x='Category', y='Energy (kWh)', color='Category', barmode='group'))
        # Graph: Payback period gauge
        st.markdown("**Solar Payback Period (Years)**")
        st.plotly_chart(px.bar(pd.DataFrame({'Payback Years': [payback_years]}), y='Payback Years', color_discrete_sequence=['#22c55e']))
