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

def filter_foods(df, preference, cholesterol_level='Normal', sugar_level='Normal'):
    filtered = df.copy()
    if preference.lower() == 'veg':
        filtered = filtered[filtered['type'] == 'veg']
    elif preference.lower() == 'non-veg':
        filtered = filtered[(filtered['type'] == 'veg') | (filtered['type'] == 'non-veg')]
    if cholesterol_level == 'High':
        filtered = filtered[filtered['is_high_fat'] == False]
    if sugar_level == 'High (Type 1/2)':
        filtered = filtered[filtered['is_high_sugar'] == False]
    return filtered

def generate_diet_plan(df_foods, target_calories, macros, max_attempts=1000, max_items_per_meal=3):
    plan = {'breakfast': [], 'lunch': [], 'dinner': [], 'snack': []}
    plan_summary = {'total_calories': 0, 'total_protein_g': 0, 'total_carbs_g': 0, 'total_fat_g': 0}
    meal_categories = ['breakfast', 'lunch', 'dinner', 'snack']
    meal_dist = {'breakfast': 0.25, 'lunch': 0.35, 'dinner': 0.30, 'snack': 0.10}
    
    def add_food_to_plan(meal_type, food_item):
        plan[meal_type].append(food_item)
        plan_summary['total_calories'] += food_item['calories']
        plan_summary['total_protein_g'] += food_item['protein']
        plan_summary['total_carbs_g'] += food_item['carbs']
        plan_summary['total_fat_g'] += food_item['fat']

    for meal_type in meal_categories:
        target_meal_calories = target_calories * meal_dist[meal_type]
        current_meal_calories = 0
        selected_items = []
        available_foods = df_foods[df_foods['category'] == meal_type].to_dict('records')
        if not available_foods: continue

        attempts = 0
        while current_meal_calories < target_meal_calories * 0.9 and attempts < max_attempts and len(selected_items) < max_items_per_meal:
            chosen_food = random.choice(available_foods)
            if chosen_food not in selected_items:
                if current_meal_calories + chosen_food['calories'] < target_meal_calories * 1.5:
                    add_food_to_plan(meal_type, chosen_food)
                    current_meal_calories += chosen_food['calories']
                    selected_items.append(chosen_food)
            attempts += 1
    return plan, plan_summary

# --- 2. FULL DATASET (50+ ITEMS) ---
food_data = [
    {'name': 'Poha with Peanuts', 'calories': 250, 'protein': 5, 'carbs': 45, 'fat': 8, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Moong Dal Chilla', 'calories': 180, 'protein': 12, 'carbs': 25, 'fat': 4, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Greek Yogurt with Honey', 'calories': 120, 'protein': 15, 'carbs': 12, 'fat': 0.5, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': True},
    {'name': 'Egg Bhurji (2 eggs)', 'calories': 200, 'protein': 14, 'carbs': 4, 'fat': 15, 'type': 'non-veg', 'category': 'breakfast', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Idli (2 pcs) with Sambar', 'calories': 160, 'protein': 6, 'carbs': 30, 'fat': 2, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Upma', 'calories': 220, 'protein': 6, 'carbs': 35, 'fat': 6, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Aloo Paratha with Curd', 'calories': 350, 'protein': 9, 'carbs': 50, 'fat': 12, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Vegetable Omelette', 'calories': 220, 'protein': 16, 'carbs': 5, 'fat': 14, 'type': 'non-veg', 'category': 'breakfast', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Masala Dosa', 'calories': 300, 'protein': 5, 'carbs': 55, 'fat': 8, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Paneer Paratha', 'calories': 320, 'protein': 14, 'carbs': 40, 'fat': 12, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Oats Upma', 'calories': 190, 'protein': 7, 'carbs': 30, 'fat': 4, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Boiled Eggs (2)', 'calories': 140, 'protein': 12, 'carbs': 1, 'fat': 10, 'type': 'non-veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Dhokla (3 pcs)', 'calories': 150, 'protein': 6, 'carbs': 28, 'fat': 3, 'type': 'veg', 'category': 'breakfast', 'is_high_fat': False, 'is_high_sugar': True},
    {'name': 'Dal Tadka (1 bowl)', 'calories': 180, 'protein': 10, 'carbs': 25, 'fat': 5, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Chicken Curry', 'calories': 320, 'protein': 25, 'carbs': 8, 'fat': 18, 'type': 'non-veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Paneer Bhurji', 'calories': 300, 'protein': 18, 'carbs': 10, 'fat': 22, 'type': 'veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Mixed Veg Sabzi', 'calories': 150, 'protein': 4, 'carbs': 20, 'fat': 7, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Brown Rice (1 cup)', 'calories': 210, 'protein': 5, 'carbs': 45, 'fat': 2, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Chana Masala', 'calories': 260, 'protein': 12, 'carbs': 40, 'fat': 6, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Fish Fry', 'calories': 280, 'protein': 22, 'carbs': 5, 'fat': 18, 'type': 'non-veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Palak Dal', 'calories': 160, 'protein': 9, 'carbs': 22, 'fat': 4, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Rajma (1 cup)', 'calories': 240, 'protein': 14, 'carbs': 38, 'fat': 5, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Jeera Rice', 'calories': 220, 'protein': 4, 'carbs': 48, 'fat': 3, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Bhindi Masala', 'calories': 140, 'protein': 3, 'carbs': 15, 'fat': 8, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Egg Curry', 'calories': 250, 'protein': 14, 'carbs': 10, 'fat': 16, 'type': 'non-veg', 'category': 'lunch', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Soya Chunks Curry', 'calories': 220, 'protein': 20, 'carbs': 15, 'fat': 6, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Curd Rice', 'calories': 250, 'protein': 8, 'carbs': 40, 'fat': 6, 'type': 'veg', 'category': 'lunch', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Grilled Fish Tikka', 'calories': 250, 'protein': 30, 'carbs': 5, 'fat': 12, 'type': 'non-veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Palak Paneer', 'calories': 280, 'protein': 15, 'carbs': 12, 'fat': 20, 'type': 'veg', 'category': 'dinner', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Whole Wheat Roti', 'calories': 85, 'protein': 3, 'carbs': 18, 'fat': 0.5, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Chicken Stir-fry', 'calories': 280, 'protein': 28, 'carbs': 10, 'fat': 12, 'type': 'non-veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Vegetable Pulao', 'calories': 270, 'protein': 7, 'carbs': 45, 'fat': 7, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Baingan Bharta', 'calories': 160, 'protein': 4, 'carbs': 18, 'fat': 9, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Lauki Ki Sabzi', 'calories': 100, 'protein': 2, 'carbs': 12, 'fat': 5, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Tandoori Chicken', 'calories': 260, 'protein': 30, 'carbs': 4, 'fat': 14, 'type': 'non-veg', 'category': 'dinner', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Moong Dal (Yellow)', 'calories': 150, 'protein': 9, 'carbs': 24, 'fat': 3, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Mushroom Matar', 'calories': 180, 'protein': 8, 'carbs': 15, 'fat': 10, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Methi Thepla (2 pcs)', 'calories': 200, 'protein': 6, 'carbs': 35, 'fat': 5, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Pumpkin Sabzi', 'calories': 120, 'protein': 2, 'carbs': 15, 'fat': 6, 'type': 'veg', 'category': 'dinner', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Roasted Makhana', 'calories': 110, 'protein': 3, 'carbs': 20, 'fat': 2, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Boiled Chana Chat', 'calories': 150, 'protein': 8, 'carbs': 22, 'fat': 3, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Handful of Walnuts', 'calories': 180, 'protein': 4, 'carbs': 4, 'fat': 18, 'type': 'veg', 'category': 'snack', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Buttermilk', 'calories': 40, 'protein': 2, 'carbs': 4, 'fat': 1, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Mixed Fruit Salad', 'calories': 100, 'protein': 1, 'carbs': 25, 'fat': 0.5, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': True},
    {'name': 'Sprout Salad', 'calories': 80, 'protein': 6, 'carbs': 15, 'fat': 1, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Tea (Less Sugar)', 'calories': 60, 'protein': 1, 'carbs': 10, 'fat': 2, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Peanut Butter on Toast', 'calories': 190, 'protein': 8, 'carbs': 20, 'fat': 10, 'type': 'veg', 'category': 'snack', 'is_high_fat': True, 'is_high_sugar': False},
    {'name': 'Roasted Almonds (10)', 'calories': 70, 'protein': 3, 'carbs': 3, 'fat': 6, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Green Tea', 'calories': 2, 'protein': 0, 'carbs': 0.5, 'fat': 0, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Popcorn (Plain)', 'calories': 100, 'protein': 3, 'carbs': 20, 'fat': 1, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': False},
    {'name': 'Apple with Cinnamon', 'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'type': 'veg', 'category': 'snack', 'is_high_fat': False, 'is_high_sugar': True},
    {'name': 'Paneer Tikka (2 pcs)', 'calories': 150, 'protein': 10, 'carbs': 4, 'fat': 10, 'type': 'veg', 'category': 'snack', 'is_high_fat': True, 'is_high_sugar': False}
]
df_foods = pd.DataFrame(food_data)

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="NutriPlan AI", layout="wide")
st.title("🌿 NutriPlan AI: Weekly Indian Diet Planner")

with st.sidebar:
    age = st.slider("Age", 10, 100, 25)
    gender = st.radio("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 250, 175)
    activity = st.selectbox("Activity Level", ["sedentary", "light", "moderate", "active"])
    pref = st.selectbox("Preference", ["veg", "non-veg"])
    goal = st.selectbox("Goal", ["loss", "maintenance", "gain"])
    cholesterol = st.selectbox("Cholesterol", ["Normal", "High"])
    sugar = st.selectbox("Sugar Level", ["Normal", "High (Type 1/2)"])

if st.button("✨ Generate My Weekly Plan"):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)
    target_cal = calculate_target_calories(tdee, goal)
    macros = calculate_macro_targets(target_cal)

    st.markdown("### 📅 Your Weekly Meal Schedule")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tabs = st.tabs(days)
    
    for i, day in enumerate(days):
        with tabs[i]:
            filtered_df = filter_foods(df_foods, pref, cholesterol, sugar)
            daily_plan, _ = generate_diet_plan(filtered_df, target_cal, macros)
            for cat in ['breakfast', 'lunch', 'dinner', 'snack']:
                st.info(f"**{cat.capitalize()}**")
                if daily_plan[cat]:
                    for item in daily_plan[cat]:
                        st.write(f"🔹 {item['name']} ({item['calories']} kcal)")
                else:
                    st.write("No matches found for this meal type.")
