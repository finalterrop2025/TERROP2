import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.stylable_container import stylable_container

# Set page configuration
st.set_page_config(page_title="TERROP", page_icon='img10.jpg', layout="wide")

# Custom CSS to hide the Streamlit footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load configuration from YAML
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Display the login and registration form
def display_auth_form():
    if st.sidebar.checkbox("Create an account"):
        st.subheader("Register New Account")
        with st.form("registration_form"):
            new_name = st.text_input("Full Name")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_registration = st.form_submit_button("Register")

            if submit_registration:
                if new_password == confirm_password:
                    # Hash and save new user details to YAML
                    hashed_password = stauth.Hasher([new_password]).generate()[0]
                    config['credentials']['usernames'][new_username] = {
                        'name': new_name,
                        'password': hashed_password
                    }
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file)
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Passwords do not match")
    else:
        # Display login form
        name, authentication_status, username = authenticator.login("Login", "main")

        if authentication_status:
            st.success(f"Welcome, {name}")
        elif authentication_status is False:
            st.error("Incorrect username or password.")
        elif authentication_status is None:
            st.warning("Please enter your login details.")

# Main App Logic
def app_main():
    import home, visualizations, prediction, make_report, about
    from streamlit_option_menu import option_menu
    import base64

    class MultiApp:
        def __init__(self):
            self.apps = []

        def add_app(self, title, func):
            self.apps.append({"title": title, "function": func})

        def run(self):
            app = option_menu(
                menu_title='TERROP',
                options=['Home', 'Visualizations', 'Prediction', 'Make a Report', 'About', 'Login/Signup'],
                icons=['house-fill', 'bar-chart-fill', 'globe', 'x-diamond-fill', 'info-circle-fill', 'person-fill'],
                default_index=0,
                orientation="horizontal"
            )
            if app == "Login/Signup":
                display_auth_form()
            else:
                st.write(f"You selected {app}")

    MultiApp().run()

# Main Entry
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    app_main()
