import streamlit as st
import random
import pandas as pd
import numpy as np
import pandas as pd                        
from pytrends.request import TrendReq

def app():
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=['War'])
    df = pytrend.interest_by_region()
    # Interest by Region
    st.dataframe(df)