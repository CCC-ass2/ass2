import streamlit as st
from pages.page0 import map_plot
from pages.page1 import display as p1display
from pages.page2 import display as p2display
from pages.page3 import display as p3display
from pages.page4 import display as p4display
from backup_main import change_toml

st.set_page_config(layout="wide")

with st.sidebar:
    add_radio = st.radio(
        "Analysis on livability of Melbourne",
        ("Home", "Stress", "Emoji & Tag Usage", "Sentiment Analysis", "About us")
    )

change_toml(True)
if add_radio == 'Home':
    # change_toml(True)
    st.plotly_chart(map_plot(), use_container_width=False)
    change_toml(False)
if add_radio == 'Stress':
    change_toml(False)
    p1display()
elif add_radio == 'Emoji & Tag Usage':
    change_toml(False)
    p2display()
elif add_radio == "Sentiment Analysis":
    change_toml(False)
    p3display()
elif add_radio == "About us":
    # change_toml(False)
    p4display()