import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# App Title
st.title("AI Prototype: Regulatory Control Coverage Intelligence Platform")

st.write("""
This prototype explores AI-driven regulatory control mapping,
coverage analysis and governance intelligence across enterprise compliance ecosystems.
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Regulatory Control Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Regulatory Data")
    st.dataframe(df)

    findings = []

    # Regulatory analysis
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # Missing control mapping
        if row["control_mapped"] == "no":
            risk_score += 40
            issues.append("Missing control mapping")

        # Weak evidence coverage
        if row["evidence_coverage"] == "weak":
            risk_score += 30
            issues.append("Weak evidence coverage")

        # Missing ownership
        if row["owner_assigned"] == "no":
            risk_score += 30
            issues.append("Missing ownership accountability")

        # Open remediation
        if row["open_issues"] > 3:
            risk_score += 20
            issues.append("High remediation backlog")

        # Critical regulation
        if row["regulation_criticality"] == "high":
            risk_score += 20
            issues.append("Critical regulatory exposure")

        findings.append({
            "regulation": row["regulation"],
            "risk_score": risk_score,
            "issues": ", ".join(issues)
        })

    risk_df = pd.DataFrame(findings)

    # Display findings
    st.subheader("Regulatory Coverage Findings")

    st.dataframe(risk_df)

    # High risk areas
    high_risk = risk_df[risk_df["risk_score"] >= 60]

    st.subheader("High-Risk Regulatory Areas")

    st.dataframe(high_risk)

    # Metrics
    st.metric(
        "High-Risk Regulatory Domains",
        len(high_risk)
    )

    # Coverage score
    avg_score = 100 - int(risk_df["risk_score"].mean())

    st.metric(
        "Regulatory Coverage Score",
        f"{avg_score}/100"
    )

    # Chart
    st.bar_chart(
        high_risk.set_index("regulation")["risk_score"]
    )

    # AI Insights
    st.subheader("AI Regulatory Governance Insights")

    summary = high_risk.to_string(index=False)

    prompt = f"""
    Analyze the following regulatory control coverage findings.

    Identify:
    - control coverage gaps
    - governance weaknesses
    - ownership accountability concerns
    - remediation bottlenecks
    - evidence management weaknesses
    - operational compliance risks

    Recommend:
    - control strengthening actions
    - remediation priorities
    - governance improvements
    - evidence management enhancements
    - operating model recommendations

    Findings:
    {summary}
    """

    with st.spinner("Generating AI governance insights..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior regulatory compliance and governance transformation expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content

        st.write(output)
