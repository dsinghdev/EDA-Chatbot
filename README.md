# EDA Chatbot with Interactive Chat

This project is an **Exploratory Data Analysis (EDA) Chatbot** built using **Streamlit**, designed to allow users to upload datasets, generate insights, and interact dynamically with a chatbot to query the data.

---

## Features

- **Dataset Upload**:
  Upload CSV files for analysis.

- **Automated EDA**:
  Automatically generates:
  - Dataset statistics
  - Missing value analysis
  - Summary statistics
  - Visualizations (via HTML report)

- **Interactive Chat**:
  Chat dynamically with the dataset to:
  - Ask questions about dataset statistics.
  - Fetch specific column insights.
  - Query missing values, mean, correlations, etc.

- **Persistent Chat History**:
  Retains conversation history for the session.

- **Temporary File Management**:
  Manages temporary files during runtime and cleans them up after the session.

---

## Tech Stack

- **Python**
- **Streamlit**: For creating the interactive web app.
- **Hugging Face Inference API**: For chatbot queries.
- **Pandas Profiling**: For generating the EDA report.
- **Session State**: To maintain chat history and app state.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/eda-chatbot.git
   cd eda-chatbot
   ```
2. **Create a Virtual Environment:**

```bash
python -m venv venv
venv\Scripts\activate     # For Windows
```
3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```
3. **Run the Application:**

```bash
streamlit run app.py
```