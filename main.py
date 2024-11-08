import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.stylable_container import stylable_container
import yaml

# Set page configuration
st.set_page_config(page_title="TERROP", page_icon='img10.jpg', layout="wide")



# Custom CSS to hide the Streamlit footer
hide_streamlit_style = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#names = ["Obinna Nwachukwu", "Jane Francis"]
#usernames = ["obigod", "jane"]
# Hashed passwords (replace with securely generated hashed passwords)
#hashed_passwords = stauth.Hasher(['obigod123', 'jane123']).generate()
#st.write(hashed_passwords)


# Define user information
#names = ["Obinna Nwachukwu", "Jane Francis"]
#usernames = ["obigod", "jane"]

# Generate hashed passwords
# Replace 'obigod123' and 'jane123' with securely hashed passwords in production
#plaintext_passwords = ['obigod123', 'jane123']
#hashed_passwords = stauth.Hasher(plaintext_passwords).generate()


from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    #config['preauthorized']
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
                </style>
                """
    st.markdown(change_singup_color, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.session_state.get('logged_in', False):
            st.subheader("You are logged in.")
            if st.button("Logout", key="logout_button"):
                # Logout and reset session
                authenticator.logout('Logout', 'main')
                st.session_state.clear()  # Clear all session states
                st.session_state['logged_in'] = False  # Ensure logged_in is set to False
                st.rerun()  # Rerun to reflect logout state
        else:
            # Display login form
            name, authentication_status, username = authenticator.login("Login", location="main")
            

            # Check the authentication status 
            if authentication_status:
                st.session_state.logged_in = True
                st.session_state.user_info = name
                st.markdown(
                    """
                    <style>
                    .st-emotion-cache-1rsyhoq.e1nzilvr5{
                        color: #dfe0d3;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.success(f"Logged in successfully! Welcome, {name}")
            elif authentication_status == False:
                st.error("Username/password is incorrect")
            elif authentication_status == None:
                st.warning("Enter your username and password. If you don't have your login credentials, please contact the administrator for assistance")


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

            remove_bg_color = """
                <style>
                .stApp {
                    background-color: transparent;
                }
                </style>
                """
            st.markdown(remove_bg_color, unsafe_allow_html=True)

            @st.cache_data
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
                </style>
            """
            st.markdown(hide_menu_style, unsafe_allow_html=True)

            app = option_menu(
                menu_title='TERROP',
                options=['Home', 'Visualizations', 'Prediction', 'Make a Report', 'About', 'Login/Signup'],
                icons=['house-fill', 'bar-chart-fill', 'globe', 'x-diamond-fill', 'info-circle-fill', 'person-fill'],
                menu_icon="globe-europe-africa",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "5!important", "background-color": 'white'},
                    "icon": {"color": "#956241", "font-size": "23px"},
                    "nav-link": {"color": "#473021", "font-size": "20px", "font-weight": "bold", "centre": "left", "--hover-color": "#d2c8c2"},
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
            elif app == "Login/Signup":
                display_auth_form()

    MultiApp().run()

# Main Entry
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    app_main()
