import streamlit as st
from GSpreadFunctions import get_info, get_check_in_status, get_check_in_dict
import gspread
import pandas as pd
import pandasql as ps
import datetime
from streamlit_free_text_select import st_free_text_select
from itertools import chain
import toml

def refresh_clicked():
    st.session_state.refresh = True

def check_in_clicked():
    st.session_state.check_in = True
    st.session_state.series_info = get_info(st.session_state.name, st.session_state.email, st.session_state.gc, "DHMS 2024-25", "2/23/2024 - Volunteers")

def login_clicked():
    login_creds = pd.read_csv("users.csv")
    if st.session_state.username in list(login_creds["username"]) and st.session_state.password in list(login_creds["password"]):
        st.session_state.valid_admin = "correct"
        st.session_state.sidebar = "collapsed"
    else:
        st.session_state.valid_admin = "incorrect"

    st.session_state.i = st.session_state.i + 1

    st.session_state.username_key = f"user_{st.session_state.i}"
    st.session_state.password_key = f"pass_{st.session_state.i}"

def admin_clicked():
    if st.session_state.sidebar != "expanded":
        st.session_state.sidebar = "expanded"

def volunteer_clicked():
    st.session_state.valid_admin = None

def close_side():
    st.session_state.sidebar = "collapsed"

def color_checked_in(name):
    if name == 'n/a':
        color = '#f0f0f5'
    else:
        checked_in = st.session_state.check_in_dict[name]
        color = '#90ee90' if checked_in else '#FF7F7F'

    return f'background-color: {color}'

def date_selected():
    st.session_state.refresh=False

def reassign_name_clicked():
    st.session_state.refresh=False

def reassign_teahcer_clicked():
    st.session_state.refresh=False

def app() -> None:

    if "check_in" not in st.session_state:
        st.session_state.check_in = False
    if "initial_setup" not in st.session_state:
        st.session_state.initial_setup = True
    if "valid_admin" not in st.session_state:
        st.session_state.valid_admin = None
    if "username_key" not in st.session_state:
        st.session_state.username_key = "user_2"
    if "password_key" not in st.session_state:
        st.session_state.password_key = "pass_2"
    if "i" not in st.session_state:
        st.session_state.i = 2
    if "sidebar" not in st.session_state:
        st.session_state.sidebar = "collapsed"
    if "refresh" not in st.session_state:
        st.session_state.refresh = False
    if "reassign_name" not in st.session_state:
        st.session_state.reassign_name = None
    if "reassign_teacher" not in st.session_state:
        st.session_state.reassign_teacher = None
    
    
    # Page configuration
    st.set_page_config(
        page_title="DHMS Check-In",
        page_icon=":large_green_circle:",
        layout='wide',
        initial_sidebar_state=st.session_state.sidebar
    )

    st.markdown(
        """

        <style>

        svg[data-baseweb=icon] {
                display: none;
            }

        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK {
                display: none;
            }

        .st-emotion-cache-1i6nhz1 {
                display: none;
            }

        div[data-testid="InputInstructions"] > span:nth-child(1) {
                visibility: hidden;
            }

        div[data-testid=stSidebarCollapseButton] { 
                display: none;    
            }

        .st-emotion-cache-1cyulp7 {
                display: none;
            }

        button[kind=primary] {
                float: right;
                background-color: #e0e0ef;
                border: none;
                color: black
            }
                
        button[kind=primary]:hover {
                background-color: #e0e0ef;
                border: none;
                color: #0000EE
            }

        </style>

    """,
        unsafe_allow_html=True,
    )

    if "gc" not in st.session_state:
        credentials_dict = toml.load(".streamlit/secrets.toml")
        credentials_dict = dict((k.lower(), v) for k,v in credentials_dict.items())
        st.session_state.gc = gspread.service_account_from_dict(credentials_dict)

    if st.session_state.initial_setup:
        sh = st.session_state.gc.open("DHMS 2024-25")
        worksheet = sh.worksheet("2/23/2024 - Volunteers")
        df = pd.DataFrame(worksheet.get_all_records())

        st.session_state.names = ps.sqldf("""SELECT name FROM df""", locals())
        st.session_state.emails = ps.sqldf("""SELECT email FROM df""", locals())
        st.session_state.teachers = ps.sqldf("""SELECT DISTINCT teacher FROM df""", locals())

        st.session_state.df = get_check_in_status(st.session_state.gc, "2/23/2024 - Volunteers")
        st.session_state.check_in_dict = get_check_in_dict(st.session_state.gc, "2/23/2024 - Volunteers")

    with st.sidebar:
        st.button(
            r"$\LARGE{\textsf{x}}$",
            on_click=close_side,
            type="primary",
        )

        st.markdown(
                "<h1 style='text-align: center; color: black;'>Admin Login</h1>",
                unsafe_allow_html=True,
            )

        if st.session_state.valid_admin == "incorrect":

            st.warning("Incorrect username or password, please try again.")

            st.session_state.username = st.text_input("Username:")
            st.session_state.password = st.text_input("Password:")

            st.button("Login", on_click=login_clicked, use_container_width=True, key=1)

        else:

            st.session_state.username = st.text_input("Username:", key=st.session_state.username_key)
            st.session_state.password = st.text_input("Password:", key=st.session_state.password_key)

            st.button("Login", on_click=login_clicked, use_container_width=True, key=1)


    if st.session_state.valid_admin == "correct":

        st.markdown(
            "<h1 style='text-align: center; color: black;'>Druid Hills Middle School Admin View</h1>",
            unsafe_allow_html=True,
        )

        # Sub title
        st.markdown(
            "<p style='text-align: center; color: black; opacity: .6;'>Enter the following information to check-in and receive your volunteer assignments</p>",
            unsafe_allow_html=True,
        )

        _, _, col1, _ = st.columns([1,1.2,.3,1])

        with col1:
            st.button("Volunteer Check-In", on_click=volunteer_clicked, use_container_width=True)

        _, col3, _ = st.columns([1,1.5,1])

        with col3:

            if st.session_state.refresh:
                st.session_state.df = get_check_in_status(st.session_state.gc, "2/23/2024 - Volunteers")
                st.session_state.check_in_dict = get_check_in_dict(st.session_state.gc, "2/23/2024 - Volunteers")

                st.session_state.refresh = False

            tab1, tab2 = st.tabs(["Event Dashboard", "Create New Event"])

            with tab1:
            
                with st.container(height=((len(st.session_state.df) + 1) * 35 + 3) + 475):

                    st.markdown(
                        "<h5 style='color: black;'>Select the date of the event:</h5>",
                        unsafe_allow_html=True,
                    )

                    st.session_state.date_of_event = st.date_input("What is the date of the event?", None, label_visibility="collapsed")

                    col5, col2 = st.columns([1,.2])
                    with col5:
                        st.markdown(
                        "<h5 style='color: black;'>Check-in Status:</h5>",
                        unsafe_allow_html=True,
                    )
                    with col2:
                        st.button("Refresh", on_click=refresh_clicked, use_container_width=True)

                    st.dataframe(st.session_state.df.style.map(color_checked_in, subset=['vol_1', 'vol_2', 'vol_3']), height = (len(st.session_state.df) + 1) * 35 + 3,use_container_width=True)

                    st.markdown(
                        "<h5 style='color: black;'>Re-assign Volunteer:</h5>",
                        unsafe_allow_html=True,
                    )

                    st.session_state.reassign_name = st_free_text_select(label="Name:", options=list(st.session_state.names["name"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible")

                    st.session_state.reassign_teacher = st_free_text_select(label="New Teacher Assignment:", options=list(st.session_state.teachers["teacher"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible")

                    st.button("Confirm Re-assign", use_container_width=True, disabled=((st.session_state.reassign_name == None) or (st.session_state.reassign_teacher == None)))

            with tab2:
                with st.container(height=670):
                    st.markdown(
                        "<h5 style='color: black;'>Create New Event:</h5>",
                        unsafe_allow_html=True,
                    )
                    st.session_state.date_of_new_event = st.date_input("What is the date of the new event?", None)

                    st.session_state.volunteer_assignments = st.file_uploader("Upload your volunteer assignments below", type=['xlsx', 'csv'], help="Upload a csv or xlsx file with the names, emails, and teacher assignment for each volunteer.")

                    st.button("Confirm New Event", use_container_width=True)

                    st.markdown(
                        "<h5 style='color: black;'>Add Volunteer to Event:</h5>",
                        unsafe_allow_html=True,
                    )

                    st.session_state.new_vol_name = st.text_input(label="Name:", label_visibility="visible")

                    st.session_state.new_vol_email = st.text_input(label="Email:", label_visibility="visible")

                    st.session_state.new_vol_teacher = st.text_input(label="Teacher Assignment:", label_visibility="visible")

                    st.button("Confirm New Volunteer", use_container_width=True)
    else:

        _, col4, _ = st.columns([1,1.2,1])

        with col4:

            if st.session_state.check_in:

                st.markdown(
                    "<h1 style='text-align: center; color: black;'>Druid Hills Middle School Volunteer Check-In</h1>",
                    unsafe_allow_html=True,
                )

                # Sub title
                st.markdown(
                    "<p style='text-align: center; color: black; opacity: .6;'>Enter the following information to check-in and receive your volunteer assignments</p>",
                    unsafe_allow_html=True,
                )

                _, col1 = st.columns([1,.28])

                with col1:
                    st.button("Admin Login", on_click=admin_clicked, use_container_width=True)

                with st.container(height=370):

                    st.success("Welcome, you are checked in! See information below and take a screenshot to refer back to.")

                    st.markdown("**Name:**")

                    st.write(st.session_state.series_info["name"].iloc[0])

                    st.markdown("**Teacher:**")

                    st.write(st.session_state.series_info["teacher"].iloc[0])

                    st.markdown("**Room Number:**")

                    st.write(str(st.session_state.series_info["room_number"].iloc[0]))

            else:

                st.markdown(
                    "<h1 style='text-align: center; color: black;'>Druid Hills Middle School Volunteer Check-In</h1>",
                    unsafe_allow_html=True,
                )

                # Sub title
                st.markdown(
                    "<p style='text-align: center; color: black; opacity: .6;'>Enter the following information to check-in and receive your volunteer assignments</p>",
                    unsafe_allow_html=True,
                )

                _, col1 = st.columns([1,.28])

                with col1:
                    st.button("Admin Login", on_click=admin_clicked, use_container_width=True)

                with st.container(height=380):
                    # Title

                    st.markdown(
                        "<h5 style='color: black;'>Your Information:</h5>",
                        unsafe_allow_html=True,
                    )

                    st.session_state.name = st_free_text_select(label="Name:", options=list(st.session_state.names["name"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible")

                    st.session_state.email = st_free_text_select(label="Email:", options=list(st.session_state.emails["email"]), index=None, format_func=lambda x: x.lower(), placeholder=' ', disabled=False, delay=300, label_visibility="visible")

                    st.session_state.phone_num = st.text_input(label="Phone Number:")

                    st.button("Check-In", on_click=check_in_clicked, use_container_width=True)

    st.session_state.initial_setup = False

if __name__ == "__main__":
    app()
