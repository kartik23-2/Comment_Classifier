
import streamlit as st
import requests

API_URL = "https://comment-classifier-0ep9.onrender.com/check-comment"

st.title("Comment Classifier (Spam + Profanity)")

text = st.text_area("Enter a comment to check:")

if st.button("Check"):
    if text.strip() == "":
        st.warning("Please enter a comment.")
    else:
        with st.spinner("Checking..."):
            response = requests.post(API_URL, json={"text": text})

            if response.status_code == 200:
                result = response.json()

                st.subheader("Spam Result")
                st.write("Spam:", result["spam_check"]["is_spam"])
                st.write("Confidence:", result["spam_check"]["confidence"])

                st.subheader("Profanity Result")
                st.write("Profanity:", result["profanity_check"]["is_profane"])
                st.write("Confidence:", result["profanity_check"]["confidence"])
            else:
                st.error("Error contacting API. Check Render deployment.")
