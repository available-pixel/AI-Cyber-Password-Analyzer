import streamlit as st
import math
import secrets
import string

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Cyber Password Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# DARK CYBER THEME (CSS)
# -----------------------------
st.markdown("""
<style>
@keyframes glow {
    0% { box-shadow: 0 0 5px #7f5cff; }
    50% { box-shadow: 0 0 20px #7f5cff; }
    100% { box-shadow: 0 0 5px #7f5cff; }
}

html, body, [class*="css"] {
    background-color: #0b0f19;
    color: #e6e6ff;
}

.cyber-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #b18cff;
    margin-bottom: 10px;
}

.cyber-subtitle {
    text-align: center;
    font-size: 18px;
    color: #9aa4ff;
    margin-bottom: 20px;
}

.cyber-box {
    background: #12172a;
    padding: 25px;
    border-radius: 12px;
    animation: glow 3s infinite;
}

.metric {
    font-size: 20px;
    margin-bottom: 12px;
}

.good { color: #00ffcc; }
.warn { color: #ffcc00; }
.bad  { color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="cyber-title">Check how fast a hacker can guess your password</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="cyber-subtitle">(Vérifie à quelle vitesse un hacker peut deviner ton mot de passe)</div>',
    unsafe_allow_html=True
)

# -----------------------------
# FUNCTIONS
# -----------------------------
def password_entropy(password):
    space = 0
    if any(c.islower() for c in password):
        space += 26
    if any(c.isupper() for c in password):
        space += 26
    if any(c.isdigit() for c in password):
        space += 10
    if any(not c.isalnum() for c in password):
        space += 32

    if space == 0:
        return 0

    return len(password) * math.log2(space)


def time_to_crack(entropy):
    guesses_per_sec = 1e9
    seconds = (2 ** entropy) / guesses_per_sec

    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"


def generate_strong_password(length=16):
    alphabet = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*()-_=+[]{};:,.?"
    )
    return "".join(secrets.choice(alphabet) for _ in range(length))


# -----------------------------
# LAYOUT
# -----------------------------
left, right = st.columns(2)

# -----------------------------
# LEFT: PASSWORD INPUT
# -----------------------------
with left:
    st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
    st.subheader("🔐 Enter your password")
    st.caption("(Enter your password – nothing is stored)")

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Type a password...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RIGHT: ANALYSIS
# -----------------------------
with right:
    st.markdown('<div class="cyber-box">', unsafe_allow_html=True)
    st.subheader("🧠 AI Cybersecurity Analysis")
    st.caption("(Analyzes your password strength and estimates hack time)")

    if password:
        entropy = password_entropy(password)
        crack_time = time_to_crack(entropy)

        if entropy < 40:
            level = "WEAK ❌"
            color = "bad"
        elif entropy < 70:
            level = "MEDIUM ⚠️"
            color = "warn"
        else:
            level = "STRONG ✅"
            color = "good"

        st.markdown(
            f"<div class='metric'>Entropy: <b>{entropy:.2f}</b> bits</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='metric'>Strength: <span class='{color}'>{level}</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='metric'>Estimated crack time: <b>{crack_time}</b></div>",
            unsafe_allow_html=True
        )
        st.caption("(Temps estimé pour un hacker avec un GPU moderne)")

        # 🔥 AI PASSWORD SUGGESTION (ONLY IF NOT STRONG)
        if level != "STRONG ✅":
            st.markdown("### 🤖 AI Suggested Secure Password")
            st.caption("(Mot de passe généré automatiquement – très difficile à pirater)")
            st.code(generate_strong_password(), language="text")

        else:
            st.success("Excellent password! No AI suggestion needed 💪")

        # Hacker simulation
        st.markdown("### 🧪 Hacker Simulation")
        st.write("""
        - **Brute Force Attack** *(Essai toutes les combinaisons possibles)*
        - **Dictionary Attack** *(Teste des mots connus & mots de passe courants)*
        - **Hybrid Attack** *(Mots + chiffres + symboles)*
        """)

    else:
        st.info("Waiting for password input...")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("⚠️ Educational purpose only | Projet démonstratif en cybersécurité & IA")
