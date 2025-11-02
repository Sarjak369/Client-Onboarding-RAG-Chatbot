import streamlit as st
from datetime import datetime


class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = st.session_state.get("messages", [])
        self.employee_information = assistant.employee_information

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        if not self.messages:
            st.chat_message("ai").markdown(
                "🧠 **Umbrella Assistant Online.** How can I assist you today?"
            )
        for message in self.messages:
            role_icon = "👤" if message["role"] == "user" else "☂️"
            with st.chat_message(message["role"], avatar=role_icon):
                st.markdown(message["content"])

    def render_user_input(self):
        user_input = st.chat_input("Type your query securely here...")
        if user_input:
            self.messages.append({"role": "user", "content": user_input})
            st.chat_message("user", avatar="👤").markdown(user_input)

            with st.chat_message("ai", avatar="☂️"):
                response_stream = self.get_response(user_input)
                response = st.write_stream(response_stream)

            self.messages.append({"role": "ai", "content": response})
            st.session_state["messages"] = self.messages

    def render_sidebar_profile(self):
        with st.sidebar:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg",
                width=120,
            )
            st.markdown("### 🧾 Employee Profile")
            st.markdown(
                f"**Name:** {self.employee_information['name']} {self.employee_information['lastname']}")
            st.markdown(f"**Email:** {self.employee_information['email']}")
            st.markdown(
                f"**Department:** {self.employee_information['department']}")
            st.markdown(
                f"**Position:** {self.employee_information['position']}")
            st.markdown(
                f"**Supervisor:** {self.employee_information['supervisor']}")
            st.markdown(
                f"**Location:** {self.employee_information['location']}")
            st.markdown("---")
            st.caption(
                f"Active Session: {datetime.now().strftime('%H:%M:%S')}")

    def render(self):
        self.render_sidebar_profile()
        self.render_messages()
        self.render_user_input()
