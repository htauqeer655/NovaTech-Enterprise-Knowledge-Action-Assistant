import inspect
import os
import uuid

import gradio as gr
import requests

API_BASE_URL = "http://127.0.0.1:8001"

REGISTER_URL = f"{API_BASE_URL}/register"
LOGIN_URL = f"{API_BASE_URL}/login"
CHAT_URL = f"{API_BASE_URL}/chat"
UPLOAD_URL = f"{API_BASE_URL}/upload"

css = """
/* =========================================================
   NovaTech Enterprise Assistant — polished SaaS UI
   ========================================================= */

:root {
    --nt-navy: #12213f;
    --nt-navy-2: #24385d;
    --nt-indigo: #5b5ce2;
    --nt-indigo-dark: #4c4dcc;
    --nt-bg: #f3f5f9;
    --nt-surface: #ffffff;
    --nt-surface-soft: #f7f8fb;
    --nt-border: #e1e5ec;
    --nt-muted: #71809a;
    --nt-shadow: 0 16px 42px rgba(18, 33, 63, .08);
}

html, body {
    margin: 0 !important;
    background: var(--nt-bg) !important;
}

.gradio-container {
    width: 100% !important;
    max-width: none !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    background: var(--nt-bg) !important;
    color: var(--nt-navy) !important;
}

.contain {
    max-width: none !important;
}

footer {
    display: none !important;
}

/* =========================
   Login / Signup
   ========================= */

#auth_page {
    width: min(540px, calc(100% - 28px)) !important;
    max-width: 540px !important;
    margin: 6vh auto !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: var(--nt-surface) !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--nt-shadow) !important;
}

#auth_brand {
    padding: 34px 30px 26px !important;
    text-align: center !important;
    background: #e9ecf1 !important;
}

#auth_brand .brand-logo {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 6px;
}

#auth_brand .brand-symbol {
    color: var(--nt-navy);
    font-size: 24px;
    font-weight: 800;
}

#auth_brand h1 {
    margin: 0 !important;
    color: var(--nt-navy) !important;
    font-size: 34px !important;
    font-weight: 780 !important;
    letter-spacing: -.7px !important;
}

#auth_brand .brand-subtitle {
    margin: 8px 0 5px !important;
    color: var(--nt-navy) !important;
    font-size: 15px !important;
    font-weight: 750 !important;
}

#auth_brand .brand-description {
    max-width: 430px;
    margin: 0 auto;
    color: var(--nt-muted);
    font-size: 13px;
    line-height: 1.5;
}

#auth_tabs {
    gap: 0 !important;
    margin: 0 !important;
}

#auth_tabs button {
    min-height: 44px !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    font-weight: 750 !important;
}

#login_tab_btn {
    background: var(--nt-indigo) !important;
    color: #fff !important;
}

#signup_tab_btn {
    background: #fff !important;
    color: var(--nt-navy) !important;
}

#login_panel, #signup_panel {
    padding: 22px 30px 28px !important;
    background: #fff !important;
    border: 0 !important;
}

#login_panel h3, #signup_panel h3 {
    margin: 0 0 14px !important;
    color: var(--nt-navy) !important;
    font-size: 18px !important;
}

#auth_page input {
    min-height: 44px !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    background: #fff !important;
}

#auth_page input:focus {
    border-color: var(--nt-indigo) !important;
    box-shadow: 0 0 0 3px rgba(91,92,226,.12) !important;
}

#auth_page label span {
    color: var(--nt-navy) !important;
    font-weight: 650 !important;
}

#login_btn, #signup_btn {
    width: 100% !important;
    min-height: 44px !important;
    margin-top: 5px !important;
    border: 0 !important;
    border-radius: 8px !important;
    background: var(--nt-indigo) !important;
    color: #fff !important;
    font-weight: 750 !important;
}

#login_btn:hover, #signup_btn:hover {
    background: var(--nt-indigo-dark) !important;
}

/* =========================
   Dashboard shell
   ========================= */

#dashboard {
    width: min(1040px, calc(100% - 32px)) !important;
    max-width: 1040px !important;
    margin: 24px auto 36px !important;
    padding: 0 0 18px !important;
}

#top_header {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    min-height: 56px !important;
    padding: 0 2px !important;
    margin-bottom: 14px !important;
}

#top_brand {
    min-width: 0 !important;
    padding: 0 !important;
}

#top_brand .top-brand-wrap {
    display: flex;
    align-items: center;
    gap: 9px;
    white-space: nowrap;
}

#top_brand .top-symbol {
    color: var(--nt-navy);
    font-size: 21px;
    font-weight: 800;
}

#top_brand h2 {
    margin: 0 !important;
    color: var(--nt-navy) !important;
    font-size: 21px !important;
    font-weight: 780 !important;
    letter-spacing: -.35px !important;
}

#user_status {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    min-width: 105px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: var(--nt-navy) !important;
    font-size: 13px !important;
}

#top_header > button {
    flex: 0 0 auto !important;
    width: 118px !important;
    min-height: 40px !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 8px !important;
    background: #fff !important;
    color: var(--nt-navy) !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 7px rgba(18,33,63,.04) !important;
}

#top_header > button:hover {
    background: #f7f8fb !important;
    border-color: #cfd5df !important;
}

#top_header > button:last-child {
    color: #fff !important;
    background: var(--nt-indigo) !important;
    border-color: var(--nt-indigo) !important;
}

#top_header > button:last-child:hover {
    background: var(--nt-indigo-dark) !important;
}

/* =========================
   Hero / intro
   ========================= */

#intro {
    margin-bottom: 14px !important;
    padding: 4px 2px 0 !important;
}

#intro .hero {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
}

#intro h1 {
    margin: 0 !important;
    color: var(--nt-navy) !important;
    font-size: 30px !important;
    line-height: 1.08 !important;
    font-weight: 800 !important;
    letter-spacing: -.7px !important;
}

#intro .intro-subtitle {
    margin: 6px 0 8px !important;
    color: var(--nt-navy-2) !important;
    font-size: 14px !important;
    font-weight: 650 !important;
}

#intro .capabilities {
    color: var(--nt-muted) !important;
    font-size: 12.5px !important;
    font-weight: 550 !important;
}

/* =========================
   Chat card
   ========================= */

#chat_shell {
    position: relative !important;
    overflow: hidden !important;
    background: #fff !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 13px !important;
    box-shadow: 0 12px 30px rgba(18,33,63,.055) !important;
}

#chat_shell::before {
    content: "ASSISTANT";
    position: absolute;
    top: 12px;
    left: 16px;
    z-index: 5;
    padding: 4px 8px;
    border-radius: 5px;
    background: #f1f3f8;
    color: var(--nt-muted);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .9px;
    pointer-events: none;
}

#chatbot {
    height: 430px !important;
    min-height: 430px !important;
    border: 0 !important;
    border-radius: 13px !important;
    background: #fff !important;
}

#chatbot .message {
    font-size: 14px !important;
    line-height: 1.55 !important;
}

#chatbot .prose {
    color: var(--nt-navy) !important;
}

#chatbot .avatar-container {
    border-radius: 50% !important;
}

/* =========================
   Composer
   ========================= */

#composer {
    align-items: stretch !important;
    gap: 9px !important;
    margin-top: 11px !important;
}

#message_box textarea {
    min-height: 48px !important;
    padding: 12px 14px !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 9px !important;
    background: #fff !important;
    color: var(--nt-navy) !important;
    font-size: 14px !important;
    box-shadow: 0 2px 8px rgba(18,33,63,.025) !important;
}

#message_box textarea:focus {
    border-color: var(--nt-indigo) !important;
    box-shadow: 0 0 0 3px rgba(91,92,226,.10) !important;
}

#send_button {
    width: 102px !important;
    min-width: 102px !important;
    min-height: 48px !important;
    border: 0 !important;
    border-radius: 9px !important;
    background: var(--nt-indigo) !important;
    color: #fff !important;
    font-weight: 760 !important;
}

#send_button:hover {
    background: var(--nt-indigo-dark) !important;
}

/* =========================
   Quick action toolbar
   ========================= */

#quick_actions {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 0 !important;
    margin-top: 10px !important;
    overflow: hidden !important;
    background: #fff !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 8px rgba(18,33,63,.025) !important;
}

#quick_actions button {
    min-height: 50px !important;
    border: 0 !important;
    border-right: 1px solid var(--nt-border) !important;
    border-radius: 0 !important;
    background: #fff !important;
    color: var(--nt-navy) !important;
    font-size: 13px !important;
    font-weight: 720 !important;
}

#quick_actions button:last-child {
    border-right: 0 !important;
}

#quick_actions button:hover {
    background: #f7f8fc !important;
    color: var(--nt-indigo-dark) !important;
}

/* =========================
   Document management
   ========================= */

#document_management {
    margin-top: 10px !important;
    overflow: hidden !important;
    background: #fff !important;
    border: 1px solid var(--nt-border) !important;
    border-radius: 9px !important;
}

#document_management > button {
    min-height: 47px !important;
    border: 0 !important;
    border-radius: 0 !important;
    background: #fff !important;
    color: var(--nt-navy) !important;
    font-weight: 720 !important;
}

#document_management > div {
    padding: 14px !important;
    border-top: 1px solid var(--nt-border) !important;
}

#document_management button {
    border-radius: 7px !important;
}

/* =========================
   Responsive
   ========================= */

@media (max-width: 800px) {
    #dashboard {
        width: calc(100% - 20px) !important;
        margin-top: 12px !important;
    }

    #top_header {
        flex-wrap: wrap !important;
        align-items: center !important;
    }

    #top_brand {
        flex: 1 1 100% !important;
    }

    #user_status {
        justify-content: flex-start !important;
        min-width: auto !important;
    }

    #top_header > button {
        flex: 1 1 0 !important;
        width: auto !important;
    }

    #chatbot {
        height: 390px !important;
        min-height: 390px !important;
    }

    #quick_actions {
        grid-template-columns: repeat(2, 1fr) !important;
    }

    #quick_actions button:nth-child(2) {
        border-right: 0 !important;
    }

    #quick_actions button:nth-child(-n+2) {
        border-bottom: 1px solid var(--nt-border) !important;
    }
}

@media (max-width: 500px) {
    #auth_page {
        width: calc(100% - 18px) !important;
        margin: 14px auto !important;
    }

    #auth_brand,
    #login_panel,
    #signup_panel {
        padding-left: 20px !important;
        padding-right: 20px !important;
    }

    #top_brand h2 {
        font-size: 19px !important;
    }

    #intro h1 {
        font-size: 25px !important;
    }

    #chatbot {
        height: 360px !important;
        min-height: 360px !important;
    }

    #composer {
        flex-direction: column !important;
    }

    #send_button {
        width: 100% !important;
    }

    #quick_actions {
        grid-template-columns: 1fr !important;
    }

    #quick_actions button {
        border-right: 0 !important;
        border-bottom: 1px solid var(--nt-border) !important;
    }

    #quick_actions button:last-child {
        border-bottom: 0 !important;
    }
}
"""

# ============================================================
# HELPERS
# ============================================================


def get_error_detail(response, default):
    try:
        return response.json().get("detail", default)
    except Exception:
        return default


def create_session():
    return str(uuid.uuid4())


def _login_failed(message):
    """Return value for a failed login (7 outputs, stay on auth page)."""
    return (
        None,
        "",
        gr.update(visible=True),   # auth_page
        gr.update(visible=False),  # dashboard
        gr.update(visible=True),   # login_panel
        gr.update(visible=False),  # signup_panel
        message,
    )


# ============================================================
# AUTH
# ============================================================


def register_user(username, password):
    username = (username or "").strip()
    password = password or ""

    if not username:
        return "❌ Username is required."

    if len(password) < 8:
        return "❌ Password must be at least 8 characters."

    try:
        response = requests.post(
            REGISTER_URL,
            json={"username": username, "password": password},
            timeout=10,
        )
    except requests.RequestException as e:
        return f"❌ API connection error: {e}"

    if response.status_code != 200:
        return "❌ " + get_error_detail(response, "Registration failed.")

    return "✅ Account created successfully. Now switch to Login."


def login(username, password):
    username = (username or "").strip()
    password = password or ""

    if not username or not password:
        return _login_failed("❌ Username and password are required.")

    try:
        response = requests.post(
            LOGIN_URL,
            json={"username": username, "password": password},
            timeout=10,
        )
    except requests.RequestException as e:
        return _login_failed(f"❌ API connection error: {e}")

    if response.status_code != 200:
        return _login_failed("❌ " + get_error_detail(response, "Login failed."))

    try:
        token = response.json()["access_token"]
    except Exception:
        return _login_failed("❌ Invalid response from login API.")

    return (
        token,
        f"👤 **{username}**",
        gr.update(visible=False),  # auth_page
        gr.update(visible=True),   # dashboard
        gr.update(visible=True),   # login_panel (reset for next time)
        gr.update(visible=False),  # signup_panel
        "",
    )


def logout():
    return (
        None,                      # token_state
        gr.update(visible=True),   # auth_page
        gr.update(visible=False),  # dashboard
        gr.update(visible=True),   # login_panel
        gr.update(visible=False),  # signup_panel
        "Logged out.",             # login_status
        [],                        # chatbot
        create_session(),          # session_id
        "",                        # login_password
        "",                        # user_status
    )


def show_login():
    return (
        gr.update(visible=True),
        gr.update(visible=False),
        "",
    )


def show_signup():
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        "",
    )


# ============================================================
# CHAT
# ============================================================


def _reply(history, message, answer, session_id):
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return history, "", session_id


def chat(message, history, token, session_id):
    history = history or []
    message = (message or "").strip()

    if not message:
        return history, "", session_id

    if not session_id:
        session_id = create_session()

    if not token:
        return _reply(history, message, "❌ Please login first.", session_id)

    try:
        response = requests.post(
            CHAT_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={"question": message, "session_id": session_id},
            timeout=60,
        )
    except requests.RequestException as e:
        return _reply(history, message, f"❌ Connection error: {e}", session_id)

    if response.status_code == 401:
        return _reply(
            history, message, "❌ Session expired. Please login again.", session_id
        )

    if response.status_code != 200:
        return _reply(
            history,
            message,
            "❌ " + get_error_detail(response, "Request failed."),
            session_id,
        )

    try:
        answer = response.json()["answer"]
    except Exception:
        answer = "❌ Invalid response from server."

    return _reply(history, message, answer, session_id)


def clear_chat():
    return [], create_session()


# ============================================================
# DOCUMENT UPLOAD
# ============================================================


def upload_document(file, token):
    if file is None:
        return "❌ Select a PDF or DOCX file."

    if not token:
        return "❌ Please login first."

    file_path = file if isinstance(file, str) else getattr(file, "name", None)

    if not file_path:
        return "❌ Could not read the selected file."

    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                UPLOAD_URL,
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (os.path.basename(file_path), f)},
                timeout=120,
            )
    except (requests.RequestException, OSError) as e:
        return f"❌ Upload error: {e}"

    if response.status_code == 401:
        return "❌ Session expired. Please login again."

    if response.status_code != 200:
        return "❌ " + get_error_detail(response, "Upload failed.")

    try:
        data = response.json()
        return f"✅ Uploaded and indexed: {data['filename']}"
    except Exception:
        return "✅ Document uploaded successfully."


# ============================================================
# QUICK ACTIONS
# ============================================================


def policy_question():
    return "How many annual leaves does a confirmed employee get?"


def ticket_question():
    return "Create an IT ticket for VPN not working with high priority."


def status_question():
    return "What is the status of IT-0001?"


def list_question():
    return "Show me all IT tickets."


# ============================================================
# CHATBOT CONFIG
# ============================================================

chatbot_kwargs = {
    "height": 430,
    "show_label": False,
    "elem_id": "chatbot",
    "show_copy_button": True,
    "placeholder": (
        "## ✻ How can I help you today?\n\n"
        "Ask about HR policies, raise an IT ticket, "
        "or check the status of one."
    ),
    "type": "messages",
}

if os.path.exists("assets/profile.png") and os.path.exists("assets/assistant.png"):
    chatbot_kwargs["avatar_images"] = [
        "assets/profile.png",
        "assets/assistant.png",
    ]

# Drop any kwargs the installed Gradio version doesn't support
try:
    _supported = inspect.signature(gr.Chatbot.__init__).parameters
    chatbot_kwargs = {k: v for k, v in chatbot_kwargs.items() if k in _supported}
except Exception:
    pass

# ============================================================
# THEME
# ============================================================

theme = gr.themes.Soft()

# ============================================================
# GRADIO APP
# ============================================================

with gr.Blocks(
    title="NovaTech Enterprise Assistant",
    theme=theme,
    css=css,
) as demo:

    token_state = gr.State(None)
    session_id = gr.State(None)

    # --------------------------------------------------------
    # AUTH PAGE
    # --------------------------------------------------------

    with gr.Group(visible=True, elem_id="auth_page") as auth_page:

        gr.HTML(
            """
            <div class="brand-logo">
                <span class="brand-symbol">◇</span>
                <span style="font-size: 34px; font-weight: 750; color: #14213d;">
                    NovaTech
                </span>
            </div>
            <div class="brand-subtitle">Enterprise Knowledge &amp; Action Assistant</div>
            <div class="brand-description">
                Secure company knowledge, HR information and IT support in one place.
            </div>
            """,
            elem_id="auth_brand",
        )

        with gr.Row(elem_id="auth_tabs"):
            login_tab_btn = gr.Button("🔐 Login", variant="primary", elem_id="login_tab_btn")
            signup_tab_btn = gr.Button("🆕 Sign Up", elem_id="signup_tab_btn")

        with gr.Group(visible=True, elem_id="login_panel") as login_panel:
            gr.Markdown("### Welcome back")

            login_username = gr.Textbox(
                label="Username",
                placeholder="Enter username",
                autofocus=True,
            )
            login_password = gr.Textbox(
                label="Password",
                placeholder="Enter password",
                type="password",
            )
            login_btn = gr.Button(
                "Login",
                variant="primary",
                elem_id="login_btn",
            )
            login_status = gr.Markdown(elem_id="login_status")

        with gr.Group(visible=False, elem_id="signup_panel") as signup_panel:
            gr.Markdown("### Create your account")

            signup_username = gr.Textbox(
                label="Username",
                placeholder="Choose username",
            )
            signup_password = gr.Textbox(
                label="Password",
                placeholder="Minimum 8 characters",
                type="password",
            )
            signup_btn = gr.Button(
                "Create Account",
                variant="primary",
                elem_id="signup_btn",
            )
            signup_status = gr.Markdown(elem_id="signup_status")

    # --------------------------------------------------------
    # MAIN DASHBOARD
    # --------------------------------------------------------

    with gr.Group(visible=False, elem_id="dashboard") as dashboard:

        # Compact application header
        with gr.Row(elem_id="top_header"):
            gr.HTML(
                """
                <div class="top-brand-wrap">
                    <span class="top-symbol">◇</span>
                    <h2>NovaTech Assistant</h2>
                </div>
                """,
                elem_id="top_brand",
                scale=5,
            )

            user_status = gr.Markdown(
                "👤 User",
                elem_id="user_status",
            )

            clear_btn = gr.Button(
                "＋ New Chat",
                scale=0,
            )

            logout_btn = gr.Button(
                "Logout",
                scale=0,
            )

        # Product hero
        gr.HTML(
            """
            <div class="hero">
                <div>
                    <h1>NovaTech Assistant</h1>
                    <div class="intro-subtitle">
                        Enterprise Knowledge &amp; Action Assistant
                    </div>
                    <div class="capabilities">
                        • Secure API&nbsp;&nbsp;&nbsp; • Knowledge Base&nbsp;&nbsp;&nbsp; • IT Support
                    </div>
                </div>
            </div>
            """,
            elem_id="intro",
        )

        # Main chat workspace
        with gr.Group(elem_id="chat_shell"):
            chatbot = gr.Chatbot(**chatbot_kwargs)

        # Composer
        with gr.Row(elem_id="composer"):
            msg = gr.Textbox(
                label="",
                show_label=False,
                placeholder="Ask NovaTech anything...",
                lines=1,
                max_lines=5,
                elem_id="message_box",
                scale=1,
            )
            send_btn = gr.Button(
                "➤  Send",
                variant="primary",
                elem_id="send_button",
                scale=0,
            )

        # Quick actions
        with gr.Row(elem_id="quick_actions"):
            policy_btn = gr.Button("📚  Policies")
            ticket_btn = gr.Button("🎫  Create Ticket")
            status_btn = gr.Button("🔎  Ticket Status")
            list_btn = gr.Button("📋  All Tickets")

        # Document management
        with gr.Accordion(
            "📄  Document Management",
            open=False,
            elem_id="document_management",
        ):
            upload_file = gr.File(
                label="Upload PDF or DOCX",
                file_types=[".pdf", ".docx"],
                type="filepath",
            )
            upload_btn = gr.Button("Upload & Index")
            upload_status = gr.Markdown()

    # --------------------------------------------------------
    # EVENTS — unchanged backend behavior
    # --------------------------------------------------------

    login_tab_btn.click(
        show_login,
        outputs=[login_panel, signup_panel, signup_status],
    )

    signup_tab_btn.click(
        show_signup,
        outputs=[login_panel, signup_panel, signup_status],
    )

    login_outputs = [
        token_state,
        user_status,
        auth_page,
        dashboard,
        login_panel,
        signup_panel,
        login_status,
    ]

    login_btn.click(
        login,
        inputs=[login_username, login_password],
        outputs=login_outputs,
    )

    # Enter inside password field = Login
    login_password.submit(
        login,
        inputs=[login_username, login_password],
        outputs=login_outputs,
    )

    signup_btn.click(
        register_user,
        inputs=[signup_username, signup_password],
        outputs=signup_status,
    )

    logout_btn.click(
        logout,
        outputs=[
            token_state,
            auth_page,
            dashboard,
            login_panel,
            signup_panel,
            login_status,
            chatbot,
            session_id,
            login_password,
            user_status,
        ],
    )

    chat_inputs = [msg, chatbot, token_state, session_id]
    chat_outputs = [chatbot, msg, session_id]

    send_btn.click(chat, inputs=chat_inputs, outputs=chat_outputs)

    # Enter = send
    msg.submit(chat, inputs=chat_inputs, outputs=chat_outputs)

    # New chat
    clear_btn.click(clear_chat, outputs=[chatbot, session_id])

    policy_btn.click(policy_question, outputs=msg)
    ticket_btn.click(ticket_question, outputs=msg)
    status_btn.click(status_question, outputs=msg)
    list_btn.click(list_question, outputs=msg)

    upload_btn.click(
        upload_document,
        inputs=[upload_file, token_state],
        outputs=upload_status,
    )

    demo.load(create_session, outputs=session_id)

if __name__ == "__main__":
    demo.launch(share=True)
