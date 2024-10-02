import streamlit as st
from GSpreadFunctions import get_info, get_check_in_status, get_check_in_dict, check_name_email_pair, mark_checked_in, reassign_vol, add_vol, create_new_event, initial_assignments
import gspread
import pandas as pd
import pandasql as ps
import datetime
from streamlit_free_text_select import st_free_text_select
from itertools import chain
import toml
import time
import re


def refresh_clicked():
    st.session_state.initial_setup = True

def check_in_clicked():
    st.session_state.check_in = True
    st.session_state.incorrect = check_name_email_pair(st.session_state.df_vol, st.session_state.name, st.session_state.email)
    if not st.session_state.incorrect:
        mark_checked_in(st.session_state.vol_ws, st.session_state.name, st.session_state.email)

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

    st.session_state.initial_setup = True

def admin_clicked():
    if st.session_state.sidebar != "expanded":
        st.session_state.sidebar = "expanded"

def volunteer_clicked():
    st.session_state.valid_admin = None

def close_side():
    st.session_state.sidebar = "collapsed"

def color_checked_in(name):
    if name == ' ':
        color = '#f0f0f5'
    else:
        checked_in = st.session_state.check_in_dict[name]
        color = '#90ee90' if checked_in else '#FF7F7F'

    return f'background-color: {color}'

def date_selected():
    st.session_state.refresh=False
    st.session_state.current_event = st.session_state.temp_current_event
    st.session_state.initial_setup = True

def reassign_name_clicked():
    st.session_state.refresh=False

def reassign_teahcer_clicked():
    st.session_state.refresh=False

def reassign_clicked():
    st.session_state.j += 1
    st.session_state.assign_vol_key = f"assign_{st.session_state.j}"
    st.session_state.assign_teach_key = f"assign_teach_{st.session_state.j}"
    st.session_state.initial_setup = True
    reassign_vol(st.session_state.vol_ws, st.session_state.teacher_ws, st.session_state.reassign_name, st.session_state.reassign_teacher)

def add_vol_clicked():
    st.session_state.j += 1
    st.session_state.add_vol_key = f"add_{st.session_state.j}"
    st.session_state.add_vol_email_key = f"add_email_{st.session_state.j}"
    st.session_state.initial_setup = True
    add_vol(st.session_state.vol_ws, st.session_state.new_vol, st.session_state.new_email)

def new_event_clicked():
    st.session_state.j += 1
    st.session_state.vol_list_upload = f"vol_{st.session_state.j}"
    st.session_state.new_event_date = f"date_{st.session_state.j}"
    st.session_state.grade_list = f"grade_{st.session_state.j}"
    try:
        new_event = create_new_event(st.session_state.date_of_new_event, st.session_state.sh)
    except:
        st.session_state.create_table_error = True
    
    if not st.session_state.create_table_error:
        initial_assignments(new_event, st.session_state.teacher_ws, st.session_state.teacher_grades, st.session_state.volunteer_list)
        st.session_state.event_created = True

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
    if "incorrect" not in st.session_state:
        st.session_state.incorrect = False
    if "create_table_error" not in st.session_state:
        st.session_state.create_table_error = False
    if "event_created" not in st.session_state:
        st.session_state.event_created = False
    if "j" not in st.session_state:
        st.session_state.j = 1
    if "vol_list_upload" not in st.session_state:
        st.session_state.vol_list_upload = f"vol_{st.session_state.j}"
    if "new_event_date" not in st.session_state:
        st.session_state.new_event_date = f"date_{st.session_state.j}"
    if "grade_list" not in st.session_state:
        st.session_state.grade_list = f"grade_{st.session_state.j}"
    if "add_vol_key" not in st.session_state:
        st.session_state.add_vol_key = f"add_{st.session_state.j}"
    if "assign_vol_key" not in st.session_state:
        st.session_state.assign_vol_key = f"assign_{st.session_state.j}"
    if "assign_teach_key" not in st.session_state:
        st.session_state.assign_teach_key = f"assign_teach_{st.session_state.j}"
    if "add_vol_email_key" not in st.session_state:
        st.session_state.add_vol_email_key = f"add_email_{st.session_state.j}"
    if "current_event" not in st.session_state:
        st.session_state.current_event = "2024-09-20"
    
    
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

        .st-emotion-cache-zooupb {
                display: none;
            }

        .st-emotion-cache-20q1e1 {
                display: none;
            }

        .st-emotion-cache-1wbqy5l {
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

    if st.session_state.initial_setup:
        current_year_db = "DHMS 2024-25"
        current_event_sheet_vol = str(st.session_state.current_event) + " - Volunteers"
        current_event_sheet_feed = str(st.session_state.current_event) + " - Feedback"

        credentials_dict = toml.load(".streamlit/secrets.toml")
        credentials_dict = dict((k.lower(), v) for k,v in credentials_dict.items())
        gc = gspread.service_account_from_dict(credentials_dict)
        time.sleep(1)
        st.session_state.sh = gc.open(current_year_db)
        time.sleep(1)
        st.session_state.teacher_ws = st.session_state.sh.worksheet("Teachers")
        st.session_state.vol_ws = st.session_state.sh.worksheet(current_event_sheet_vol)

        st.session_state.df_vol = pd.DataFrame(st.session_state.vol_ws.get_all_records())
        st.session_state.df_teach = pd.DataFrame(st.session_state.teacher_ws.get_all_records())

        df_vol = st.session_state.df_vol
        df_teach = st.session_state.df_teach

        st.session_state.names = ps.sqldf("""SELECT name FROM df_vol""", locals())
        st.session_state.emails = ps.sqldf("""SELECT email FROM df_vol""", locals())
        st.session_state.teachers = ps.sqldf(f"""SELECT DISTINCT teacher FROM df_vol""", locals())

        st.session_state.df = get_check_in_status(st.session_state.df_vol, st.session_state.df_teach)
        st.session_state.check_in_dict = get_check_in_dict(st.session_state.df_vol)

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
            st.session_state.password = st.text_input("Password:", type='password')

            st.button("Login", on_click=login_clicked, use_container_width=True, key=1)

        else:

            st.session_state.username = st.text_input("Username:", key=st.session_state.username_key)
            st.session_state.password = st.text_input("Password:", key=st.session_state.password_key, type='password')

            st.button("Login", on_click=login_clicked, use_container_width=True, key=1)


    if st.session_state.valid_admin == "correct":

        st.markdown(
            "<h1 style='text-align: center; color: black;'>Druid Hills Middle School Admin View</h1>",
            unsafe_allow_html=True,
        )

        # Sub title
        st.markdown(f"<p style='text-align: center; color: black; opacity: .6;'>The current event state is set for the date {st.session_state.current_event}</p>",
            unsafe_allow_html=True,
        )

        _, col30, _, col1, _ = st.columns([1,.3,.9,.3,1])

        with col30:
            with st.popover("Change Event"):
                st.session_state.temp_current_event = st.date_input("Select the date of the event")
                st.button("Confirm", on_click=date_selected, use_container_width=True)

        with col1:
            st.button("Volunteer Check-In", on_click=volunteer_clicked, use_container_width=True)

        _, col3, _ = st.columns([1,1.5,1])

        with col3:

            # if st.session_state.refresh:
            #     st.session_state.df = get_check_in_status(st.session_state.df_vol, st.session_state.df_teach)
            #     st.session_state.check_in_dict = get_check_in_dict(st.session_state.df_vol)

            #     st.session_state.refresh = False

            tab1, tab2 = st.tabs(["Event Dashboard", "Create New Event"])

            with tab1:
            
                # with st.container(height=((len(st.session_state.df) + 1) * 35 + 3) + 375):

                with st.container(border=True):

                    # st.markdown(
                    #     "<h5 style='color: black;'>Select the date of the event:</h5>",
                    #     unsafe_allow_html=True,
                    # )

                    # st.session_state.date_of_event = st.date_input("What is the date of the event?", None, label_visibility="collapsed")

                    col5, col2 = st.columns([1,.2])
                    with col5:
                        st.markdown(
                        "<h5 style='color: black;'>Check-in Status:</h5>",
                        unsafe_allow_html=True,
                    )
                    with col2:
                        st.button("Refresh", on_click=refresh_clicked, use_container_width=True)

                    max_num_vols = max(st.session_state.df["vols_assigned"])
                    vol_subset = []
                    for i in range(1, max_num_vols + 1):
                        vol_subset.append(f"vol_{i}")

                    st.dataframe(st.session_state.df.style.map(color_checked_in, subset=vol_subset), height = (len(st.session_state.df) + 1) * 35 + 3,use_container_width=True)

                    col20, col21 = st.columns([1,1])

                    with col21:

                        st.markdown(
                            "<h5 style='color: black;'>Re-Assign Volunteer:</h5>",
                            unsafe_allow_html=True,
                        )

                        st.session_state.reassign_name = st_free_text_select(label="Name:", options=list(st.session_state.names["name"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible", key=st.session_state.assign_vol_key)

                        # if st.session_state.reassign_name != None:
                        #     # Get historical data
                        #     st.write("Historical data will appear here")

                        st.session_state.reassign_teacher = st_free_text_select(label="New Teacher Assignment:", options=list(st.session_state.teachers["teacher"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible", key=st.session_state.assign_teach_key)

                        st.button("Assign Volunteer", on_click=reassign_clicked, use_container_width=True, disabled=((st.session_state.reassign_name == None) or (st.session_state.reassign_teacher == None)))

                    with col20:

                        st.markdown(
                            "<h5 style='color: black;'>Add Volunteer:</h5>",
                            unsafe_allow_html=True,
                        )

                        st.session_state.new_vol = st_free_text_select(label="Name:", options=[], index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="visible", key=st.session_state.add_vol_key)

                        st.session_state.new_email = st_free_text_select(label="Email:", options=[], index=None, format_func=lambda x: x.lower(), placeholder=' ', disabled=False, delay=300, label_visibility="visible", key=st.session_state.add_vol_email_key)

                        st.button("Add Volunteer", on_click=add_vol_clicked, use_container_width=True, disabled=((st.session_state.new_vol == None) or (st.session_state.new_email == None)))

                        # # if st.session_state.reassign_name != None:
                        # #     # Get historical data
                        # #     st.write("Historical data will appear here")

            with tab2:
                if st.session_state.create_table_error:
                    st.error("An event already exists for this date. Please select a different date.")
                    st.session_state.create_table_error = False

                if st.session_state.event_created:
                    st.success(f"Event for {st.session_state.date_of_new_event} was successfully created!")
                    st.session_state.event_created = False

                with st.container(border=True):
                    st.markdown(
                        "<h5 style='color: black;'>Create New Event:</h5>",
                        unsafe_allow_html=True,
                    )

                    st.session_state.volunteer_list = st.file_uploader("Upload your volunteer list below", type=['xlsx', 'csv'], help="Upload a csv or xlsx file with the names (one column) and emails for each volunteer. Make sure to include a header row.", key=st.session_state.vol_list_upload)

                    col6, col7 = st.columns([1,1])
                    with col6:
                        st.session_state.date_of_new_event = st.date_input("What is the date of the new event?", None, key=st.session_state.new_event_date)
                    with col7:
                        st.session_state.teacher_grades = st.multiselect("Which grades are apart of the event?", ["6", "7", "8"], key=st.session_state.grade_list)

                    st.button("Confirm New Event", on_click=new_event_clicked, use_container_width=True, disabled=(st.session_state.date_of_new_event == None) or (st.session_state.volunteer_list == None))

    else:

        _, col4, _ = st.columns([1,1.2,1])

        with col4:

            if st.session_state.check_in and not st.session_state.incorrect:

                st.session_state.series_info = get_info(st.session_state.df_vol, st.session_state.name, st.session_state.email)
            
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

                if st.session_state.incorrect:
                    st.error("Your email and name do not match with our records. Please re-enter your information.")

                st.markdown("**Name:**")

                st.session_state.name = st_free_text_select(label="Name:", options=list(st.session_state.names["name"]), index=None, format_func=lambda x: x.title(), placeholder=' ', disabled=False, delay=300, label_visibility="collapsed")
                
                st.markdown("**Email:**")

                st.session_state.email = st_free_text_select(label="Email:", options=list(st.session_state.emails["email"]), index=None, format_func=lambda x: x.lower(), placeholder=' ', disabled=False, delay=300, label_visibility="collapsed")

                # Uncomment once the phone update thing is ready
                # st.markdown("**Phone Number:**")

                # st.session_state.phone_num = st.text_input(label="Phone Number:", label_visibility="collapsed")

                st.button("Check-In", on_click=check_in_clicked, use_container_width=True)

    st.session_state.initial_setup = False

if __name__ == "__main__":
    app()
