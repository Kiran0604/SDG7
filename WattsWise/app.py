from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid
import math

app = Flask(__name__)

# Appliance wattage defaults (from calcy.py)
DEFAULT_APPLIANCES = {
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

# Placeholder for appliance data (in-memory storage for simplicity)
appliances = []

@app.route('/')
def index():
    return render_template('dashboard.html', appliances=appliances)

@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    name = request.form.get('name')
    power = request.form.get('power')
    hours = request.form.get('hours')
    appliance_id = str(uuid.uuid4())
    appliances.append({
        'id': appliance_id,
        'name': name,
        'power': power,
        'hours': hours
    })
    return jsonify({'id': appliance_id, 'name': name, 'power': power, 'hours': hours})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form.get('feedback')
    # Placeholder for storing feedback (e.g., save to database)
    print(feedback)
    return jsonify({'message': 'Feedback submitted successfully!'})

# Energy tips logic (from calcy.py)
def get_energy_tips(app):
    tips = []
    name = app["name"].lower()
    hours = app["hours"]
    watt = app["watt"]
    high_power = watt > 1000
    if name == "geyser":
        if hours > 0.5:
            tips.append("Reduce geyser usage to under 30 mins/day.")
        tips.append("Use a timer or smart plug to prevent overuse.")
        tips.append("Set thermostat to 50–55°C.")
        tips.append("👉 Example: Racold 5-Star 15L Storage Geyser (₹8,500)")
    elif name == "air conditioner":
        if hours > 4:
            tips.append("Try reducing A/C use by 1 hour/day or use sleep mode.")
        tips.append("Set thermostat to 24–25°C for optimal efficiency.")
        tips.append("Clean air filters every 2 weeks.")
        tips.append("Upgrade to a BEE 5-star inverter AC.")
        tips.append("👉 Example: LG 1.5 Ton 5-Star Inverter Split AC (₹45,000)")
    elif name == "refrigerator":
        tips.append("Keep fridge 2-3 inches from wall for ventilation.")
        tips.append("Avoid frequent door opening.")
        tips.append("👉 Example: Samsung 253L 3-Star Inverter (₹24,000)")
    elif name == "washing machine":
        tips.append("Wash only full loads or use eco/half-load mode.")
        tips.append("Use cold water cycles.")
        tips.append("👉 Example: Bosch 7kg Front Load 5-Star (₹28,000)")
    elif name == "microwave":
        tips.append("Avoid preheating unless necessary.")
        tips.append("Use auto-cook presets for optimized energy use.")
    elif name == "ceiling fan":
        tips.append("Clean blades for efficient airflow.")
        tips.append("Use BLDC fans for 65% savings.")
        tips.append("👉 Example: Atomberg Renesa BLDC Fan (₹3,000)")
    elif name == "led bulb" and watt > 20:
        tips.append("Switch to certified 9W LED bulbs.")
        tips.append("👉 Example: Philips 9W B22 LED Bulb (₹80)")
    elif name == "television":
        tips.append("Use low brightness mode and power off when not in use.")
    elif name == "computer":
        tips.append("Use energy saver/sleep mode.")
        tips.append("Switch off monitor if idle for long.")
    if high_power and name not in ["air conditioner", "geyser", "microwave"]:
        tips.append(f"Consider replacing {app['name']} with a more efficient model.")
    return tips

# Calculator route
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    results = None
    if request.method == 'POST':
        bill_amount = float(request.form.get('bill_amount', 0))
        price_per_unit = float(request.form.get('price_per_unit', 0))
        monthly_units = bill_amount / price_per_unit if price_per_unit else 0
        names = request.form.getlist('appliance_name[]')
        watts = request.form.getlist('appliance_watt[]')
        hours = request.form.getlist('appliance_hours[]')
        appliances = []
        for n, w, h in zip(names, watts, hours):
            if n and w and h:
                w = float(w)
                h = float(h)
                monthly_kwh = (w * h * 30) / 1000
                tips = get_energy_tips({"name": n, "watt": w, "hours": h})
                percent = (monthly_kwh / monthly_units * 100) if monthly_units else 0
                appliances.append({"name": n, "watt": w, "hours": h, "monthly_kwh": round(monthly_kwh,1), "tips": tips, "percent": round(percent,1)})
        total_appliance_kwh = sum(app["monthly_kwh"] for app in appliances)
        saving_kwh = total_appliance_kwh * 0.10
        saving_money = saving_kwh * price_per_unit
        results = {
            "monthly_units": round(monthly_units,1),
            "appliances": appliances,
            "saving_kwh": round(saving_kwh,1),
            "saving_money": round(saving_money,2),
            "annual_saving_kwh": round(saving_kwh*12,1),
            "annual_saving_money": round(saving_money*12,2)
        }
    return render_template('calculator.html', results=results)

# Graphs route
@app.route('/graphs')
def graphs():
    # Example data (can be replaced with user data)
    appliances = [
        {"name": "Refrigerator", "watt": 150, "hours": 24},
        {"name": "Air Conditioner", "watt": 1200, "hours": 4},
        {"name": "LED TV", "watt": 100, "hours": 5},
        {"name": "Ceiling Fan", "watt": 75, "hours": 10},
        {"name": "Washing Machine", "watt": 500, "hours": 1}
    ]
    bill_amount = 5000.0
    price_per_unit = 8.0
    total_units = bill_amount / price_per_unit
    monthly_kwh = [(a['watt']*a['hours']*30)/1000 for a in appliances]
    appliance_names = [a['name'] for a in appliances]
    total_appliance_kwh = sum(monthly_kwh)
    percent_appliance_bill = round((total_appliance_kwh/total_units)*100,2)
    reduced_kwh = [round(kwh*0.10,2) for kwh in monthly_kwh]
    monthly_savings_money = round(sum(reduced_kwh)*price_per_unit,2)
    yearly_savings_money = round(monthly_savings_money*12,2)
    total_savings_kwh_year = round(sum(reduced_kwh)*12,2)
    # Solar simulation
    surface_area = 100.0
    system_size_kw = round(surface_area/9,2)
    installation_cost = int(system_size_kw*50000)
    maintenance_cost_per_year = int(system_size_kw*2000)
    daily_solar_gen = system_size_kw*4.5
    monthly_solar_gen = daily_solar_gen*30
    yearly_solar_gen = daily_solar_gen*365
    yearly_solar_savings = int(yearly_solar_gen*price_per_unit)
    payback_years = round(installation_cost/(yearly_solar_savings-maintenance_cost_per_year),1) if yearly_solar_savings>maintenance_cost_per_year else float('inf')
    # Chart colors
    colors = ['#14b8a6','#fbbf24','#6366f1','#ef4444','#22c55e']
    graph_data = {
        'appliance_names': appliance_names,
        'monthly_kwh': monthly_kwh,
        'reduced_kwh': reduced_kwh,
        'colors': colors,
        'total_appliance_kwh': round(total_appliance_kwh,2),
        'total_units': round(total_units,2),
        'percent_appliance_bill': percent_appliance_bill,
        'monthly_savings_money': monthly_savings_money,
        'yearly_savings_money': yearly_savings_money,
        'total_savings_kwh_year': total_savings_kwh_year,
        'system_size_kw': system_size_kw,
        'installation_cost': installation_cost,
        'maintenance_cost_per_year': maintenance_cost_per_year,
        'yearly_solar_gen': int(yearly_solar_gen),
        'yearly_solar_savings': yearly_solar_savings,
        'payback_years': payback_years,
        'monthly_solar_gen': int(monthly_solar_gen)
    }
    return render_template('graphs.html', graph_data=graph_data)

# API endpoint for calculator
@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.json
    bill_amount = float(data.get('bill_amount', 0))
    price_per_unit = float(data.get('price_per_unit', 0))
    appliances = data.get('appliances', [])
    monthly_units = bill_amount / price_per_unit if price_per_unit else 0
    result_appliances = []
    for app in appliances:
        n = app.get('name')
        w = float(app.get('watt', 0))
        h = float(app.get('hours', 0))
        monthly_kwh = (w * h * 30) / 1000
        tips = get_energy_tips({"name": n, "watt": w, "hours": h})
        percent = (monthly_kwh / monthly_units * 100) if monthly_units else 0
        result_appliances.append({"name": n, "watt": w, "hours": h, "monthly_kwh": round(monthly_kwh,1), "tips": tips, "percent": round(percent,1)})
    total_appliance_kwh = sum(app["monthly_kwh"] for app in result_appliances)
    saving_kwh = total_appliance_kwh * 0.10
    saving_money = saving_kwh * price_per_unit
    results = {
        "monthly_units": round(monthly_units,1),
        "appliances": result_appliances,
        "saving_kwh": round(saving_kwh,1),
        "saving_money": round(saving_money,2),
        "annual_saving_kwh": round(saving_kwh*12,1),
        "annual_saving_money": round(saving_money*12,2)
    }
    return jsonify(results)

# API endpoint for graphs data
@app.route('/api/graphs-data', methods=['GET'])
def api_graphs_data():
    appliances = [
        {"name": "Refrigerator", "watt": 150, "hours": 24},
        {"name": "Air Conditioner", "watt": 1200, "hours": 4},
        {"name": "LED TV", "watt": 100, "hours": 5},
        {"name": "Ceiling Fan", "watt": 75, "hours": 10},
        {"name": "Washing Machine", "watt": 500, "hours": 1}
    ]
    bill_amount = 5000.0
    price_per_unit = 8.0
    total_units = bill_amount / price_per_unit
    monthly_kwh = [(a['watt']*a['hours']*30)/1000 for a in appliances]
    appliance_names = [a['name'] for a in appliances]
    total_appliance_kwh = sum(monthly_kwh)
    percent_appliance_bill = round((total_appliance_kwh/total_units)*100,2)
    reduced_kwh = [round(kwh*0.10,2) for kwh in monthly_kwh]
    monthly_savings_money = round(sum(reduced_kwh)*price_per_unit,2)
    yearly_savings_money = round(monthly_savings_money*12,2)
    total_savings_kwh_year = round(sum(reduced_kwh)*12,2)
    # Solar simulation
    surface_area = 100.0
    system_size_kw = round(surface_area/9,2)
    installation_cost = int(system_size_kw*50000)
    maintenance_cost_per_year = int(system_size_kw*2000)
    daily_solar_gen = system_size_kw*4.5
    monthly_solar_gen = daily_solar_gen*30
    yearly_solar_gen = daily_solar_gen*365
    yearly_solar_savings = int(yearly_solar_gen*price_per_unit)
    payback_years = round(installation_cost/(yearly_solar_savings-maintenance_cost_per_year),1) if yearly_solar_savings>maintenance_cost_per_year else float('inf')
    colors = ['#14b8a6','#fbbf24','#6366f1','#ef4444','#22c55e']
    graph_data = {
        'appliance_names': appliance_names,
        'monthly_kwh': monthly_kwh,
        'reduced_kwh': reduced_kwh,
        'colors': colors,
        'total_appliance_kwh': round(total_appliance_kwh,2),
        'total_units': round(total_units,2),
        'percent_appliance_bill': percent_appliance_bill,
        'monthly_savings_money': monthly_savings_money,
        'yearly_savings_money': yearly_savings_money,
        'total_savings_kwh_year': total_savings_kwh_year,
        'system_size_kw': system_size_kw,
        'installation_cost': installation_cost,
        'maintenance_cost_per_year': maintenance_cost_per_year,
        'yearly_solar_gen': int(yearly_solar_gen),
        'yearly_solar_savings': yearly_solar_savings,
        'payback_years': payback_years,
        'monthly_solar_gen': int(monthly_solar_gen)
    }
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)