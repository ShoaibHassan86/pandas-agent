import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI

# Load API key from secrets or input field
api_key = st.secrets.get("openai_key") or st.text_input("🔑 Enter OpenAI API key", type="password")

st.title("📊 Natural Language Pandas + Chart Agent")
st.markdown("Upload a CSV file and ask data questions or request charts. Example: 'plot sales by category' or 'filter rows where price > 50'.")

# File upload
uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])

# Load CSV
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Input prompt
    prompt = st.text_area("💬 Ask a question or request a chart", placeholder="e.g., plot total sales by region as a bar chart")

    # Run query
    if st.button("🚀 Run Query"):
        if prompt and api_key:
            with st.spinner("🧠 Thinking..."):

                # OpenAI Client
                client = OpenAI(api_key=api_key)

                try:
                    # Prepare GPT prompt
                    gpt_prompt = (
                        "You are a Python pandas and matplotlib/seaborn expert. "
                        "Given the DataFrame df, write Python code to answer the following user query: "
                        f"{prompt}. Always use matplotlib or seaborn for charts. Display output with Streamlit. "
                        "Only return Python code. Do not explain anything."
                    )

                    # Send to OpenAI - use gpt-3.5-turbo instead of gpt-4
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful Python and pandas assistant."},
                            {"role": "user", "content": gpt_prompt}
                        ]
                    )

                    code = response.choices[0].message.content.strip()
                    st.code(code, language='python')

                    # Execute the code
                    local_vars = {
                        "df": df.copy(),
                        "st": st,
                        "plt": plt,
                        "sns": sns,
                        "pd": pd
                    }

                    exec(code, {}, local_vars)

                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please enter both a question and an OpenAI API key.")
