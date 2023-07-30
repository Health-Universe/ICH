import streamlit as st
import joblib
import base64
from streamlit_option_menu import option_menu
import datetime
import pandas as pd
import time
import shap
import matplotlib.pyplot as plt

if 'model' not in st.session_state:
    model = joblib.load('model.pkl')
    st.session_state["model"] = model
else:
    model = st.session_state["model"]

st.set_page_config(page_title='Web Calculator For sICH', layout="wide", page_icon=':ambulance:')


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
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background()
st.markdown("<h1 style='text-align: center'>Computational tool for predicting in-hospital mortality in severe spontaneous intracerebral hemorrhage</h1>", unsafe_allow_html=True)
select_dic = {
    'No': 0,
    'Yes': 1
}
col1, col2, col3 = st.columns([2, 6, 2])
# with col1:
#     st.image('logo.png')
with col2:
    st.markdown("<h2 style='text-align: center'>Please answer the questions below to calculate:</h2>", unsafe_allow_html=True)
with st.form("my_form"):
    col7, col8 = st.columns([5, 5])
    spo2_mean = st.empty()
    with col7:
        vaso_drug = st.selectbox('Use of vasoactive drugs', ('No', 'Yes'))
        mannitol = st.selectbox('Use of mannitol', ('No', 'Yes'))
        anticoagulants = st.selectbox('Use of anticoagulant drugs', ('No', 'Yes'))
        ventilation = st.selectbox('Mechanical ventilation', ('No', 'Yes'))
        heart_failure = st.selectbox('Heart failure', ('No', 'Yes'))
        surgical_intervention = st.selectbox('Surgical intervention', ('No', 'Yes'))
        chloride_mean = st.text_input("Chloride")
    with col8:
        gcs_min = st.text_input("GCS")
        sofa = st.text_input("SOFA")
        temperature_mean = st.text_input("Temperature(℃)")
        rdw_mean = st.text_input("RDW(%)")
        sodium_mean = st.text_input("Sodium(mmol/L)")
        potassium_mean = st.text_input("Potassium(mmol/L)")
        spo2_mean = spo2_mean.text_input("Blood oxygen saturation(%)")
    col4, col5, col6 = st.columns([2, 2, 6])
    with col4:
        submitted = st.form_submit_button("Calculate")
    with col5:
        reset = st.form_submit_button("Reset")
    if submitted:
        test_df = pd.DataFrame(
            [select_dic[anticoagulants], select_dic[mannitol], select_dic[vaso_drug], select_dic[ventilation],
             float(temperature_mean), select_dic[surgical_intervention], float(potassium_mean), 
             int(sofa), float(spo2_mean), float(rdw_mean), select_dic[heart_failure], float(sodium_mean), 
             int(gcs_min), float(chloride_mean)]).T
        pre_res = model.predict_proba(test_df)[0][1] * 100
        if  pre_res> 29.3:
            flag = "Please early intervention and monitoring."
        elif pre_res < 29.3:
            flag = "Please continue the current effective treatment and closely monitor the patient's condition."
        st.subheader("The probability of being hospitalized and dying from the disease is {:.3f}%（the threshold for  disease mortality is 29.3%）".format(pre_res))
        st.subheader(flag)

        with st.spinner('force plot generation, please wait...'):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(test_df)
            shap.force_plot(explainer.expected_value, shap_values[0], test_df.iloc[0].values, feature_names=['Use of anticoagulant drugs', 'Use of mannitol', 'Use of vasoactive drugs', 
                                                          'Mechanical ventilation', 'Temperature', 'Surgical intervention', 'Potassium', 
                                                          'SOFA', 'Blood oxygen saturation', 'RDW', 'Heart failure', 'Sodium', 'GCS', 'Chloride'], matplotlib=True, show=False, figsize=(20, 5))
            plt.xticks(fontproperties='Times New Roman', size=16)
            plt.yticks(fontproperties='Times New Roman', size=16)
            plt.tight_layout()
            plt.savefig('force.png', dpi=600)
            st.image('force.png')
    elif reset:
        st.experimental_rerun()
        spo2_mean.empty()
