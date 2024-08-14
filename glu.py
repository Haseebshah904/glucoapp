import streamlit as st
import anthropic

# Set your API key here
API_KEY = st.secerts["claude_api_key"]

# Function to generate a message prompt for Claude AI
def generate_meal_plan_request(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference):
    return f"""
    Please create a personalized meal plan for me based on the following information:
    - Fasting Sugar Level: {fasting_sugar} mg/dL
    - Pre-Meal Sugar Level: {pre_meal_sugar} mg/dL
    - Post-Meal Sugar Level: {post_meal_sugar} mg/dL
    - Dietary Preference: {dietary_preference}
    
    Consider my blood sugar levels and dietary preference to create a meal plan that helps manage my condition.
    """

# Function to get a response from Claude AI
def get_claude_response(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference):
    client = anthropic.Anthropic(api_key=api_key)

    # Generate the meal plan request message
    meal_plan_request = generate_meal_plan_request(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference)

    # Use Claude AI to get the response
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0,
        system="You are a world-class nutritionist. who specializes in diabetes management.",
        messages=[
            {
                "role": "user",
                "content": meal_plan_request
            }
        ]
    )
    
    raw_content=message.content
    itinerary=raw_content[0].text
    return itinerary

# Streamlit App
st.title("GlucoGuide: Personalized Meal Plans for Diabetic Patients")
st.write("Enter your blood sugar levels and dietary preferences to receive a personalized meal plan.")

# Sidebar for user input
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0)

dietary_preference = st.sidebar.selectbox(
    "Dietary Preference",
    ("No Preference", "Vegetarian", "Vegan", "Low Carb", "High Protein")
)

if st.sidebar.button("Generate Meal Plan"):
    # Pass the API key to the function
    meal_plan_response = get_claude_response(API_KEY, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference)
    st.write("## Your Personalized Meal Plan")
    st.write(meal_plan_response)
