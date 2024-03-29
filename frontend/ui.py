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
import base64
import streamlit as st
import datetime
import requests
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="IPL Tweets Analysis", layout="wide")
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
''', unsafe_allow_html=True)

# Apply custom CSS to remove padding and margins
st.markdown(
    """
    <style>
    .stSidebar img {
        padding: 0px;
        margin: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


df = pd.read_csv('../unique_dates_cities_df.csv')
df2 = pd.read_csv('../df1_cleaned_final.csv')

# Assuming you have a DataFrame named df with a 'city' column
unique_cities = df['city'].unique().tolist()

st.sidebar.image('assets/ipl_analyzer_logo.svg', width=400)

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to Analyze?",
    ("Past Macro-Data", "Past Micro-Data", "Forecast Data", "Real-Time Data")
)

# Create a radio button in the sidebar to select the theme
# with st.sidebar:
    # theme_mode = st.radio("Choose a Theme Mode", ("Light Theme", "Dark Theme"))
    # if theme_mode == "Light Theme":
    #     [theme] = ["light"]



if add_selectbox == "Past Macro-Data":
    # Add a nice background color
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    [data-testid="stToolbar"] {
        right: 2rem;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Analyzing Past Macro-Data")

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

    st.subheader('Explore Users in World Map')
    # Button to trigger the backend processing
    if st.button("Generate Bubble Map"):
        # Convert selected dates to strings
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Send a request to the FastAPI backend to generate the bubble map
        response = requests.get(
            f"http://localhost:8000/generate_bubble_map/?start_date={start_date_str}&end_date={end_date_str}")

        if response.status_code == 200:
            st.success("Bubble map generated successfully!")
            HtmlFile = open("../bubble_map7.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=800)
        else:
            st.error("Error generating the bubble map.")

    st.subheader('Explore City-Wise Bar Chart')
    # Button to trigger the backend processing
    if st.button("Generate Bar Chart"):
        # Convert selected dates to strings
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Send a request to the FastAPI backend to generate the bubble map
        response = requests.get(
            f"http://localhost:8000/generate_city_chart/?start_date={start_date_str}&end_date={end_date_str}")

        if response.status_code == 200:
            st.success("City Chart generated successfully!")
            HtmlFile = open("../city_chart.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=800)

    st.subheader('Explore City-Wise Line Chart')
    # Button to trigger the backend processing
    if st.button("Generate Line Chart"):
        # Convert selected dates to strings
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Send a request to the FastAPI backend to generate the bubble map
        response = requests.get(
            f"http://localhost:8000/generate_line_chart/?start_date={start_date_str}&end_date={end_date_str}")

        if response.status_code == 200:
            st.success("Line Chart generated successfully!")
            HtmlFile = open("../line_chart1.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=800)

if add_selectbox == "Forecast Data":
    # Add a nice background color
    page_bg_img = '''
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0);
        }

        [data-testid="stToolbar"] {
            right: 2rem;
        }
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Display the Forecast Data screen/page
    st.title("Forecast Future-Data")

    today = datetime.date.today()

    # Create two columns
    column1, column2 = st.columns(2)

    # Add Start Date selector to the first column
    with column1:
        predict_date = st.date_input('Select Day like to Predict', today)

    # Add Start Date selector to the first column
    with column2:
        # Using object notation
        select_city = st.selectbox(
            "Select City like to Predict?",
            unique_cities
        )

    st.subheader(f'Explore Tweet Count in {select_city.title()} City on {predict_date}')
    # Button to trigger the backend processing
    if st.button("Predict"):
        # Convert selected dates to strings
        predict_date_str = predict_date.strftime("%Y-%m-%d")
        # end_date_str = end_date.strftime("%Y-%m-%d")
        select_city = str(select_city)

        # Create a JSON request body
        request_body = {
            "predict_date": predict_date_str,
            "select_city": select_city,
        }

        # Send a request to the FastAPI backend to generate the bubble map
        response = requests.post(
            f"http://localhost:8000/predict_future_tweet_count/?predict_date={predict_date_str}&select_city={select_city}",
            json=request_body,
        )
        # st.error("Error.")
        if response.status_code == 200:
            prediction_result = response.json()  # Get the prediction result as a string
            st.success("Prediction successful!")
            st.write(f"There will be {int(prediction_result)} users tweet on {predict_date} in {select_city.title()}")
        else:
            st.error(f"error {predict_date} & {select_city}")


if add_selectbox == "Past Micro-Data":
    # Add a nice background color
    page_bg_img = '''
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1620121692029-d088224ddc74?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0);
        }

        [data-testid="stToolbar"] {
            right: 2rem;
        }
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Analyzing Past Micro-Data")

    # Sidebar for column selection using checkboxes
    selected_columns = st.multiselect("Select Columns to Display", df2.columns.tolist())

    filtered_df = df2[selected_columns]

    # Search keyword input
    search_keyword = st.text_input("Search Keyword")

    # Filter DataFrame based on selected columns and search keyword
    if selected_columns:
        filtered_df = df2[
            df2[selected_columns].astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)]
    else:
        filtered_df = df2[df2.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)]

    # Single date selection
    selected_date = st.date_input("Select Date")

    # Filter DataFrame based on selected columns and single date
    if selected_columns:
        filtered_df = df2[
            (df2[selected_columns].astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(
                axis=1)) &
            (df2['day'] == selected_date.day) &
            (df2['month'] == selected_date.month) &
            (df2['year'] == selected_date.year)]
    else:
        filtered_df = df2[
            (df2.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)) &
            (df2['day'] == selected_date.day) &
            (df2['month'] == selected_date.month) &
            (df2['year'] == selected_date.year)]

    # Display the filtered DataFrame with dynamically selected columns
    st.subheader("Filtered DataFrame:")
    st.dataframe(filtered_df[selected_columns] if selected_columns else filtered_df)

    # Export to CSV button
    if st.button("Export to CSV"):
        # Create a CSV file
        csv_filename = "exported_data.csv"
        csv_file = filtered_df.to_csv(index=False).encode('utf-8')

        # Provide a download link for the CSV file
        b64 = base64.b64encode(csv_file).decode()
        st.download_button(
            label="Download CSV",
            data=csv_file,
            file_name="exported_data.csv",
            key="download_csv",
            help="Click to download the CSV file.",
        )







