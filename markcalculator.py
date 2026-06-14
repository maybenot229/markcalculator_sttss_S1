import streamlit as st

st.set_page_config(page_title="Mark Calculator", page_icon="📊", layout="centered")

st.title("📊 Weighted Mark Calculator")
st.caption("Enter your marks below. Leave blank or type `-` to skip a subject.")

subjects = {
    "Chinese": 5,
    "Malay": 6,
    "English": 5,
    "SPM Mathematics": 3,
    "Adv Math": 4,
    "Moral": 2,
    "Sejarah": 4,
    "Physics": 6,
    "Chemistry": 6,
    "Biology": 6,
    "PE": 2,
    "ICT": 2,
}

st.divider()

inputs = {}
cols = st.columns(2)

for i, (subject, weight) in enumerate(subjects.items()):
    col = cols[i % 2]
    with col:
        val = st.text_input(f"{subject} (weight: {weight})", key=subject, placeholder="- to skip")
        inputs[subject] = (val.strip(), weight)

st.divider()

if st.button("Calculate", type="primary", use_container_width=True):
    active = {}
    skipped = []
    errors = []

    for subject, (val, weight) in inputs.items():
        if val == "" or val == "-":
            skipped.append(subject)
            continue
        try:
            mark = float(val)
            if not (0 <= mark <= 100):
                errors.append(f"{subject}: mark must be 0–100")
            else:
                active[subject] = {"mark": mark, "weight": weight}
        except ValueError:
            errors.append(f"{subject}: invalid input '{val}'")

    if errors:
        for e in errors:
            st.error(e)

    elif not active:
        st.warning("No subjects entered.")

    else:
        numerator = sum(d["mark"] * d["weight"] for d in active.values())
        denominator = sum(d["weight"] for d in active.values())
        avg = numerator / denominator

        st.success(f"### Weighted Average: {avg:.2f}")

        with st.expander("See breakdown"):
            formula_parts = [f"({d['mark']} × {d['weight']})" for d in active.values()]
            st.code(f"[{' + '.join(formula_parts)}] ÷ {denominator} = {avg:.2f}")
            st.table(
                [{"Subject": s, "Mark": d["mark"], "Weight": d["weight"], "Contribution": round(d["mark"] * d["weight"], 2)}
                 for s, d in active.items()]
            )

        if skipped:
            st.caption(f"Skipped: {', '.join(skipped)}")