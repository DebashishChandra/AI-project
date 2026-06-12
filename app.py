import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide"
)

@st.cache_data
def load_dataset():

    df = pd.read_csv(
        "Diseases_and_Symptoms.csv"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df

df_symptoms = load_dataset()

def calculate_bmi(weight, height):

    if height <= 0:
        return 0

    return round(
        weight / (height * height),
        2
    )


def predict_disease(selected_symptoms):

    if df_symptoms.empty:
        return "Dataset not loaded."

    if len(selected_symptoms) == 0:
        return "Please select symptoms."

    disease_scores = {}

    for _, row in df_symptoms.iterrows():

        disease = row["diseases"]

        score = 0

        for symptom in selected_symptoms:

            if symptom in df_symptoms.columns:

                try:

                    if int(row[symptom]) == 1:
                        score += 1

                except:
                    pass

        if disease not in disease_scores:

            disease_scores[disease] = score

        else:

            disease_scores[disease] = max(
                disease_scores[disease],
                score
            )

    result = sorted(
        disease_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    output = ""

    for disease, score in result[:5]:

        if score > 0:

            output += f"• {disease.title()}\n"

    if output == "":
        return "No disease matched."

    return output

def diet_plan(goal):

    if goal == "Weight Loss":

        return """
Breakfast: Oats + Fruits

Lunch: Vegetables + Rice

Dinner: Salad

Drink More Water
"""

    elif goal == "Weight Gain":

        return """
Breakfast: Eggs + Milk

Lunch: Rice + Chicken

Dinner: Paneer

Healthy Snacks
"""

    else:

        return """
Balanced Diet

Vegetables

Fruits

Protein

Water
"""
def exercise_plan(goal):

    if goal == "Weight Loss":

        return """
Running

Cycling

Skipping
"""

    elif goal == "Weight Gain":

        return """
Pushups

Squats

Weight Training
"""

    else:

        return """
Walking

Yoga

Stretching
"""

HISTORY_FILE = "history.csv"

def save_history(name, record):

    if not name:
        return

    if os.path.exists(HISTORY_FILE):

        df = pd.read_csv(
            HISTORY_FILE
        )

    else:

        df = pd.DataFrame(
            columns=["Name","Record"]
        )

    df.loc[len(df)] = [
        name,
        record
    ]

    df.to_csv(
        HISTORY_FILE,
        index=False
    )

def load_history(name):

    if not os.path.exists(
        HISTORY_FILE
    ):

        return pd.DataFrame(
            columns=["Name","Record"]
        )

    df = pd.read_csv(
        HISTORY_FILE
    )

    return df[
        df["Name"] == name
    ]


st.title("🏥 AI Health Assistant")
st.subheader(
    "SDG 3 - Good Health and Well Being"
)

name = st.sidebar.text_input(
    "Patient Name"
)

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Symptom Checker",
        "BMI Calculator",
        "Diet Recommendation",
        "Exercise Recommendation",
        "Patient History"
    ]
)


if menu == "Symptom Checker":

    st.header(
        "🤒 Symptom Checker"
    )

    if not df_symptoms.empty:

        symptom_list = [

            col

            for col in df_symptoms.columns

            if col != "diseases"
        ]

        selected = st.multiselect(
            "Select Symptoms",
            symptom_list
        )

        if st.button(
            "Predict Disease"
        ):

            result = predict_disease(
                selected
            )

            st.success(result)

            save_history(
                name,
                f"Symptoms: {selected}"
            )

elif menu == "BMI Calculator":

    st.header(
        "⚖ BMI Calculator"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0
    )

    height = st.number_input(
        "Height (m)",
        min_value=0.1
    )

    if st.button(
        "Calculate BMI"
    ):

        result = calculate_bmi(
            weight,
            height
        )

        st.success(
            f"BMI = {result}"
        )

        save_history(
            name,
            f"BMI = {result}"
        )


elif menu == "Diet Recommendation":

    st.header(
        "🥗 Diet Recommendation"
    )

    goal = st.selectbox(
        "Goal",
        [
            "Weight Loss",
            "Weight Gain",
            "Healthy Lifestyle"
        ]
    )

    if st.button(
        "Get Diet Plan"
    ):

        st.info(
            diet_plan(goal)
        )

        save_history(
            name,
            f"Diet Goal = {goal}"
        )


elif menu == "Exercise Recommendation":

    st.header(
        "🏃 Exercise Recommendation"
    )

    goal = st.selectbox(
        "Goal",
        [
            "Weight Loss",
            "Weight Gain",
            "Healthy Lifestyle"
        ]
    )

    if st.button(
        "Get Exercise Plan"
    ):

        st.info(
            exercise_plan(goal)
        )

        save_history(
            name,
            f"Exercise Goal = {goal}"
        )


elif menu == "Patient History":

    st.header(
        "📋 Patient History"
    )

    if name:

        st.dataframe(
            load_history(name)
        )

    else:

        st.warning(
            "Enter Patient Name"
        )