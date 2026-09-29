import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import json
import os

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

for key in ["f1","f2","f3"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ================= USER STORAGE =================
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        return json.load(open(USER_FILE))
    return {}

def save_users(users):
    json.dump(users, open(USER_FILE, "w"))

users = load_users()

def signup(u, p):
    if u in users:
        return False
    users[u] = p
    save_users(users)
    return True

def login(u, p):
    return users.get(u) == p

# ================= LOAD MODELS =================
diabetes_model = pickle.load(open('rf_model.pkl', 'rb'))
diabetes_scaler = pickle.load(open('scaler.pkl', 'rb'))
heart_model = pickle.load(open('heart_disease_model.sav','rb'))

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background:
    linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://img.freepik.com/premium-vector/medical-healthcare-diagnostics-disease-concept-design-tech-background_808699-288.jpg");
    background-size: cover;
    background-position: center;
    color: white;
}

/* NAVBAR */
.navbar {
    display: flex;
    justify-content: space-between;
    padding: 15px 40px;
    align-items: center;
}
.nav-links {
    display: flex;
    gap: 25px;
}

/* BUTTON SAME SIZE */
.stButton>button {
    background: linear-gradient(135deg, #4CAF50, #2ecc71);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    width: 180px;
    height: 45px;
    font-size: 15px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.08);
}

/* HERO CARD */
.hero-card {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ================= LANDING PAGE =================
if st.session_state.page == "home":

    st.markdown("""
    <div class="navbar">
        <h2>Health AI</h2>
    </div>
    """, unsafe_allow_html=True)

    # CLICKABLE NAV
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(" Home"):
            st.session_state.f1 = not st.session_state.f1
        if st.session_state.f1:
            st.info("Welcome to AI Health Prediction System")

    with c2:
        if st.button(" About"):
            st.session_state.f2 = not st.session_state.f2
        if st.session_state.f2:
            st.info("ML based system for Diabetes & Heart prediction")

    with c3:
        if st.button(" Features"):
            st.session_state.f3 = not st.session_state.f3
        if st.session_state.f3:
            st.info("✔ Accurate Models\n✔ Easy Input\n✔ Instant Results")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("<h1>Multi-Disease Prediction System</h1>", unsafe_allow_html=True)
        st.markdown("<h3>Predict Your Health Risks with AI</h3>", unsafe_allow_html=True)
        st.write("Early detection of Diabetes and Heart Disease using Machine Learning")

        if st.button("Start Now"):
            st.session_state.page = "auth"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="hero-card">
            <h3>✔ Accurate Models</h3>
            <p>High accuracy ML predictions</p>
            <br>
            <h3>✔ Easy Input</h3>
            <p>User friendly design</p>
            <br>
            <h3>✔ Instant Results</h3>
            <p>Fast predictions</p>
        </div>
        """, unsafe_allow_html=True)

# ================= AUTH =================
elif st.session_state.page == "auth":

    col_back, _ = st.columns([2,8])
    with col_back:
        if st.button("← Home"):
            st.session_state.page = "home"
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6a11cb, #2575fc); padding:30px; border-radius:20px;">
        <h1>Welcome </h1>
        <p>Access your AI Health Dashboard</p>
        <br>
        ✓ Diabetes Prediction<br><br>
        ✓ Heart Disease Detection<br><br>
        ✓ Instant Results
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h2>Secure Access</h2>", unsafe_allow_html=True)

        choice = st.radio("Select Option", ["Login", "Signup"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if choice == "Signup":
            if st.button("Create Account"):
                if signup(username, password):
                    st.success("Account created")
                else:
                    st.error("Username already exists")

        else:
            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.page = "main"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ================= MAIN =================
elif st.session_state.page == "main" and st.session_state.logged_in:

    col_back, _ = st.columns([2,8])
    with col_back:
        if st.button("← Home"):
            st.session_state.page = "home"
            st.session_state.logged_in = False
            st.rerun()

    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System',
                              ['Diabetes Prediction',
                               'Heart Disease Prediction',
                               'Predict Both'],
                              icons=['activity','heart','cpu'],
                              default_index=0)

    st.title("Multiple Disease Prediction System")

    # ================= DIABETES =================
    if selected == 'Diabetes Prediction':

        st.subheader('Diabetes Prediction')

        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose')
        with col3:
            BP = st.text_input('Blood Pressure')

        with col1:
            Skin = st.text_input('Skin Thickness')
        with col2:
            Insulin = st.text_input('Insulin')
        with col3:
            BMI = st.text_input('BMI')

        with col1:
            DPF = st.text_input('DPF')
        with col2:
            Age = st.text_input('Age')

        if st.button("Predict Diabetes"):
            try:
                data = [[float(Pregnancies), float(Glucose), float(BP),
                         float(Skin), float(Insulin), float(BMI),
                         float(DPF), float(Age)]]

                scaled = diabetes_scaler.transform(data)
                prob = diabetes_model.predict_proba(scaled)[0][1]*100

                if prob > 50:
                    st.error(f"High Risk: {prob:.2f}%")
                else:
                    st.success(f"Low Risk: {prob:.2f}%")
            except:
                st.error("Enter valid values")

    # ================= HEART =================
    elif selected == 'Heart Disease Prediction':

        st.subheader('Heart Disease Prediction')

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex')
        with col3:
            cp = st.text_input('Chest Pain')

        with col1:
            bp = st.text_input('BP')
        with col2:
            chol = st.text_input('Cholesterol')
        with col3:
            fbs = st.text_input('FBS')

        with col1:
            rest = st.text_input('Rest ECG')
        with col2:
            thalach = st.text_input('Max HR')
        with col3:
            exang = st.text_input('Angina')

        with col1:
            old = st.text_input('Oldpeak')
        with col2:
            slope = st.text_input('Slope')
        with col3:
            ca = st.text_input('CA')

        with col1:
            thal = st.text_input('Thal')

        if st.button("Predict Heart"):
            try:
                data = [[float(age), float(sex), float(cp),
                         float(bp), float(chol), float(fbs),
                         float(rest), float(thalach),
                         float(exang), float(old),
                         float(slope), float(ca), float(thal)]]

                prob = heart_model.predict_proba(data)[0][1] * 100

                if prob > 50:
                    st.error(f"High Risk of Heart Disease: {prob:.2f}%")
                else:
                    st.success(f"Low Risk of Heart Disease: {prob:.2f}%")

            except:
                st.error("Enter valid values")

    # ================= BOTH =================
    elif selected == 'Predict Both':

        st.subheader('Predict Both')

        col1, col2 = st.columns(2)

        with col1:
            age = st.text_input('Age')
            bp = st.text_input('Blood Pressure')
            glucose = st.text_input('Glucose')

        with col2:
            chol = st.text_input('Cholesterol')
            bmi = st.text_input('BMI')

        if st.button("Predict Both"):
            try:
                d_data = [[1, float(glucose), float(bp), 20, 80, float(bmi), 0.5, float(age)]]
                d_scaled = diabetes_scaler.transform(d_data)
                d_prob = diabetes_model.predict_proba(d_scaled)[0][1]*100

                h_data = [[float(age), 1, 0, float(bp), float(chol), 0,
                           0, 150, 0, 1.0, 1, 0, 1]]
                h_prob = heart_model.predict_proba(h_data)[0][1]*100

                c1, c2 = st.columns(2)

                with c1:
                    if d_prob > 50:
                        st.error(f"Diabetes High Risk: {d_prob:.2f}%")
                    else:
                        st.success(f"Diabetes Low Risk: {d_prob:.2f}%")

                with c2:
                    if h_prob > 50:
                        st.error(f"Heart High Risk: {h_prob:.2f}%")
                    else:
                        st.success(f"Heart Low Risk: {h_prob:.2f}%")

            except:
                st.error("Enter valid values")