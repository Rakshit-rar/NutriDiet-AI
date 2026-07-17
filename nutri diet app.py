import streamlit as st
import pandas as pd
import random

# --- 1. CORE LOGIC FUNCTIONS ---
def calculate_bmi(weight, height):
    return round(weight / ((height/100)**2), 2)

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity):
    factors = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'extra_active': 1.9}
    return round(bmr * factors.get(activity, 1.2), 2)

def calculate_target_calories(tdee, goal):
    if goal == 'loss': return tdee - 500
    if goal == 'gain': return tdee + 500
    return tdee

def calculate_macro_targets(target_calories):
    return {
        'protein_g': round((target_calories * 0.25) / 4, 1),
        'carbs_g': round((target_calories * 0.50) / 4, 1),
        'fat_g': round((target_calories * 0.25) / 9, 1)
    }

def filter_foods(df, preference, cholesterol_level, sugar_level):
    filtered = df.copy()
    if preference.lower() == 'veg':
        filtered = filtered[filtered['type'] == 'veg']
    if cholesterol_level == 'High':
        filtered = filtered[filtered['is_high_fat'] == False]
    if sugar_level == 'High (Type 1/2)':
        filtered = filtered[filtered['is_high_sugar'] == False]
    return filtered

def generate_weekly_plan(df, target_cal, max_items=2):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_plan = {}
    dist = {'breakfast': 0.25, 'lunch': 0.35, 'dinner': 0.30, 'snack': 0.10}
    
    for day in days:
        day_meals = {}
        for cat, perc in dist.items():
            cat_df = df[df['category'] == cat]
            if not cat_df.empty:
                # Generate a varied selection for each day
                sample = cat_df.sample(n=min(max_items, len(cat_df)))
                day_meals[cat] = sample.to_dict('records')
            else:
                day_meals[cat] = []
        weekly_plan[day] = day_meals
    return weekly_plan

# --- 2. DATASET ---
food_data = [
    {'name': 'Poha with Peanuts', 'calories': 250, 'protein': 5, 'carbs': 45, 'fat': 8, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Moong Dal Chilla', 'calories': 180, 'protein': 12, 'carbs': 25, 'fat': 4, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Greek Yogurt', 'calories': 120, 'protein': 15, 'carbs': 12, 'fat': 0.5, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': True},
    {'name': 'Egg Bhurji', 'calories': 200, 'protein': 14, 'carbs': 4, 'fat': 15, 'type': 'non-veg', 'category': 'breakfast', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Dal Tadka & Roti', 'calories': 280, 'protein': 12, 'carbs': 40, 'fat': 8, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Chicken Curry', 'calories': 320, 'protein': 25, 'carbs': 8, 'fat': 18, 'type': 'non-veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Paneer Bhurji', 'calories': 300, 'protein': 18, 'carbs': 10, 'fat': 22, 'type': 'veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Mixed Veg Sabzi', 'calories': 150, 'protein': 4, 'carbs': 20, 'fat': 7, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Rajma Masala', 'calories': 250, 'protein': 14, 'carbs': 35, 'fat': 6, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Palak Paneer', 'calories': 280, 'protein': 15, 'carbs': 12, 'fat': 20, 'type': 'veg', 'category': 'dinner', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Roasted Makhana', 'calories': 110, 'protein': 3, 'carbs': 20, 'fat': 2, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Buttermilk', 'calories': 40, 'protein': 2, 'carbs': 4, 'fat': 1, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False}
]
df_foods = pd.DataFrame(food_data)

# --- 3. STREAMLIT UI (MODERN STANDARDS) ---
st.set_page_config(page_title="NutriPlan AI", layout="wide")

# Custom CSS for modern look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #0056b3; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 NutriPlan AI: Weekly Indian Diet Planner")
st.markdown("Your personalized health journey, optimized by AI.")
st.markdown("--- ")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3565/3565418.png", width=100)
    st.header("👤 Profile Settings")
    age = st.slider("Age", 10, 100, 25)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 250, 175)
    activity = st.selectbox("Activity Level", ["sedentary", "light", "moderate", "active"])
    pref = st.selectbox("Dietary Preference", ["veg", "non-veg"])
    goal = st.select_slider("Goal", options=["loss", "maintenance", "gain"])

    st.header("🏥 Medical Factors")
    cholesterol = st.selectbox("Cholesterol", ["Normal", "High"])
    sugar = st.selectbox("Sugar Level", ["Normal", "High (Type 1/2)"])

if st.button("✨ Generate My Weekly Plan"):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)
    target_cal = calculate_target_calories(tdee, goal)
    macros = calculate_macro_targets(target_cal)

    # Dashboard Header
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Target Calories", f"{int(target_cal)} kcal")
    with col2: st.metric("Protein", f"{macros['protein_g']}g")
    with col3: st.metric("Carbs", f"{macros['carbs_g']}g")
    with col4: st.metric("Fats", f"{macros['fat_g']}g")

    st.markdown("### 📅 Your Weekly Meal Schedule")
    
    filtered_df = filter_foods(df_foods, pref, cholesterol, sugar)
    weekly_plan = generate_weekly_plan(filtered_df, target_cal)

    # Tabs for 7 Days
    tabs = st.tabs(list(weekly_plan.keys()))
    
    for i, (day, meals) in enumerate(weekly_plan.items()):
        with tabs[i]:
            st.subheader(f"🍴 {day} Menu")
            m_col1, m_col2 = st.columns(2)
            
            categories = list(meals.keys())
            for j, cat in enumerate(categories):
                target_col = m_col1 if j < 2 else m_col2
                with target_col:
                    st.info(f"**{cat.capitalize()}**")
                    if meals[cat]:
                        for item in meals[cat]:
                            st.write(f"🔹 {item['name']} ({item['calories']} kcal)")
                    else:
                        st.write("No items match your criteria.")
    
    st.success("Your personalized weekly plan is ready!")
