# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 00:42:24 2022

@author: Jordi Garcia Ruspira
"""


import streamlit as st
import pandas as pd
import requests
import json
import time
import plotly.graph_objects as go
import random
import plotly.io as pio
from streamlit_echarts import st_echarts
import plotly.io as pio 
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image 


st.set_page_config(
    page_title="Osmosis Validators - Sankey chart",
    page_icon=":atom_symbol:",
    layout="wide",
    menu_items=dict(About="It's a work of Jordi"),
)


st.title(":atom_symbol: OSMO Rewards :atom_symbol:") 
#st.image("https://s1.gifyu.com/images/image_processing20210907-12647-r8jmvu.gif")
st.success("This app only contains a chart showing the daily rewards from Osmosis epoch distribution.")
st.text("")
st.subheader('Streamlit App by [Jordi R.](https://twitter.com/RuspiTorpi/). Powered by Flipsidecrypto')
st.text("")
 

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    ) 
pio.renderers.default = 'browser'




API_KEY = st.secrets["API_KEY"]



  
SQL_QUERY = """  select distinct liquidity_provider_address as liquidity_provider_address from osmosis.core.fact_liquidity_provider_actions
where tx_status = 'SUCCEEDED'

"""  
  

TTL_MINUTES = 15
# return up to 100,000 results per GET request on the query id
PAGE_SIZE = 100000
# return results of page 1
PAGE_NUMBER = 1

def create_query(SQL_QUERY):
    r = requests.post(
        'https://node-api.flipsidecrypto.com/queries', 
        data=json.dumps({
            "sql": SQL_QUERY,
            "ttlMinutes": TTL_MINUTES
        }),
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY},
    )
    if r.status_code != 200:
        raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))
    
    return json.loads(r.text)    
  
def get_query_results(token):
    r = requests.get(
        'https://node-api.flipsidecrypto.com/queries/{token}?pageNumber={page_number}&pageSize={page_size}'.format(
          token=token,
          page_number=PAGE_NUMBER,
          page_size=PAGE_SIZE
        ),
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY}
    )
    if r.status_code != 200:
        raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
    
    data = json.loads(r.text)
    if data['status'] == 'running':
        time.sleep(10)
        return get_query_results(token)

    return data

  

 
input_feature = st.text_input('Introduce wallet address: ','osmo1s3uhtyzcu2ft4w2dhjtew3gt3lpmc2az2rw5ll')
    
get_rewards_historical = requests.get("https://api-osmosis-chain.imperator.co/lp/v1/rewards/historical/"+input_feature+"/OSMO").json()

df_historical_rewards = pd.DataFrame(get_rewards_historical)
df_historical_rewards = df_historical_rewards.sort_values(by="day") 

 
fig = px.area(df_historical_rewards, x="day", y="amount")#, color="continent", line_group="country")
 
st.plotly_chart(fig, use_container_width=True) 
