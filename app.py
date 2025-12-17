from database import init_db, insert_demo_data, has_demo_data


import streamlit as st
from database import init_db, get_reference_speed, store_deviation

init_db()

st.set_page_config(page_title="Machine Speed Monitor", layout="centered")

st.title("🖨️ Machine Speed Monitor (Demo)")

# --- Input ---
machine_id = st.selectbox("Machine", ["RO-01", "RO-02"])
paper_type = st.selectbox("Paper type", ["SC-B 60g", "LWC 70g"])
run_size = st.selectbox("Run size", ["0–10k", "10k–50k", ">50k"])
current_speed = st.number_input("Current speed (copies/hour)", min_value=0)

# --- Reference ---
reference_speed = get_reference_speed(machine_id, paper_type, run_size)

if reference_speed:
    deviation = (current_speed / reference_speed) * 100

    if deviation >= 98:
        st.success(f"🟢 Optimal – {deviation:.1f}% of best speed")
        status = "GREEN"
    elif deviation >= 95:
        st.warning(f"🟡 Slight deviation – {deviation:.1f}%")
        status = "YELLOW"
    else:
        st.error(f"🔴 Underperformance – {deviation:.1f}%")
        status = "RED"

    st.metric("Best historical speed", f"{reference_speed:.0f}")
else:
    st.info("No historical reference available")
    deviation = None
    status = "NO_REFERENCE"

# --- Deviation reason ---
if status == "RED":
    st.subheader("Reason for deviation (mandatory)")

    category = st.selectbox(
        "Category",
        ["Technical", "Job-related", "Other"]
    )

    technical_issue = None
    informed_party = None

    if category == "Technical":
        technical_issue = st.selectbox(
            "Technical issue",
            ["Paper web", "Folder", "Dryer", "Register", "Other"]
        )
        informed_party = st.multiselect(
            "Who was informed?",
            ["Team Leader", "Maintenance"]
        )

    comment = st.text_area("Comment")

    if st.button("Save deviation"):
        if category == "Technical" and not informed_party:
            st.error("Please specify who was informed.")
        else:
            store_deviation({
                "machine_id": machine_id,
                "current_speed": current_speed,
                "reference_speed": reference_speed,
                "deviation_percent": deviation,
                "category": category,
                "technical_issue": technical_issue,
                "informed_party": ", ".join(informed_party) if informed_party else None,
                "comment": comment
            })
            st.success("Deviation saved successfully.")

from database import insert_demo_data
insert_demo_data()

