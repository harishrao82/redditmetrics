import streamlit as st
import pandas as pd
import numpy as np
import praw
import time
from datetime import datetime
import re

st.title('subreddit stats for /r/onlineaffairs')
left_column, right_column = st.columns(2)
DATA_URL="https://docs.google.com/spreadsheets/d/e/2PACX-1vQrPXtUthoVkidTDvxI4LLeiHvdQaUXciXC_U3MUjwCobukceCTP5vjEgIUWelRKECJm_xnhV_DYnU0/pub?gid=560482593&single=true&output=csv"
@st.cache
def load_data(subreddit):
    reddit = praw.Reddit(client_id='Ppp0O5Dfj9KUEA', client_secret='QBDYcuo9DjOcOLBCppgfbeyuE_g', user_agent='Reddit WebScrap',check_for_async=False)
    new_posts = reddit.subreddit(subreddit).new(limit=None)
    dfsub=pd.DataFrame(columns=['time','upvote','downvote','title','body','sex'])
    i=0
    for post in new_posts:
        #print(post.selftext)
        #print(post.title)
        row=[]
        ts = int(post.created_utc)
        time=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        row.append(time)
        row.append(post.ups)
        row.append(post.downs)
        row.append(post.title)
        row.append(post.selftext)
        m = re.match("(^(\d\d).*([MF]4[MF]))", post.title,flags=re.IGNORECASE)
        if m:
            Age=int(m.groups()[1])
            Sex=m.groups()[2]
            # #print(Sex)
            # if Sex == "[M4F]":
            #   print(post.title)
            # else:
            #   print(post.title)
            row.append(Sex.upper())
        else:
            row.append('NA')
        #print(row)
        dfsub.loc[i]=row
        i+=1
    dfsub['time'] = pd.to_datetime(dfsub['time'])
    dfsub['time_est']=dfsub.time + pd.DateOffset(hours=-4)
    dfsub['date'] = pd.to_datetime(dfsub['time_est'], errors='coerce')
    return dfsub

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
