import math

# Preset appliances with typical wattage (India-focused)
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

# Get numeric input with error handling
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# Advanced rule-based suggestion engine
def get_energy_tips(app):
    tips = []
    name = app["name"].lower()
    hours = app["hours"]
    watt = app["watt"]
    high_power = watt > 1000

    # Behavioral tips per appliance
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

    # Catch-all for custom or high-power appliances
    if high_power and name not in ["air conditioner", "geyser", "microwave"]:
        tips.append(f"Consider replacing {app['name']} with a more efficient model.")

    return tips

# Main budgeting calculator
def main():
    print("\n=== ⚡ Smart Energy Budgeting & Solar ROI Calculator ⚡ ===")

    # Basic inputs
    bill_amount = get_float("Enter monthly electricity bill (₹): ")
    price_per_unit = get_float("Enter price per unit (₹/kWh): ")
    monthly_units = bill_amount / price_per_unit
    print(f"\n📊 Estimated Monthly Consumption: {monthly_units:.1f} kWh")

    # Appliance inputs
    appliances = []
    print("\nChoose your major appliances. Type 'done' when finished.")
    while True:
        print("\nAvailable appliances:")
        for i, appliance in enumerate(DEFAULT_APPLIANCES.keys(), 1):
            print(f"{i}. {appliance}")
        choice = input("Enter appliance name or number (or 'done'): ").strip()
        if choice.lower() == 'done':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(DEFAULT_APPLIANCES):
            name = list(DEFAULT_APPLIANCES.keys())[int(choice) - 1]
            watt = DEFAULT_APPLIANCES[name]
        else:
            name = choice
            watt = get_float(f"Enter wattage for {name} in watts: ")

        hours = get_float(f"How many hours/day do you use {name}? ")
        monthly_kwh = (watt * hours * 30) / 1000
        appliances.append({"name": name, "watt": watt, "hours": hours, "monthly_kwh": monthly_kwh})

    total_appliance_kwh = sum(app["monthly_kwh"] for app in appliances)
    print(f"\n⚙️ Appliance Consumption Breakdown:")
    for app in appliances:
        percent = (app["monthly_kwh"] / monthly_units) * 100
        print(f" - {app['name']}: {app['monthly_kwh']:.1f} kWh/month ({percent:.1f}%)")

    # Recommendations and savings
    print("\n📋 Personalized Energy Saving Tips & Product Recommendations:")
    saving_kwh = 0
    saving_money = 0
    for app in appliances:
        tips = get_energy_tips(app)
        if tips:
            est_saving = app["monthly_kwh"] * 0.10  # 10% conservative estimate
            saving_kwh += est_saving
            saving_money += est_saving * price_per_unit
            print(f"\n🔌 {app['name']} ({app['monthly_kwh']:.1f} kWh/month):")
            for tip in tips:
                print(f"   - {tip}")

    print(f"\n💰 Estimated Monthly Savings: ₹{saving_money:.2f} (~{saving_kwh:.1f} kWh)")
    print(f"📆 Estimated Annual Savings: ₹{saving_money * 12:.2f} (~{saving_kwh * 12:.1f} kWh)")

    # Solar simulation
    solar_choice = input("\nDo you want to simulate solar panel installation? (yes/no): ").strip().lower()
    if solar_choice == "yes":
        area = get_float("Enter available rooftop area (sq. meters): ")
        kw_capacity = round(area / 9.0, 2)
        cost_per_kw = 50000  # ₹/kW
        maintenance_per_year = 2000  # ₹/kW/year

        total_install_cost = kw_capacity * cost_per_kw
        annual_maintenance = kw_capacity * maintenance_per_year
        annual_generation = kw_capacity * 4.5 * 365
        annual_savings = annual_generation * price_per_unit
        net_annual_profit = annual_savings - annual_maintenance
        payback_period = total_install_cost / net_annual_profit if net_annual_profit > 0 else float('inf')

        print("\n☀️ Solar Simulation Results:")
        print(f" - Estimated System Size: {kw_capacity:.2f} kW")
        print(f" - Installation Cost: ₹{total_install_cost:,.0f}")
        print(f" - Annual Generation: {annual_generation:.0f} kWh")
        print(f" - Annual Bill Reduction: ₹{annual_savings:.0f}")
        print(f" - Net Annual Savings (after maintenance): ₹{net_annual_profit:.0f}")
        print(f" - Payback Period: {payback_period:.1f} years")

    print("\n✅ Simulation Complete! Stay energy smart & eco-friendly! 🌱")

if __name__ == "__main__":
    main()
    
    
