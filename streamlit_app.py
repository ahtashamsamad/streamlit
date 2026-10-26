
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(
    page_title="Student Predictor",
    page_icon="🎓",
    layout="centered"
)

# App heading
st.title("🎓 Student Pass / Fail Predictor")
st.markdown(
    "Enter the student's details below to predict their result."
)
st.markdown("---")

# Input widgets
col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider(
        "Study Hours Per Day",
        min_value=0.0,
        max_value=10.0,
        value=4.0,
        step=0.5
    )

with col2:
    prev_score = st.slider(
        "Previous Exam Score",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0
    )

st.markdown("---")

# Prediction button
if st.button("🎯 Predict Result", use_container_width=True):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={
                "study_hours": study_hours,
                "prev_score": prev_score
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            if result["prediction"] == 1:
                st.success(
                    f"✅ Result: {result['result_label']}"
                )
            else:
                st.error(
                    f"❌ Result: {result['result_label']}"
                )

            st.metric(
                "Model Confidence",
                f"{result['confidence'] * 100:.1f}%"
            )

            with st.expander("View API Response"):
                st.json(result)

        else:
            st.error(
                f"API Error: {response.status_code}"
            )
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI server is not running. "
            "Please start FastAPI first."
        )

    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# Input summary
st.markdown("---")
st.subheader("📊 Current Input Summary")

m1, m2 = st.columns(2)

m1.metric(
    "Study Hours",
    f"{study_hours} hrs/day"
)

m2.metric(
    "Previous Score",
    f"{prev_score}/100"
)
