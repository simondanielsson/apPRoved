import requests
import streamlit as st

API_BASE_URL = "http://localhost:8082"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwic3ViIjoiYWRtaW4ifQ.bvp710BgRCUhoZDBlDol23FV-D4rX5snSCNv2GRkcqs"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}


def fetch_repositories():
    response = requests.get(f"{API_BASE_URL}/repositories", headers=HEADERS)
    if response.status_code == 200:
        print("fetch_repositories", response.json())
        return response.json()
    return []


def fetch_pull_requests(repository_id):
    response = requests.get(
        f"{API_BASE_URL}/repositories/{repository_id}/pull_requests",
        headers=HEADERS,
    )
    if response.status_code == 200:
        print("fetch_pull_requests", response.json())
        return response.json()
    return []


def fetch_reviews(repository_id, pull_request_id):
    response = requests.get(
        f"{API_BASE_URL}/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews",
        headers=HEADERS,
    )
    if response.status_code == 200:
        return response.json()
    return []


def fetch_review(repository_id, pull_request_id, review_id):
    response = requests.get(
        f"{API_BASE_URL}/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews/{review_id}",
        headers=HEADERS,
    )
    if response.status_code == 200:
        return response.json()
    return {}


def add_review(repository_id, pull_request_id):
    response = requests.post(
        f"{API_BASE_URL}/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews",
        headers=HEADERS,
    )
    if response.status_code == 201:
        return response.json()
    return []


def add_repository(repository_name, github_url):
    response = requests.post(
        f"{API_BASE_URL}/repositories",
        json={"repository_name": repository_name, "github_url": github_url},
        headers=HEADERS,
    )
    return response.status_code == 201


def add_pull_request(repository_id, pull_request_number):
    response = requests.post(
        f"{API_BASE_URL}/repositories/{repository_id}/pull_requests",
        headers=HEADERS,
        json={"pull_request_number": pull_request_number},
    )
    return response.status_code == 201


st.title("AI Pull Request Reviewer")

st.subheader("Repositories")
repositories = fetch_repositories()
repo_col1, repo_col2 = st.columns([4, 1])

with repo_col1:
    for repo in repositories:
        if st.button(repo["repository_name"], key=f"repo-{repo['id']}"):
            st.session_state["selected_repo_id"] = repo["id"]
            st.session_state["selected_repo_name"] = repo["repository_name"]

with repo_col2, st.expander("Add Repository"):
    repo_name = st.text_input("Repository Name")
    repo_url = st.text_input("GitHub URL")
    if st.button("Add Repository"):
        if add_repository(repo_name, repo_url):
            st.success("Repository added successfully!")
        else:
            st.error("Failed to add repository.")

# Second row for pull requests
if "selected_repo_id" in st.session_state:
    st.subheader(f"Pull Requests for {st.session_state['selected_repo_name']}")
    pull_requests = fetch_pull_requests(st.session_state["selected_repo_id"])
    pr_col1, pr_col2 = st.columns([4, 1])

    with pr_col1:
        for pr in pull_requests:
            if st.button(
                str(pr["pull_request_number"]),
                key=f"pr-{st.session_state['selected_repo_id']}-{pr['id']}",
            ):
                st.session_state["selected_pr_id"] = pr["id"]
                st.session_state["selected_pr_number"] = pr["pull_request_number"]

    with pr_col2, st.expander(
        "Add Pull Request",
    ):
        pr_number = st.text_input(
            "PR Number",
            key=f"pr_number_{st.session_state['selected_repo_id']}",
        )
        if st.button(
            "Add PR",
            key=f"add_pr_{st.session_state['selected_repo_id']}",
        ):
            if add_pull_request(st.session_state["selected_repo_id"], pr_number):
                st.success(f"Pull Request {pr_number} added successfully!")
            else:
                st.error("Failed to add pull request.")

if "selected_pr_id" in st.session_state:
    st.subheader(f"Reviews for PR {st.session_state['selected_pr_number']}")
    reviews = fetch_reviews(
        st.session_state["selected_repo_id"],
        st.session_state["selected_pr_id"],
    )
    review_col1, review_col2 = st.columns([4, 1])

    with review_col1:
        for review in reviews:
            if st.button(f"Review {review['id']}", key=f"review-{review['id']}"):
                selected_review = fetch_review(
                    st.session_state["selected_repo_id"],
                    st.session_state["selected_pr_id"],
                    review["id"],
                )
                st.session_state["selected_review"] = selected_review

    with review_col2:
        if st.button("Add Review"):
            if add_review(
                st.session_state["selected_repo_id"],
                st.session_state["selected_pr_id"],
            ):
                st.success("Review added successfully!")
            else:
                st.error("Failed to add review.")

    if selected_review := st.session_state.get("selected_review"):
        st.subheader(f"Review {selected_review['review_id']}")
        review_contents = selected_review["review_contents"]
        review_files = selected_review["file_names"]

        for review_message, file_name in zip(review_contents, review_files):
            st.write(f"**File `{file_name}`:**")
            st.write(review_message)
