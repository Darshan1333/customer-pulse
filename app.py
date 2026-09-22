"""Customer Pulse: a small Streamlit customer-success dashboard using demo data."""

from __future__ import annotations

from html import escape
from typing import Any

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Customer Pulse", page_icon="◉", layout="wide")

DATA: dict[str, dict[str, Any]] = {
    "Acme Retail": {"industry": "Retail", "arr": 420_000, "health": 82, "adoption": 78, "renewal": 94, "nps": 48, "csat": 94,
        "signals": [("Leadership", "New Chief Customer Officer joined.", "3 days ago", "Opportunity"), ("Growth", "42 store-manager roles opened.", "6 days ago", "Opportunity"), ("Usage", "Store adoption increased 14%.", "Yesterday", "Positive"), ("Support", "Two workflow issues remain open.", "2 days ago", "Risk")],
        "stakeholders": [("Maya Chen", "VP Customer Experience", "Economic Buyer", "High"), ("Arjun Mehta", "Director, Store Operations", "Champion", "High"), ("Priya Shah", "IT Program Manager", "Influencer", "Medium"), ("Rahul Singh", "Regional Store Manager", "User", "Medium")],
        "goals": ["Increase adoption across regional stores", "Reduce manual reporting time", "Demonstrate measurable operational ROI"]},
    "Northstar Finance": {"industry": "Financial Services", "arr": 285_000, "health": 64, "adoption": 51, "renewal": 48, "nps": 24, "csat": 91,
        "signals": [("Usage", "Weekly active users fell 9%.", "Yesterday", "Risk"), ("Leadership", "Cost-efficiency initiative announced.", "4 days ago", "Risk"), ("Hiring", "Digital transformation hiring increased.", "8 days ago", "Opportunity"), ("Support", "SLA compliance remains at 97%.", "2 days ago", "Positive")],
        "stakeholders": [("Daniel Wong", "Head of Operations", "Economic Buyer", "High"), ("Rhea Kapoor", "Transformation Lead", "Champion", "Medium"), ("Omar Khan", "IT Administrator", "Influencer", "Medium")],
        "goals": ["Recover adoption in underused teams", "Quantify cost and productivity savings", "Prepare a renewal business case"]},
    "Vertex Health": {"industry": "Healthcare", "arr": 610_000, "health": 91, "adoption": 89, "renewal": 120, "nps": 61, "csat": 97,
        "signals": [("Expansion", "New regional operating unit announced.", "2 days ago", "Opportunity"), ("Usage", "Adoption reached a portfolio high of 89%.", "Yesterday", "Positive"), ("Executive", "Sponsor requested an ROI-focused QBR.", "5 days ago", "Opportunity"), ("Support", "No critical issues in the last 30 days.", "Today", "Positive")],
        "stakeholders": [("Anika Rao", "Chief Digital Officer", "Executive Sponsor", "High"), ("Samir Patel", "Product Operations", "Champion", "High"), ("Elena Martin", "Regional Lead", "User", "Medium")],
        "goals": ["Prove ROI at executive level", "Extend successful workflows to the new unit", "Create internal customer advocates"]},
}

st.markdown("""<style>
.stApp{background:#f7f8fa}.block-container{max-width:1450px;padding-top:1.4rem}.hero{background:#101828;color:white;padding:28px 32px;border-radius:18px;margin-bottom:20px}.hero h1{margin:0;font-size:32px}.hero p{margin:8px 0 0;color:#c9d2df}.card{background:white;border:1px solid #e4e7ec;border-radius:14px;padding:18px;margin-bottom:14px}.label{color:#667085;font-size:11px;text-transform:uppercase;letter-spacing:.6px}.value{color:#101828;font-size:26px;font-weight:700;margin-top:5px}.small{color:#667085;font-size:13px}.section{color:#101828;font-size:20px;font-weight:650;margin:26px 0 12px}.insight{background:#eff8ff;border:1px solid #b9e6fe;border-radius:14px;padding:19px;line-height:1.55}.action{background:#fafafa;border-left:3px solid #101828;padding:12px 14px;margin:8px 0;border-radius:0 8px 8px 0}.signal{padding:13px 0;border-bottom:1px solid #eaecf0}.signal:last-child{border-bottom:0}.badge{display:inline-block;padding:3px 8px;border-radius:999px;font-size:11px;font-weight:650}.positive{background:#ecfdf3;color:#067647}.risk{background:#fef3f2;color:#b42318}.opportunity{background:#eff8ff;color:#175cd3}.neutral{background:#f2f4f7;color:#475467}
</style>""", unsafe_allow_html=True)


def money(value: int | float) -> str:
    return f"${value:,.0f}"


def status(health: int | float) -> str:
    return "Healthy" if health >= 75 else "Watch" if health >= 55 else "At Risk"


def icon(health: int | float) -> str:
    return "🟢" if health >= 75 else "🟡" if health >= 55 else "🔴"


def badge_class(kind: str) -> str:
    return {"Positive": "positive", "Risk": "risk", "Opportunity": "opportunity"}.get(kind, "neutral")


def recommended_insight(customer: dict[str, Any]) -> str:
    if customer["health"] < 55:
        return "Usage and relationship signals indicate elevated renewal risk. Prioritize executive alignment and a focused adoption recovery plan."
    if customer["adoption"] < 65:
        return "Adoption is the clearest value gap. Connect the product to one measurable business outcome and create a short recovery plan with the champion."
    return "The account is showing strong adoption and positive engagement. Connect the latest business signal to measurable outcomes and explore where the successful workflow can expand."


def portfolio_frame() -> pd.DataFrame:
    """Create a stable tabular view, avoiding fragile DataFrame attribute access."""
    return pd.DataFrame(
        [{"Account": name, "Industry": item["industry"], "ARR": item["arr"], "Health": item["health"],
          "Adoption": item["adoption"], "Renewal": item["renewal"]} for name, item in DATA.items()]
    )


st.sidebar.markdown("## Customer Pulse")
st.sidebar.caption("Enterprise customer intelligence for CSMs")
view = st.sidebar.radio("View", ["Portfolio", "Account Intelligence"])

if view == "Portfolio":
    st.markdown('<div class="hero"><h1>Customer Pulse</h1><p>Know what changed, why it matters, and what to do next.</p></div>', unsafe_allow_html=True)
    df = portfolio_frame()
    metrics = [
        ("Accounts", len(df), "Enterprise portfolio"), ("ARR", money(df["ARR"].sum()), "Total recurring revenue"),
        ("Avg health", f'{df["Health"].mean():.0f}/100', "Portfolio health"), ("Avg adoption", f'{df["Adoption"].mean():.0f}%', "Product adoption"),
        ("At risk", int((df["Health"] < 55).sum()), "Needs attention"),
    ]
    for column, (label, value, description) in zip(st.columns(len(metrics)), metrics):
        with column:
            st.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="small">{description}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Portfolio health</div>', unsafe_allow_html=True)
    health_counts = pd.DataFrame({"Status": ["Healthy", "Watch", "At Risk"], "Accounts": [int((df["Health"] >= 75).sum()), int(((df["Health"] >= 55) & (df["Health"] < 75)).sum()), int((df["Health"] < 55).sum())]})
    st.bar_chart(health_counts.set_index("Status"), width="stretch")

    st.markdown('<div class="section">Account command center</div>', unsafe_allow_html=True)
    table = df.copy()
    table["ARR"] = table["ARR"].map(money)
    table["Health"] = table["Health"].map(lambda value: f"{icon(value)} {value} · {status(value)}")
    table["Renewal"] = table["Renewal"].map(lambda value: f"{value} days")
    st.dataframe(table, width="stretch", hide_index=True)

    st.markdown('<div class="section">Priority queue</div>', unsafe_allow_html=True)
    for _, row in df.sort_values(["Health", "Renewal"]).iterrows():
        action = "Executive escalation + adoption recovery plan" if row["Health"] < 55 else "Renewal readiness review + value proof" if row["Renewal"] < 60 else "Map expansion opportunity to latest business signal"
        severity = "risk" if row["Health"] < 55 else "opportunity"
        st.markdown(f'<div class="card"><strong>{icon(row["Health"])} {escape(str(row["Account"]))}</strong> <span class="badge {severity}">{status(row["Health"])}</span><br><span class="small">Health {row["Health"]}/100 · Adoption {row["Adoption"]}% · Renewal {row["Renewal"]} days</span><br><br><strong>Next best action:</strong> {action}</div>', unsafe_allow_html=True)

else:
    name = st.sidebar.selectbox("Customer", list(DATA))
    customer = DATA[name]
    st.markdown(f'<div class="hero"><h1>{escape(name)}</h1><p>{escape(customer["industry"])} · Account intelligence briefing</p></div>', unsafe_allow_html=True)
    metrics = [("Health", f'{customer["health"]}/100', status(customer["health"])), ("ARR", money(customer["arr"]), "Current contract"), ("Adoption", f'{customer["adoption"]}%', "Product usage"), ("Renewal", f'{customer["renewal"]}d', "Time to renewal"), ("NPS", customer["nps"], "Customer sentiment"), ("CSAT", f'{customer["csat"]}%', "Support satisfaction")]
    for column, (label, value, description) in zip(st.columns(len(metrics)), metrics):
        with column:
            st.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="small">{description}</div></div>', unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])
    with left:
        st.markdown('<div class="section">What is happening?</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for category, signal, age, kind in customer["signals"]:
            st.markdown(f'<div class="signal"><span class="badge neutral">{escape(category)}</span> <span class="badge {badge_class(kind)}">{escape(kind)}</span><div><strong>{escape(signal)}</strong></div><div class="small">{escape(age)}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="section">Signal-to-action logic</div>', unsafe_allow_html=True)
        st.info("The production version would ingest CRM, product, support and trusted external signals, then use AI to summarize them with source links and timestamps.")
    with right:
        st.markdown('<div class="section">What should I tell the customer today?</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight"><strong>Recommended customer insight</strong><br><br>{escape(recommended_insight(customer))}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section">Next-best actions</div>', unsafe_allow_html=True)
        actions = ["Lead with the recommended business insight.", "Confirm the customer outcome and measure progress against it.", "Multi-thread the account across buyer, champion and users."]
        if customer["health"] < 55:
            actions[0] = "Escalate internally and create a time-bound recovery plan."
        elif customer["renewal"] < 60:
            actions[0] = "Start renewal readiness and quantify realized value."
        for index, action in enumerate(actions, start=1):
            st.markdown(f'<div class="action"><strong>Action {index}</strong><br>{escape(action)}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Stakeholder map</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(customer["stakeholders"], columns=["Name", "Role", "Relationship", "Priority"]), width="stretch", hide_index=True)
    st.markdown('<div class="section">Customer goals</div>', unsafe_allow_html=True)
    for index, (column, goal) in enumerate(zip(st.columns(len(customer["goals"])), customer["goals"]), start=1):
        with column:
            st.markdown(f'<div class="card"><strong>Goal {index}</strong><p class="small">{escape(goal)}</p></div>', unsafe_allow_html=True)

st.caption("Demo data · Production roadmap: CRM + product analytics + support + trusted external signals + AI summaries with citations")
