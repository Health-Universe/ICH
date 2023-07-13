import streamlit as st
import joblib
import base64
from streamlit_option_menu import option_menu
import datetime
import pandas as pd
import time

if 'model' not in st.session_state:
    model = joblib.load('model.pkl')
    st.session_state["model"] = model
else:
    model = st.session_state["model"]

st.set_page_config(page_title='xxx', layout="wide", page_icon=':ambulance:')


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background():
    page_bg_img = '''
    <style>
    .css-1nnpbs {width: 100vw}
    h1 {padding: 0.75rem 0px 0.75rem;margin-top: 2rem;box-shadow: 0px 3px 5px gray;}
    h2 {background-color: #8080801f;margin-top: 2vh;border-left: red solid 0.6vh}
    .css-1avcm0n {background: rgb(14, 17, 23, 0)}
    .css-18ni7ap {background: rgb(0, 120, 190);z-index:1;height:3rem}
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    .css-z5fcl4 {padding: 0 1rem 1rem}
    .css-12ttj6m {box-shadow: 0.05rem 0.05rem 0.2rem 0.1rem rgb(192, 192, 192);margin:0 calc(20% + 0.5rem);}
    .css-1cbqeqj {text-align: center;}
    .css-1x8cf1d {background: #00800082}
    .css-1x8cf1d:hover {background: #00800033}
    img {margin: -13vh 0vh 0vh 16vh;z-index:2;max-width:}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background()
st.markdown("<h1 style='text-align: center'>xxx system</h1>", unsafe_allow_html=True)
select_dic = {
    'No': 0,
    'Yes': 1
}
col1, col2, col3 = st.columns([2, 6, 2])
with col1:
    st.image('logo.png')
with col2:
    st.markdown("<h2 style='text-align: center'>xxx system</h2>", unsafe_allow_html=True)
with st.form("my_form"):
    col9, col10, col11, col12 = st.columns([2.5, 2.5, 2.5, 2.5])
    col7, col8 = st.columns([5, 5])
    with col9:
        in_time = st.date_input(
            "intime",
            datetime.datetime.now())
    with col10:
        in_time_ = st.time_input("", datetime.time(8, 0), step=60)
    with col7:
        potassium_mean = st.text_input("potassium_mean")
        gcs_min = st.text_input("gcs_min")
        sofa = st.text_input("sofa")
        calcium_mean = st.text_input("calcium_mean")
        spo2_mean = st.text_input("spo2_mean")
        rdw_mean = st.text_input("rdw_mean")
        sodium_mean = st.text_input("sodium_mean")
    with col11:
        out_time = st.date_input(
            "outime",
            datetime.datetime.now())
    with col12:
        out_time_ = st.time_input("", datetime.time(8, 0), key='444', step=60)
    with col8:
        anticoagulants = st.selectbox('anticoagulants', ('No', 'Yes'))
        mannitol = st.selectbox('mannitol', ('No', 'Yes'))
        vaso_drug = st.selectbox('vaso_drug', ('No', 'Yes'))
        ventilation = st.selectbox('ventilation', ('No', 'Yes'))
        temperature_mean = st.text_input("temperature_mean")
        surgical_intervention = st.selectbox('surgical_intervention', ('No', 'Yes'))
        heart_failure = st.selectbox('heart_failure', ('No', 'Yes'))

    submitted = st.form_submit_button("Calculate")
    if submitted:
        flag = datetime.datetime.combine(out_time, out_time_) - datetime.datetime.combine(in_time, in_time_)
        test_df = pd.DataFrame(
            [select_dic[anticoagulants], select_dic[mannitol], select_dic[vaso_drug], select_dic[ventilation],
             float(temperature_mean), select_dic[surgical_intervention], select_dic[heart_failure],
             float(potassium_mean), int(gcs_min), int(sofa), float(calcium_mean), float(spo2_mean),
             float(rdw_mean), float(sodium_mean), pd.Series(flag).dt.total_seconds()[0] / 86400]).T
        st.subheader("Probability of disease occurrence: {:.3f}%".format(model.predict_proba(test_df)[0][1] * 100))
col4, col5, col6 = st.columns([2, 6, 2])
with col5:
    selected_footer = option_menu(
        menu_title=None,
        options=["Project Instruction", "Model Description", "Model Description Figures", "Project Flow Chart"],
        icons=["projector-fill", "info-circle-fill", "bar-chart-steps", "diagram-3-fill"],
        default_index=0,
        orientation="horizontal",
    )
    if selected_footer == "Project Instruction":
        st.write('xxx')
    elif selected_footer == "Model Description":
        st.write('123')
    elif selected_footer == "Model Description Figures":
        sign = True
        bar = st.empty()
        em = st.empty()
        img = st.empty()
        while sign:
            my_bar = bar.progress(0)
            em.markdown('<div style="height: 16vh;width:20vw"></div>', unsafe_allow_html=True)
            for i in range(1, 3):
                my_bar.progress(i * 1 / 2)
                img.image('{}.png'.format(i))
                time.sleep(3)
    elif selected_footer == "Project Flow Chart":
        st.write('123')
