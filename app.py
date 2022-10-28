import streamlit as st
import pandas as pd
import numpy as np

st.title('subreddit stats for /r/onlineaffairs')
left_column, right_column = st.columns(2)
DATA_URL="https://docs.google.com/spreadsheets/d/e/2PACX-1vQrPXtUthoVkidTDvxI4LLeiHvdQaUXciXC_U3MUjwCobukceCTP5vjEgIUWelRKECJm_xnhV_DYnU0/pub?gid=560482593&single=true&output=csv"
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data['date'] = pd.to_datetime(data['time_est'], errors='coerce')
    return data

with right_column:
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Data Loaded!")


with left_column:
    option = st.selectbox(
        'Pick type of post?',
        ('M4F', 'F4M', 'ALL'))

    st.write('You selected:', option)


if option == 'ALL':
    filtered_data=data
else:
    filtered_data=data[data['sex'] == option]


# with left_column:
#     if st.checkbox('Show filtered data'):
#         st.subheader('filtered data')
#         st.write(filtered_data[['title','sex','time_est','upvote']])

with right_column:
    header_var=f"'Number of posts by hour for {option} post'"
    st.subheader(header_var)
    hist_values = np.histogram(filtered_data['date'].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)
