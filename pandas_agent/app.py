import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns

openai.api_key = st.secrets.get("openai_key") or st.text_input("🔑 Enter OpenAI API key", type="password")

st.title("📊 Natural Language Pandas + Chart Agent")
st.markdown("Upload a CSV file and ask data questions or request charts. Example: *'plot sales by category'* or *'filter rows where price > 50'*.")

uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    prompt = st.text_area("💬 Ask a question or request a chart", placeholder="e.g., plot total sales by region as a bar chart")

    if st.button("🚀 Run Query"):
        if prompt and openai.api_key:
            with st.spinner("🧠 Thinking..."):
                try:
                    gpt_prompt = (
                        "You are a Python pandas and matplotlib/seaborn expert. "
                        "Given the DataFrame `df`, write Python code to answer the following: "
                        f"{prompt}. Always use matplotlib or seaborn for plots. Show the result or plot using Streamlit. "
                        "Do not include explanations. Only return code."
                    )

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a Python data expert using pandas and Streamlit."},
                            {"role": "user", "content": gpt_prompt}
                        ]
                    )

                    code = response['choices'][0]['message']['content']
                    st.code(code, language='python')

                    # Prepare environment
                    local_vars = {'df': df.copy(), 'st': st, 'plt': plt, 'sns': sns, 'pd': pd}
                    exec(code, {}, local_vars)

                except Exception as e:
                    st.error(f"⚠️ Error executing code: {e}")
        else:
            st.warning("Enter both a query and an OpenAI API key.")
