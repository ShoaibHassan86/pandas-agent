import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI
from openai.error import OpenAIError

# Load API key from secrets or user input
api_key = st.secrets.get("openai_key") or st.text_input("🔑 Enter your OpenAI API key (free trial key works)", type="password")

st.title("📊 Natural Language Pandas + Chart Agent (Free Deployment)")

st.markdown("""
Upload a CSV file and ask data questions or request charts.
Example prompts:
- "plot sales by category"
- "filter rows where price > 50"
""")

uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    prompt = st.text_area("💬 Ask a question or request a chart",
                          placeholder="e.g., plot total sales by region as a bar chart")

    if st.button("🚀 Run Query"):
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key to continue.")
        elif not prompt:
            st.warning("⚠️ Please enter a prompt/question.")
        else:
            with st.spinner("🧠 Thinking..."):
                client = OpenAI(api_key=api_key)
                gpt_prompt = (
                    "You are a Python pandas and matplotlib/seaborn expert. "
                    "Given the DataFrame df, write Python code to answer the following user query: "
                    f"{prompt}. Always use matplotlib or seaborn for charts. Display output with Streamlit. "
                    "Only return Python code. Do not explain anything."
                )

                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful Python and pandas assistant."},
                            {"role": "user", "content": gpt_prompt}
                        ]
                    )
                    code = response.choices[0].message.content.strip()
                    st.code(code, language="python")

                    local_vars = {
                        "df": df.copy(),
                        "st": st,
                        "plt": plt,
                        "sns": sns,
                        "pd": pd
                    }

                    exec(code, {}, local_vars)

                except OpenAIError as e:
                    if e.http_status == 429:
                        st.error("🚫 API quota exceeded! Please wait or use another API key.")
                    else:
                        st.error(f"⚠️ OpenAI API error: {e}")
                except Exception as e:
                    st.error(f"⚠️ Unexpected error: {e}")
