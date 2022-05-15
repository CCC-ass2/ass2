import streamlit as st

def display():
    st.title('About the project')
    st.write('''The focus of this assignment is to harvest tweets from Melbourne on the MRC and undertake a variety of social media data analytics scenarios that explore liveability of Melbourne and
    importantly how the Twitter data can be used alongside/compared with/augment the data available
    within the AURIN platform to improve our knowledge of the liveability of Melbourne. Teams can
    download data from the AURIN platform, e.g. as JSON, CSV or Shapefiles, or using the AURIN openAPI''')

    st.title('About us')
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.image('pages/backup_page4/hjc.jpg')
    c2.image('pages/backup_page4/lhy.jpg')
    c3.image('pages/backup_page4/lyx.jpg')
    c4.image('pages/backup_page4/zdk.jpg')
    c5.image('pages/backup_page4/zzq.jpg')
