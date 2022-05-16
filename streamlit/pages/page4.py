import streamlit as st

def display():
    st.title('About the project')
    st.write(''' Complex analysis scenarios usually rely on distributed cloud-based solutions and require high volumes 
    of data. In this project we are about to develop a dynamically cloud-based solution utilizing the Melbourne 
    Research Cloud (MRC) to explore the livability of Melbourne. The livability can be explored from many aspects, 
    i.e. stress level of people, unemployment rate, housing prices, people’s mental and body health situation and access 
    to infrastructural services etc, the comparision can also be made from across the greater city level or across the 
    LGA level within the greater city. 
''')

    st.title('About us')
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.image('pages/backup_page4/huo.png')
    c2.image('pages/backup_page4/lhy.png')
    c3.image('pages/backup_page4/lyx.png')
    c4.image('pages/backup_page4/zdk.png')
    c5.image('pages/backup_page4/zhu.png')
