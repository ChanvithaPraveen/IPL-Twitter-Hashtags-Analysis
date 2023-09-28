# import numpy as np
# import pandas as pd
# import streamlit as st
# import streamlit.components.v1 as components
# import datetime
#
# st.set_page_config(page_title="The Ramsey Highlights", layout="wide")
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
#         width: 400px;
#     }
#     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
#         width: 400px;
#         margin-left: -400px;
#     }
#
#     """,
#     unsafe_allow_html=True,
# )
#
# st.markdown(f'''
#     <style>
#     section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
#     </style>
# ''',unsafe_allow_html=True)
#
# # st.title("IPL Twitter Data Analyzing Dashboard")
# #
# # today = datetime.date.today()
# # tomorrow = today + datetime.timedelta(days=1)
# # start_date = st.date_input('Start date', today)
# # end_date = st.date_input('End date', tomorrow)
# # if start_date < end_date:
# #     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# # else:
# #     st.error('Error: End date must fall after start date.')
#
#
# st.title("IPL Twitter Data Analyzing Dashboard")
#
# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)
#
# # Create two columns
# col1, col2 = st.columns(2)
#
# # Add Start Date selector to the first column
# with col1:
#     start_date = st.date_input('Start date', today)
#
# # Add End Date selector to the second column
# with col2:
#     end_date = st.date_input('End date', tomorrow)
#
# # Check if the selected dates are valid
# if start_date < end_date:
#     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
#     print(f"Start date: {start_date}")
#     print(f"End date: {end_date}")
# else:
#     st.error('Error: End date must fall after start date.')
#
# # Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to Analyze?",
#     ("Past Data", "Forecast Data")
# )
#
# # Using "with" notation
# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )
#
#
#
# HtmlFile = open("../bubble_map.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# components.html(source_code, height=800)
#
# print(end_date)
#
#
#
#
#
#





import streamlit as st
import datetime
import requests


st.set_page_config(page_title="The Ramsey Highlights", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }

    """,
    unsafe_allow_html=True,
)

st.markdown(f'''
    <style>
    section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
    </style>
''',unsafe_allow_html=True)


st.title("IPL Twitter Data Analyzing Dashboard")

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

# Create two columns
col1, col2 = st.columns(2)

# Add Start Date selector to the first column
with col1:
    start_date = st.date_input('Start date', today)

# Add End Date selector to the second column
with col2:
    end_date = st.date_input('End date', tomorrow)

# Check if the selected dates are valid
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

# Button to trigger the backend processing
if st.button("Generate Bubble Map"):
    # Convert selected dates to strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Send a request to the FastAPI backend to generate the bubble map
    response = requests.get(f"http://localhost:8000/generate_bubble_map/?start_date={start_date_str}&end_date={end_date_str}")

    if response.status_code == 200:
        st.success("Bubble map generated successfully.")
    else:
        st.error("Error generating the bubble map.")


# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to Analyze?",
    ("Past Data", "Forecast Data")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )