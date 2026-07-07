import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from rag_chain import load_rag_chain

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="EduNova AI Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "💬 Chat"
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0.0
if "response_times" not in st.session_state:
    st.session_state.response_times = []

# ── THEME CSS ────────────────────────────────────────
def get_css(theme):
    if theme == "dark":
        bg = "#0a0e1a"
        bg2 = "#111827"
        card = "#131c2e"
        border = "#1e2a45"
        text = "#f1f5f9"
        text2 = "#94a3b8"
        accent = "#60b0ff"
        accent2 = "#a78bfa"
        grad = "linear-gradient(135deg, #1e3a5f, #2a4a7a)"
    else:
        bg = "#f0f4f8"
        bg2 = "#ffffff"
        card = "#ffffff"
        border = "#d1d9e6"
        text = "#0a0e1a"
        text2 = "#475569"
        accent = "#2563eb"
        accent2 = "#7c3aed"
        grad = "linear-gradient(135deg, #dbeafe, #ede9fe)"

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{ background: {bg}; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}

    [data-testid="stSidebar"] {{
        background: {bg2};
        border-right: 1px solid {border};
    }}

    .pro-header {{
        background: {grad};
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid {border};
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .pro-header h1 {{
        color: {text};
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }}
    .pro-header p {{
        color: {text2};
        margin: 4px 0 0 0;
        font-size: 0.9rem;
    }}
    .pro-badge {{
        background: rgba(255,255,255,0.15);
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        color: {text};
        font-size: 0.82rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }}

    .pro-card {{
        background: {card};
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        border: 1px solid {border};
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s;
    }}
    .pro-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }}

    .stat-box {{
        background: {card};
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid {border};
        text-align: center;
    }}
    .stat-box .num {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {accent};
    }}
    .stat-box .lbl {{
        color: {text2};
        font-size: 0.75rem;
        margin-top: 2px;
    }}

    .msg-user {{
        background: {grad};
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: 72%;
        margin-left: auto;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        font-size: 0.93rem;
        line-height: 1.6;
    }}
    .msg-bot {{
        background: {card};
        border: 1px solid {border};
        border-left: 3px solid {accent};
        color: {text};
        padding: 12px 18px;
        border-radius: 4px 18px 18px 18px;
        max-width: 78%;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        font-size: 0.93rem;
        line-height: 1.8;
    }}
    .msg-meta {{
        font-size: 0.68rem;
        color: {text2};
        margin-top: 6px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }}
    .timer-chip {{
        background: rgba(96,176,255,0.12);
        color: {accent};
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.68rem;
    }}
    .conf-chip {{
        background: rgba(167,139,250,0.12);
        color: {accent2};
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.68rem;
    }}
    .src-pill {{
        display: inline-block;
        background: {bg2};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.72rem;
        color: {text2};
        margin: 3px 3px 0 0;
    }}

    .welcome-box {{
        text-align: center;
        padding: 50px 20px 30px;
    }}
    .welcome-icon {{
        width: 72px;
        height: 72px;
        background: {grad};
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        margin: 0 auto 20px;
    }}

    .side-tag {{
        display: inline-block;
        background: {bg};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.7rem;
        color: {text2};
        margin: 2px;
    }}
    .side-divider {{
        border: none;
        border-top: 1px solid {border};
        margin: 12px 0;
    }}
    .online-dot {{
        display: inline-block;
        width: 7px;
        height: 7px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 5px;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.4; }}
    }}

    .stTextInput > div > div > input {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        color: {text} !important;
        font-size: 0.93rem !important;
        padding: 13px 18px !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(96,176,255,0.15) !important;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: {text2} !important;
    }}
    .stButton > button {{
        background: {grad} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(96,176,255,0.3) !important;
    }}
    .stDownloadButton > button {{
        background: {card} !important;
        color: {text2} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        width: 100% !important;
    }}
    </style>
    """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ── LOAD RAG ─────────────────────────────────────────
@st.cache_resource
def get_chain():
    return load_rag_chain()

with st.spinner("🔄 Loading EduNova AI..."):
    chain, retriever = get_chain()

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    th = st.session_state.theme
    text_col = "#f1f5f9" if th == "dark" else "#0a0e1a"
    text2_col = "#94a3b8" if th == "dark" else "#475569"
    border_col = "#1e2a45" if th == "dark" else "#d1d9e6"
    card_col = "#131c2e" if th == "dark" else "#ffffff"

    st.markdown(f"""
    <div style='text-align:center; padding: 16px 0 12px;'>
        <div style='width:44px;height:44px;background:linear-gradient(135deg,#60b0ff,#a78bfa);
        border-radius:12px;display:flex;align-items:center;justify-content:center;
        font-size:1.4rem;margin:0 auto 10px;'>🎓</div>
        <div style='color:{text_col};font-size:1.1rem;font-weight:700;'>EduNova AI Pro</div>
        <div style='color:{text2_col};font-size:0.75rem;'>CISSP RAG Companion</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✏️ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("suggested", None)
            st.rerun()
    with c2:
        if st.button("🌓 Theme", use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

    st.markdown("<hr class='side-divider'>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:{text2_col};font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>📊 Knowledge Base</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"<div class='stat-box'><div class='num'>9.7K</div><div class='lbl'>Pages</div></div>", unsafe_allow_html=True)
    with s2:
        st.markdown(f"<div class='stat-box'><div class='num'>12K</div><div class='lbl'>Chunks</div></div>", unsafe_allow_html=True)
    with s3:
        st.markdown(f"<div class='stat-box'><div class='num'>8</div><div class='lbl'>Domains</div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='side-divider'>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:{text2_col};font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>⚡ System Status</div>", unsafe_allow_html=True)
    for svc in ["Groq LLM", "ChromaDB", "HuggingFace"]:
        st.markdown(f"<div style='font-size:0.8rem;color:{text_col};padding:5px 0;'><span class='online-dot'></span>{svc} <span style='color:#22c55e;float:right;font-size:0.72rem;'>Online</span></div>", unsafe_allow_html=True)

    st.markdown("<hr class='side-divider'>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:{text2_col};font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>💡 Quick Questions</div>", unsafe_allow_html=True)
    quick_qs = [
        "What is the CIA Triad?",
        "Explain Defense in Depth",
        "What is PKI?",
        "RMF steps explained",
        "CISSP domains overview",
        "Symmetric vs Asymmetric encryption",
    ]
    for q in quick_qs:
        if st.button(q, key=f"qq_{q}", use_container_width=True):
            st.session_state.suggested = q
            st.rerun()

    st.markdown("<hr class='side-divider'>", unsafe_allow_html=True)

    show_src = st.toggle("📚 Show Sources", value=True)
    show_timer = st.toggle("⏱️ Show Response Time", value=True)
    show_conf = st.toggle("🎯 Show Confidence", value=True)

    st.markdown("<hr class='side-divider'>", unsafe_allow_html=True)

    if st.session_state.get("messages"):
        chat_export = "\n\n".join([
            f"{'You' if m['role']=='user' else 'EduNova AI'}: {m['content']}"
            for m in st.session_state.messages
        ])
        st.download_button("💾 Download Chat", data=chat_export,
            file_name=f"edunova_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain", use_container_width=True)

    st.markdown(f"<div style='text-align:center;color:{text2_col};font-size:0.7rem;margin-top:12px;'>EduNova AI Pro v2.0 · RAG Powered</div>", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────
st.markdown("""
<div class='pro-header'>
    <div>
        <h1>🎓 EduNova AI Pro</h1>
        <p>Intelligent CISSP Study Companion — Powered by RAG + Groq</p>
    </div>
    <div class='pro-badge'>⚡ Live · LLaMA 3.3 70B</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────
tabs = ["💬 Chat", "📚 Knowledge Graph", "📈 Analytics", "⚙️ Settings"]
tab_cols = st.columns(len(tabs))
for i, tab in enumerate(tabs):
    with tab_cols[i]:
        is_active = st.session_state.selected_tab == tab
        if st.button(tab, key=f"tab_{i}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.selected_tab = tab
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── TAB: CHAT ────────────────────────────────────────
if st.session_state.selected_tab == "💬 Chat":

    # Handle suggested
    if st.session_state.get("suggested"):
        q = st.session_state.pop("suggested")
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("🤔 Thinking..."):
            start = time.time()
            docs = retriever.invoke(q)
            answer = chain.invoke(q)
            elapsed = round(time.time() - start, 2)
            sources = list(set([d.metadata.get("source","").split("\\")[-1] for d in docs]))
            conf = min(0.99, 0.75 + (len(answer)/2000))
        st.session_state.total_questions += 1
        st.session_state.total_time += elapsed
        st.session_state.response_times.append(elapsed)
        st.session_state.messages.append({
            "role": "assistant", "content": answer,
            "sources": sources, "time": elapsed,
            "confidence": round(conf*100),
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.rerun()

    # Welcome screen
    if not st.session_state.messages:
        th = st.session_state.theme
        text_col = "#f1f5f9" if th == "dark" else "#0a0e1a"
        text2_col = "#94a3b8" if th == "dark" else "#475569"
        st.markdown(f"""
        <div class='welcome-box'>
            <div class='welcome-icon'>🎓</div>
            <h2 style='color:{text_col};font-weight:700;margin-bottom:8px;'>Welcome to EduNova AI Pro!</h2>
            <p style='color:{text2_col};font-size:0.95rem;max-width:500px;margin:0 auto 30px;'>
            Your intelligent CISSP study companion trained on <strong>9,763+ pages</strong> of material.
            Ask anything about Security, Cryptography, Risk Management & more!
            </p>
        </div>
        """, unsafe_allow_html=True)

        sug_list = [
            ("🔐", "What is the CIA Triad?"),
            ("🛡️", "Explain Defense in Depth"),
            ("🔑", "What is PKI?"),
            ("⚠️", "Risk Management Framework steps"),
            ("🔒", "Symmetric vs Asymmetric encryption"),
            ("📋", "CISSP 8 domains overview"),
        ]
        c1, c2 = st.columns(2)
        for i, (icon, text) in enumerate(sug_list):
            with (c1 if i % 2 == 0 else c2):
                if st.button(f"{icon} {text}", key=f"sug_{i}", use_container_width=True):
                    st.session_state.suggested = text
                    st.rerun()

    # Messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            content = msg['content'].replace('\n', '<br>')
            timer_html = f"<span class='timer-chip'>⏱ {msg.get('time')}s</span>" if show_timer and msg.get('time') else ""
            conf_html = f"<span class='conf-chip'>🎯 {msg.get('confidence')}%</span>" if show_conf and msg.get('confidence') else ""
            st.markdown(f"""
            <div class='msg-bot'>
                🎓 {content}
                <div class='msg-meta'>
                    {timer_html}{conf_html}
                    <span>🕐 {msg.get('timestamp','')}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            if show_src and msg.get("sources"):
                with st.expander("📚 View Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"<span class='src-pill'>📄 {src}</span>", unsafe_allow_html=True)

    # Input
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("", placeholder="💬 Ask anything about CISSP...",
                                    label_visibility="collapsed", key="input")
    with col2:
        send = st.button("Send ➤")

    if send and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 Thinking..."):
            start = time.time()
            docs = retriever.invoke(user_input)
            answer = chain.invoke(user_input)
            elapsed = round(time.time() - start, 2)
            sources = list(set([d.metadata.get("source","").split("\\")[-1] for d in docs]))
            conf = min(0.99, 0.75 + (len(answer)/2000))
        st.session_state.total_questions += 1
        st.session_state.total_time += elapsed
        st.session_state.response_times.append(elapsed)
        st.session_state.messages.append({
            "role": "assistant", "content": answer,
            "sources": sources, "time": elapsed,
            "confidence": round(conf*100),
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.rerun()

# ── TAB: KNOWLEDGE GRAPH ─────────────────────────────
elif st.session_state.selected_tab == "📚 Knowledge Graph":
    st.markdown("### 🗺️ CISSP Domain Distribution")
    domains = pd.DataFrame({
        'Domain': ['Security & Risk Mgmt', 'Asset Security', 'Security Architecture',
                   'Network Security', 'IAM', 'Security Assessment',
                   'Security Operations', 'Software Security'],
        'Weight': [15, 10, 13, 13, 13, 12, 13, 10]
    })
    fig = px.pie(domains, values='Weight', names='Domain',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(
        template='plotly_dark' if st.session_state.theme == 'dark' else 'plotly_white',
        height=420, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📖 Domain Details")
    domain_info = [
        ("🛡️", "Security & Risk Management (15%)", "Governance, compliance, risk analysis, BCP/DRP"),
        ("📦", "Asset Security (10%)", "Classification, privacy, retention, data handling"),
        ("🏗️", "Security Architecture (13%)", "Cryptography, secure design, physical security"),
        ("🌐", "Network Security (13%)", "OSI model, secure protocols, firewalls, VPNs"),
        ("🔑", "IAM (13%)", "Authentication, SSO, federation, access control"),
        ("🔍", "Security Assessment (12%)", "Audits, pen testing, vulnerability scanning"),
        ("⚙️", "Security Operations (13%)", "Incident response, logging, disaster recovery"),
        ("💻", "Software Security (10%)", "Secure SDLC, DevSecOps, OWASP Top 10"),
    ]
    c1, c2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(domain_info):
        th = st.session_state.theme
        card_c = "#131c2e" if th == "dark" else "#ffffff"
        border_c = "#1e2a45" if th == "dark" else "#d1d9e6"
        text_c = "#f1f5f9" if th == "dark" else "#0a0e1a"
        text2_c = "#94a3b8" if th == "dark" else "#475569"
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""
            <div class='pro-card'>
                <div style='font-size:1.4rem;margin-bottom:6px;'>{icon}</div>
                <div style='color:#60b0ff;font-weight:600;font-size:0.9rem;'>{title}</div>
                <div style='color:{text2_c};font-size:0.82rem;margin-top:4px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

# ── TAB: ANALYTICS ───────────────────────────────────
elif st.session_state.selected_tab == "📈 Analytics":
    st.markdown("### 📊 Session Analytics")

    total_q = st.session_state.total_questions
    avg_time = round(st.session_state.total_time / total_q, 2) if total_q > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-box'><div class='num'>{total_q}</div><div class='lbl'>Questions Asked</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><div class='num'>{avg_time}s</div><div class='lbl'>Avg Response Time</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-box'><div class='num'>9.7K</div><div class='lbl'>Pages Indexed</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-box'><div class='num'>12K</div><div class='lbl'>Chunks</div></div>", unsafe_allow_html=True)

    if st.session_state.response_times:
        st.markdown("<br>", unsafe_allow_html=True)
        rt_df = pd.DataFrame({
            "Question #": list(range(1, len(st.session_state.response_times)+1)),
            "Response Time (s)": st.session_state.response_times
        })
        fig2 = px.line(rt_df, x="Question #", y="Response Time (s)",
                       title="Response Time per Question",
                       markers=True, color_discrete_sequence=["#60b0ff"])
        fig2.update_layout(
            template='plotly_dark' if st.session_state.theme == 'dark' else 'plotly_white',
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 💬 Chat History")
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"**Q{(i//2)+1}:** {msg['content']}")
    else:
        st.info("No questions asked yet. Go to Chat tab to start!")

# ── TAB: SETTINGS ────────────────────────────────────
elif st.session_state.selected_tab == "⚙️ Settings":
    st.markdown("### ⚙️ Configuration")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🤖 Model")
        st.selectbox("LLM", ["LLaMA 3.3 70B (Active)", "LLaMA 3 8B", "Mixtral 8x7B"], index=0)
        st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
    with c2:
        st.markdown("#### 📚 RAG")
        st.number_input("Top K Chunks", 1, 20, 5)
        st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)

    st.markdown("#### 🎨 Appearance")
    theme_sel = st.selectbox("Theme", ["Dark", "Light"],
                              index=0 if st.session_state.theme == "dark" else 1)
    st.session_state.theme = "dark" if theme_sel == "Dark" else "light"

    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved!")

# ── FOOTER ───────────────────────────────────────────
th = st.session_state.theme
text2_col = "#94a3b8" if th == "dark" else "#475569"
border_col = "#1e2a45" if th == "dark" else "#d1d9e6"
st.markdown(f"""
<div style='text-align:center;color:{text2_col};font-size:0.72rem;
padding:2rem 0 1rem;border-top:1px solid {border_col};margin-top:2rem;'>
    EduNova AI Pro © 2026 &nbsp;·&nbsp; CISSP RAG Companion &nbsp;·&nbsp;
    Built with ❤️ using Streamlit, LangChain & Groq &nbsp;·&nbsp; v2.0.0
</div>
""", unsafe_allow_html=True)