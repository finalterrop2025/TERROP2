import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.stylable_container import stylable_container
import yaml

# Set page config
st.set_page_config(page_title="TERROP", page_icon='imag3.webp', layout="wide")

# Load config from YAML file
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Hash passwords securely (assuming this is for initial password setup)
# This should be done only once during initial setup
# Uncomment this line if you want to hash the passwords for storage
hashed_password = stauth.Hasher.hash_passwords(config['credentials'])

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Function to handle login and signup form display
def display_auth_form():
    change_singup_color = """
                <style>
                .st-emotion-cache-1jmvea6.e1nzilvr4 {
                    color: #efe1cc;
                }
                .st-emotion-cache-vdokb0.e1nzilvr4 {
                    color: #a2a9a9;
                }

                #welcome-to-terrop {
                    font-size: 60px; /* Adjust the size to make it smaller */
                    text-align: center; /* Center the text */
                    font-weight: bold; /* Make it bold */
                    width: 100%; /* Adjust width */
                    margin: 0 auto; /* Center the text block */
                }
                </style>
                """
    st.markdown(change_singup_color, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

        if st.session_state['logged_in']:
            st.subheader("Welcome to TERROP!")
            if st.button("Logout", key="logout_button"):
                authenticator.logout()
                st.session_state.clear()
                st.session_state['logged_in'] = False
                st.session_state['authentication_status'] = None
                st.rerun()
        else:
            try:
                authenticator.login()
            except Exception as e:
                st.error(f"An error occurred during login: {e}")

            if st.session_state['authentication_status']:
                st.session_state['logged_in'] = True
                st.write('Logged in successfully, Welcome to TERROP! ')
            elif st.session_state['authentication_status'] is False:
                st.error('Username/password is incorrect')
            elif st.session_state['authentication_status'] is None:
                st.warning('Please enter your username and password')

# Main App Logic
def app_main():
    import joblib
    import pandas as pd
    from streamlit_option_menu import option_menu
    import sqlite3
    from PIL import Image
    from category_encoders import OrdinalEncoder
    from sklearn.preprocessing import LabelEncoder
    import time
    import base64
    import home, visualizations, prediction, make_report, about

    class MultiApp:
        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({"title": title, "function": func})

        def run(self):
            def get_base64_of_bin_file(bin_file):
                with open(bin_file, 'rb') as f:
                    data = f.read()
                return base64.b64encode(data).decode()

            def set_image_as_page_bg(image_file):
                bin_str = get_base64_of_bin_file(image_file)
                page_bg_img = f'''
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{bin_str}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                }}
                </style>
                '''
                st.markdown(page_bg_img, unsafe_allow_html=True)

            set_image_as_page_bg('images/header.jpg')

            hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #welcome-to-terrop{
                    color: #cfcebd;
                    text-align: center;
                    font-weight: bold;
                    font-size: 80px;
                }
                #your-number-one-terrorism-predictor{
                    color: #f4f4eb;
                    text-align: center;
                    font-weight: bold;
                }

                 [data-testid="appCreatorAvatar"] {
                        display: none;
                    }
                </style>
            """
            st.markdown(hide_menu_style, unsafe_allow_html=True)

            default_tab = (
                0 if 'selected_tab' not in st.session_state
                else ['Home', 'Visualizations', 'Prediction', 'Make a Report', 'About', 'Login'].index(st.session_state['selected_tab'])
            )

            app = option_menu(
                menu_title='TERROP',
                options=['Home', 'Visualizations', 'Prediction', 'Make a Report', 'About', 'Login'],
                icons=['house-fill', 'bar-chart-fill', 'globe', 'x-diamond-fill', 'info-circle-fill', 'person-fill'],
                menu_icon="globe-europe-africa",
                default_index=default_tab,
                orientation="horizontal",
                styles={
                    "container": {"padding": "5!important", "background-color": "white", "border-radius": "15px"},
                    "icon": {"color": "#956241", "font-size": "23px"},
                    "nav-link": {"color": "#473021", "font-size": "20px", "font-weight": "bold", "--hover-color": "#d2c8c2"},
                    "nav-link-selected": {"background-color": "#b79581"},
                    "menu-title": {"font-size": "30px", "color": "#473021", "font-weight": "bold"},
                }
            )

            if app == "Home":
                home.app()
            elif app == "About":
                about.app()
            elif app == "Visualizations":
                if st.session_state.get('logged_in', False):
                    visualizations.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log in to view the Visualizations.")
                    display_auth_form()
            elif app == "Prediction":
                if st.session_state.get('logged_in', False):
                    prediction.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log in to make a prediction.")
                    display_auth_form()
            elif app == "Make a Report":
                if st.session_state.get('logged_in', False):
                    make_report.app()
                else:
                    st.title("WELCOME TO TERROP")
                    st.title("Your number one terrorism predictor")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.warning("Please log in to submit a report.")
                    display_auth_form()
            elif app == "Login":
                display_auth_form()
                if st.session_state.get('logged_in', False):
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col2:
                        if st.button("Go to Homepage", key="homepage_button_login"):
                            st.session_state['selected_tab'] = "Home"
                            st.experimental_rerun()

    MultiApp().run()

# Main Entry
if __name__ == "__main__":
    app_main()
