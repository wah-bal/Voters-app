import streamlit as st

if "votes" not in st.session_state:
    st.session_state.votes = []
if "used_creds" not in st.session_state:
    st.session_state.used_creds = set()

VALID_USERS = {"alex": "apple123", "sam": "banana456", "jordan": "cherry789"}
ADMIN_KEY = "mysecret77"
OPTIONS = ["Option A", "Option B", "Option C"]

st.title("🗳️ Custom Voting Portal")

st.subheader("1. Verify Identity")
username = st.text_input("Username").strip().lower()
password = st.text_input("Password", type="password").strip()

if username and password:
    if username in VALID_USERS and VALID_USERS[username] == password:
        if username in st.session_state.used_creds:
            st.error("❌ You have already submitted your vote!")
        else:
            st.success("✅ Access Granted. Rank your choices below.")
            
            st.subheader("2. Rank Your Choices")
            rank1 = st.selectbox("Your #1 Choice (Best)", ["--"] + OPTIONS)
            rank2 = st.selectbox("Your #2 Choice", ["--"] + OPTIONS)
            rank3 = st.selectbox("Your #3 Choice", ["--"] + OPTIONS)
            
            if st.button("Cast Secure Vote"):
                choices_made = [rank1, rank2, rank3]
                if "--" in choices_made or len(set(choices_made)) < 3:
                    st.error("❌ Please select 3 unique options.")
                else:
                    st.session_state.votes.append(choices_made)
                    st.used_creds.add(username)
                    st.success("🎉 Your vote is locked in!")
                    st.balloons()
    else:
        st.error("Invalid Username or Password.")

st.markdown("---")
st.subheader("👁️ Results Panel (Admin Only)")
admin_input = st.text_input("Enter Admin Key", type="password")

if admin_input == ADMIN_KEY:
    st.write("### Raw Votes Cast:", st.session_state.votes)
    scores = {opt: 0 for opt in OPTIONS}
    for vote in st.session_state.votes:
        scores[vote[0]] += 2  # 1st place gets 2 points
        scores[vote[1]] += 1  # 2nd place gets 1 point
        scores[vote[2]] += 0  # 3rd place gets 0 points
    st.write("### Standings (Borda Points):")
    st.bar_chart(scores)
