import streamlit as st
import requests
import extra_streamlit_components as stx


BACKEND_URL = "http://localhost:8000"


st.set_page_config(
    page_title="NeuraChat",
    page_icon="🤖",
    layout="wide"
)


# =========================
# Cookie Manager
# =========================

cookie_manager = stx.CookieManager()


# =========================
# Session State
# =========================

if "token" not in st.session_state:
    st.session_state.token = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False

if "show_new_chat" not in st.session_state:
    st.session_state.show_new_chat = False


# =========================
# Restore Login After Refresh
# =========================

if (
    st.session_state.token is None
    and not st.session_state.logged_out
):

    saved_token = cookie_manager.get(
        "access_token"
    )

    if saved_token:
        st.session_state.token = saved_token


# =========================
# Helper Functions
# =========================

def get_headers():

    return {
        "Authorization":
            f"Bearer {st.session_state.token}"
    }


def load_conversations():

    response = requests.get(
        f"{BACKEND_URL}/conversations/",
        headers=get_headers()
    )

    if response.status_code == 200:

        st.session_state.conversations = (
            response.json()
        )

        return True

    return False


def load_messages(conversation_id):

    response = requests.get(
        f"{BACKEND_URL}/chat/{conversation_id}/messages",
        headers=get_headers()
    )

    if response.status_code == 200:

        st.session_state.messages = (
            response.json()
        )

        return True

    st.error(response.json())

    return False


def create_new_conversation(title):

    response = requests.post(
        f"{BACKEND_URL}/conversations/",
        headers=get_headers(),
        json={
            "title": title
        }
    )

    if response.status_code == 200:

        data = response.json()

        st.session_state.conversation_id = (
            data["id"]
        )

        st.session_state.messages = []

        load_conversations()

        return True

    st.error(response.json())

    return False


def logout():

    # Stop restoring old cookie
    st.session_state.logged_out = True

    # Remove token
    st.session_state.token = None

    # Clear current conversation
    st.session_state.conversation_id = None

    # Clear messages
    st.session_state.messages = []

    # Clear conversations
    st.session_state.conversations = []

    # Hide new chat input
    st.session_state.show_new_chat = False

    # Delete browser cookie
    cookie_manager.delete(
        "access_token"
    )

    st.rerun()


# =========================
# Authentication
# =========================

if not st.session_state.token:

    st.title("🤖 NeuraChat")

    register_tab, login_tab = st.tabs([
        "Register",
        "Login"
    ])


    # =========================
    # Register
    # =========================

    with register_tab:

        st.subheader("Create Account")

        register_col1, register_col2, register_col3 = (
            st.columns([1, 2, 1])
        )

        with register_col2:

            name = st.text_input(
                "Name",
                key="register_name"
            )

            email = st.text_input(
                "Email",
                key="register_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="register_password"
            )

            if st.button(
                "Register",
                use_container_width=True
            ):

                response = requests.post(
                    f"{BACKEND_URL}/users/register",
                    json={
                        "name": name,
                        "email": email,
                        "password": password
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Registration successful! "
                        "Please login."
                    )

                else:

                    st.error(
                        response.json()
                    )


    # =========================
    # Login
    # =========================

    with login_tab:

        st.subheader("Login")

        login_col1, login_col2, login_col3 = (
            st.columns([1, 2, 1])
        )

        with login_col2:

            email = st.text_input(
                "Email",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                response = requests.post(
                    f"{BACKEND_URL}/users/login",
                    json={
                        "email": email,
                        "password": password
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    token = data["access_token"]

                    # Store token in session
                    st.session_state.token = token

                    # User logged in
                    st.session_state.logged_out = False

                    # Store token in browser cookie
                    cookie_manager.set(
                        "access_token",
                        token,
                        max_age=60 * 60
                    )

                    # Load conversations
                    load_conversations()

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        response.json()
                    )


# =========================
# Logged-in User
# =========================

else:

    # =========================
    # Top Bar
    # =========================

    top_col1, top_col2 = st.columns(
        [8, 1]
    )

    with top_col1:

        st.title("🤖 NeuraChat")

    with top_col2:

        if st.button(
            "Logout",
            use_container_width=True
        ):

            logout()


    # =========================
    # Load Conversations
    # =========================

    if not st.session_state.conversations:

        load_conversations()


    # =========================
    # Sidebar
    # =========================

    with st.sidebar:

        st.title("🗂️ History")


        # =========================
        # New Chat Button
        # =========================

        if st.button(
            "✏️ New Chat",
            use_container_width=True
        ):

            st.session_state.show_new_chat = True

            st.rerun()


        # =========================
        # New Chat Title Input
        # =========================

        if st.session_state.show_new_chat:

            new_chat_title = st.text_input(
                "Conversation title",
                placeholder="Enter title...",
                key="new_chat_title"
            )


            if st.button(
                "Create",
                use_container_width=True
            ):

                if new_chat_title.strip():

                    if create_new_conversation(
                        new_chat_title.strip()
                    ):

                        st.session_state.show_new_chat = False

                        st.rerun()

                else:

                    st.warning(
                        "Please enter a conversation title."
                    )


        st.divider()


        # =========================
        # Existing Conversations
        # =========================

        if not st.session_state.conversations:

            st.info(
                "No conversations yet."
            )

        else:

            for conversation in (
                st.session_state.conversations
            ):

                conversation_id = (
                    conversation["id"]
                )

                conversation_title = (
                    conversation["title"]
                )


                if st.button(
                    conversation_title or "Untitled",
                    key=f"conversation_{conversation_id}",
                    use_container_width=True
                ):

                    # Select conversation
                    st.session_state.conversation_id = (
                        conversation_id
                    )

                    # Load messages
                    load_messages(
                        conversation_id
                    )

                    st.rerun()


    # =========================
    # Main Chat Area
    # =========================

    if st.session_state.conversation_id:

        # =========================
        # Current Conversation Title
        # =========================

        current_title = "Chat"


        for conversation in (
            st.session_state.conversations
        ):

            if (
                conversation["id"]
                == st.session_state.conversation_id
            ):

                current_title = (
                    conversation["title"]
                    or "Untitled"
                )

                break


        st.header(
            f"💬 {current_title}"
        )


        # =========================
        # Display Messages
        # =========================

        for message in (
            st.session_state.messages
        ):

            st.chat_message(
                message["role"]
            ).write(
                message["content"]
            )


        # =========================
        # Send Message
        # =========================

        user_message = st.chat_input(
            "Type your message..."
        )


        if user_message:

            headers = get_headers()


            with st.spinner(
                "🤖 AI is thinking..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/chat/",
                    headers=headers,
                    json={
                        "conversation_id":
                            st.session_state.conversation_id,

                        "message":
                            user_message
                    }
                )


            if response.status_code == 200:

                data = response.json()


                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_message
                })


                # Add AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["content"]
                })


                st.rerun()


            else:

                st.error(
                    response.json()
                )


    else:

        st.info(
            "Create a new conversation or select one "
            "from the sidebar to start chatting."
        )