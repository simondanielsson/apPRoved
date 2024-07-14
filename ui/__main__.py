import streamlit as st

from ui import api_requests as requests

# Define the API endpoint

st.title("AI Pull Request Reviewer")

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwic3ViIjoiYWRtaW4ifQ.bvp710BgRCUhoZDBlDol23FV-D4rX5snSCNv2GRkcqs"
# Inputs for the repository ID and pull request ID
repository = st.text_input("Repository", "")
pull_request_number = st.text_input("Pull Request Number", "")
github_url = st.text_input("GitHub URL", "https://github.com")

# Create a button to trigger the review process
if st.button("Create Review"):
    if repository and pull_request_number:
        response_data = requests.create_review(
            repository,
            int(pull_request_number),
            github_url=github_url,
            token=token,
        )
        review_content = response_data.get("review_content", [])

        st.success("Review created successfully!")

        # Display each review message
        for idx, review_message in enumerate(review_content, start=1):
            st.write(f"**File {idx}:**")
            st.write(review_message)
    else:
        st.error("Please enter both repository ID and pull request ID")
