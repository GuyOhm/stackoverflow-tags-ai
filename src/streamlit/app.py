import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="StackOverflow Tag Suggester",
    page_icon="🏷️",
)

st.title("🏷️ StackOverflow Tag Suggester")
st.caption("A simple UI to test the tag suggestion API.")

# API URL (adjust if the API is not running locally)
API_URL = "http://127.0.0.1:8000/predict"

# Text area for the question
with st.form("question_form"):
    question_body = st.text_area(
        "Enter your question body",
        height=200,
        placeholder="e.g., How do I parse HTML in Python? I tried using regex but it's not reliable..."
    )
    submitted = st.form_submit_button("Suggest Tags")

if submitted and question_body:
    with st.spinner("Calling the API..."):
        try:
            response = requests.post(API_URL, json={"body": question_body})
            response.raise_for_status()  # Raises an exception for HTTP error codes (4xx or 5xx)
            
            tags_data = response.json()
            tags = tags_data.get("tags", [])
            
            st.success("API call successful!")
            
            if tags:
                st.write("Suggested Tags:")
                # Display tags as badges
                tags_html = "".join(f"<span style='background-color: #007BFF; color: white; border-radius: 5px; padding: 5px 10px; margin: 2px;'>{tag}</span>" for tag in tags)
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.warning("The model did not suggest any tags.")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the API. Make sure it is running. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
elif submitted:
    st.warning("Please enter a question body.") 