import streamlit as st
import requests
import json

st.set_page_config(page_title="GitHub Issue AI Assistant")

st.title("GitHub Issue AI Assistant")


if "cache" not in st.session_state:
    st.session_state.cache = {}

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/fastapi/fastapi"
)

issue_number = st.number_input(
    "Issue Number",
    min_value=1,
    step=1
)

if st.button("Analyze Issue"):
    if not repo_url:
        st.error("Please enter a repository URL")
    else:
        cache_key = f"{repo_url}:{issue_number}"

       
        if cache_key in st.session_state.cache:
            data = st.session_state.cache[cache_key]
        else:
            with st.spinner("Analyzing issue..."):
                response = requests.get(
                    "http://127.0.0.1:8000/analyze",
                    params={
                        "repo_url": repo_url,
                        "issue_number": issue_number
                    }
                )

            if response.status_code != 200:
                st.error(f"Error: {response.text}")
                st.stop()

            data = response.json()
            st.session_state.cache[cache_key] = data

       
        st.subheader("Readable Summary")

        priority_level = (
            f"{data['priority_score']} (High impact)"
            if int(data["priority_score"]) >= 4
            else data["priority_score"]
        )

        st.markdown(f"""
**Issue Type:** {data['type'].capitalize()}  

**Priority:** {priority_level}  

**Summary:**  
{data['summary']}

**Impact:**  
{data['potential_impact']}

**Suggested Labels:**  
{', '.join(data['suggested_labels'])}
""")

      
        st.subheader("Analysis Result")

        json_text = json.dumps(data, indent=2)

        st.code(json_text, language="json")

        
        st.download_button(
            label="⬇️ Download JSON",
            data=json_text,
            file_name="issue_analysis.json",
            mime="application/json"
        )
