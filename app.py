import streamlit as st
from chatbot import load_eda_insights, chatbot_query
from eda import generate_eda_report
import os
import shutil

# Create a temporary directory for storing EDA outputs within the current directory
UPLOAD_DIR = "temp_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

EDA_REPORT_PATH = os.path.join(UPLOAD_DIR, "eda_report.html")
EDA_INSIGHTS_PATH = os.path.join(UPLOAD_DIR, "eda_insights.json")

# Initialize session state for chat history and file checks
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "eda_loaded" not in st.session_state:
    st.session_state["eda_loaded"] = False  # Tracks whether the EDA report is already loaded

if "dummy_refresh" not in st.session_state:
    st.session_state["dummy_refresh"] = 0  # Dummy variable for triggering rerun

# Streamlit app interface
st.title("EDA Chatbot")
st.write("Upload a dataset, generate insights, and chat dynamically about the data.")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV format):", type=["csv"])

if uploaded_file:
    # Save the uploaded file locally in the temporary directory
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # Check if insights and report already exist for the uploaded file
    existing_html_report = os.path.exists(EDA_REPORT_PATH)
    existing_json_insights = os.path.exists(EDA_INSIGHTS_PATH)

    # Show the message only once when the EDA file is first loaded
    if not st.session_state["eda_loaded"]:
        if existing_html_report and existing_json_insights:
            st.info("Using previously generated EDA report and insights.")
        else:
            with st.spinner("Generating EDA report..."):
                try:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Generate EDA report and insights
                    eda_insights = generate_eda_report(file_path, EDA_REPORT_PATH, EDA_INSIGHTS_PATH)
                    st.success("EDA report and insights generated successfully!")
                except Exception as e:
                    st.error(f"An error occurred while generating EDA insights: {e}")
                    eda_insights = {}

        st.session_state["eda_loaded"] = True  # Mark EDA as loaded

    # Provide a download link for the EDA report
    if os.path.exists(EDA_REPORT_PATH):
        with open(EDA_REPORT_PATH, "rb") as f:
            st.download_button("Download EDA Report (HTML)", f, file_name="eda_report.html")

# Step 2: Chatbot Interaction
if os.path.exists(EDA_INSIGHTS_PATH):
    try:
        # Load EDA insights for the chatbot
        eda_insights = load_eda_insights(EDA_INSIGHTS_PATH)

        # Chat interface
        st.subheader("Chat with the dataset")

        # Display chat history
        for chat in st.session_state["chat_history"]:
            if chat["role"] == "user":
                st.markdown(f"**You:** {chat['message']}")
            else:
                st.markdown(f"**Bot:** {chat['message']}")

        # User input for the next question
        user_query = st.text_input("Type your question:")

        if st.button("Send"):
            if user_query.strip() == "":
                st.warning("Please enter a valid question.")
            else:
                # Add the user's message to chat history
                st.session_state["chat_history"].append({"role": "user", "message": user_query})

                with st.spinner("Processing your query..."):
                    # Get the chatbot's response
                    response = chatbot_query(eda_insights, user_query)

                # Add the chatbot's response to chat history
                st.session_state["chat_history"].append({"role": "bot", "message": response})

                # Trigger a rerun by updating the dummy_refresh variable
                st.session_state["dummy_refresh"] += 1

    except Exception as e:
        st.error(f"An error occurred while loading EDA insights: {e}")

# Cleanup: Delete temporary files after runtime
def clear_temp_dir():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
        st.session_state["eda_loaded"] = False  # Reset EDA state

st.sidebar.button("Clear Temporary Files", on_click=clear_temp_dir)
