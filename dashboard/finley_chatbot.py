import streamlit as st


def initialize_chat():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def finley_chat(income, savings, sip):

    initialize_chat()

    st.markdown("### 🤖 Ask Finley")

    user_input = st.chat_input("Ask Finley about your finances...")

    if user_input:

        response = generate_response(user_input, income, savings, sip)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("finley", response))


    for role, message in st.session_state.chat_history:

        if role == "user":
            st.chat_message("user").write(message)

        else:
            st.chat_message("assistant").write(message)


def generate_response(question, income, savings, sip):

    q = question.lower()

    if "car" in q:
        return "Buying a car depends on maintaining at least 6 months of savings buffer."

    if "invest" in q:
        return f"You should invest around ₹{sip:,.0f} monthly to achieve your goal."

    if "save" in q:
        rate = savings / income
        return f"Your savings rate is {rate*100:.1f}%. Aim for at least 20%."

    if "study" in q or "masters" in q:
        return "Higher studies funding should start early because inflation increases education cost quickly."

    return "That's a great financial question. Try asking about investments, savings, or planning."