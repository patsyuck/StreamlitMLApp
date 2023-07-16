import streamlit as st
import pandas as pd
import numpy as np
import lightgbm
import pickle
import base64

app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Prediction']) #two pages
if app_mode == 'Home':
    st.title('LOAN PREDICTION')
    st.image('sources/loan.jpg')
    #st.markdown('Dataset:')
    #df = pd.read_csv('datasets/application_train.csv')
    #data = df[['TARGET', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 
    #    'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'DAYS_BIRTH']]
    #st.write(data.head())
    #st.markdown('Total Income VS Credit')
    #st.bar_chart(data[['AMT_INCOME_TOTAL', 'AMT_CREDIT']].head(20))
elif app_mode == 'Prediction':
    st.image('sources/money.jpg')
    st.subheader('You need to fill all necessary information in order to get a reply to your loan request!')
    st.sidebar.header("Information about the client:")
    dct_gender = {'F': 0, 'M': 1, 'NA': np.nan}
    dct_binary = {'N': 0, 'Y': 1}
    dct_money = {'0-50 k': 0, '50-100 k': 1, '100-150 k': 2, '150-200 k': 3, '200-250 k': 4, 
        '250-300 k': 5, '300-350 k': 6, '350-400 k': 7, '400-450 k': 8, '450-500 k': 9, '500+ k': 10}
    dct_annuity = {'0-10 k': 0, '10-20 k': 1, '20-30 k': 2, '30-40 k': 3, '40-50 k': 4, 
        '50-60 k': 5, '60-70 k': 6, '70-80 k': 7, '80-90 k': 8, '90-100 k': 9, '100+ k': 10}
    dct_price = {'0-200 k': 0, '200-400 k': 1, '400-600 k': 2, '600-800 k': 3, '800-1000 k': 4, 
        '1000-1200 k': 5, '1200-1400 k': 6, '1400-1600 k': 7, '1600-1800 k': 8, '1800-2000 k': 9, '2000+ k': 10}
    dct_job = {'Working': 1, 'Commercial': 2, 'State': 3, 'Pensioner': 4, 'Other': 5}
    dct_education = {'Lower secondary': 1, 'Secondary (special)': 2, 'Incomplete higher': 3, 'Complete higher': 4, 'Academic degree': 5}
    dct_family = {'Married': 1, 'Not married': 2, 'Civil': 3, 'Separated': 4, 'Widow': 5, 'Other': 6}
    dct_apartment = {'House': 1, 'Parents': 2, 'Municipal': 3, 'Rented': 4, 'Office': 5, 'Coop': 6}
    Age = st.sidebar.slider('Age', 18, 70, 35)
    Children = st.sidebar.slider('Children count', 0, 20, 0)
    Children = Children if Children < 6 else 6
    #Loan_Amount_Term = st.sidebar.selectbox('Loan_Amount_Term', (12.0,36.0,60.0,84.0,120.0,180.0,240.0,300.0,360.0))
    Gender = dct_gender[st.sidebar.radio('Gender', tuple(dct_gender.keys()))]
    Car = dct_binary[st.sidebar.radio('Has Car', tuple(dct_binary.keys()))]
    Realty = dct_binary[st.sidebar.radio('Has Realty', tuple(dct_binary.keys()))]
    Job = dct_job[st.sidebar.radio('Income Type', options=list(dct_job.keys()))]
    IsJobWorking = 1 if Job == 1 else 0
    IsJobCommercial = 1 if Job == 2 else 0
    IsJobState = 1 if Job == 3 else 0
    IsJobPensioner = 1 if Job == 4 else 0
    Education = dct_education[st.sidebar.radio('Education', options=list(dct_education.keys()))]
    IsEducLowerSec = 1 if Education == 1 else 0
    IsEducSecondary = 1 if Education == 2 else 0
    IsEducHigherInc = 1 if Education == 3 else 0
    IsEducHigher = 1 if Education == 4 else 0
    Family = dct_family[st.sidebar.radio('Family', options=list(dct_family.keys()))]
    IsFamMarried = 1 if Family == 1 else 0
    IsFamNotMarried = 1 if Family == 2 else 0
    IsFamCivil = 1 if Family == 3 else 0
    IsFamSeparated = 1 if Family == 4 else 0
    IsFamWidow = 1 if Family == 5 else 0
    Apartment = dct_apartment[st.sidebar.radio('Apartment', options=list(dct_apartment.keys()))]
    IsApartHouse = 1 if Apartment == 1 else 0
    IsApartParents = 1 if Apartment == 2 else 0
    IsApartMunicipal = 1 if Apartment == 3 else 0
    IsApartRented = 1 if Apartment == 4 else 0
    IsApartOffice = 1 if Apartment == 5 else 0
    Income = dct_money[st.sidebar.radio('Total Income', options=list(dct_money.keys()))]
    Credit = dct_money[st.sidebar.radio('Credit', options=list(dct_money.keys()))]
    Annuity = dct_annuity[st.sidebar.radio('Annuity', options=list(dct_annuity.keys()))]
    Price = dct_price[st.sidebar.radio('Goods Price', options=list(dct_price.keys()))]
    data_1 = {'age': Age, 'cntChildren': Children, 'gender': Gender, 'hasCar': Car, 'hasRealty': Realty, 
        'IsJobWorking': IsJobWorking, 'IsJobCommercial': IsJobCommercial, 'IsJobState': IsJobState, 'IsJobPensioner': IsJobPensioner, 
        'IsEducLowerSec': IsEducLowerSec, 'IsEducSecondary': IsEducSecondary, 'IsEducHigherInc': IsEducHigherInc, 'IsEducHigher': IsEducHigher, 
        'IsFamMarried': IsFamMarried, 'IsFamNotMarried': IsFamNotMarried, 'IsFamCivil': IsFamCivil, 'IsFamSeparated': IsFamSeparated, 'IsFamWidow': IsFamWidow, 
        'IsApartHouse': IsApartHouse, 'IsApartParents': IsApartParents, 'IsApartMunicipal': IsApartMunicipal, 'IsApartRented': IsApartRented, 
        'IsApartOffice': IsApartOffice, 'income': Income, 'credit': Credit, 'annuity': Annuity, 'goodsPrice': Price}
    feat_lst = [data_1['gender'], data_1['hasCar'], data_1['hasRealty'], data_1['cntChildren'], data_1['income'], data_1['credit'], data_1['annuity'], 
        data_1['goodsPrice'], data_1['IsJobWorking'], data_1['IsJobCommercial'], data_1['IsJobState'], data_1['IsJobPensioner'], 
        data_1['IsEducLowerSec'], data_1['IsEducSecondary'], data_1['IsEducHigherInc'], data_1['IsEducHigher'], 
        data_1['IsFamMarried'], data_1['IsFamNotMarried'], data_1['IsFamCivil'], data_1['IsFamSeparated'], data_1['IsFamWidow'], 
        data_1['IsApartHouse'], data_1['IsApartParents'], data_1['IsApartMunicipal'], data_1['IsApartRented'], data_1['IsApartOffice'], data_1['age']]
    single_sample = np.array(feat_lst).reshape(1,-1)
    if st.button("Predict"):
        with open("./sources/raining-money.gif", "rb") as file_1:
            contents = file_1.read()
            data_url_yes = base64.b64encode(contents).decode("utf-8") 
        with open("./sources/no-spider-man.gif", "rb") as file_2:
            contents = file_2.read()
            data_url_no = base64.b64encode(contents).decode("utf-8")
        with open('./sources/LGB_auc_0.6582.pickle', 'rb') as file_3:
            model = pickle.load(file_3)[0]
            prediction = model.predict(single_sample)
        if prediction[0]:
            st.error('Sorry, you will not get the loan from Bank')
            st.markdown(f'<img src="data:image/gif;base64,{data_url_no}" alt="cat gif">', unsafe_allow_html=True)
        else:
            st.success('Congratulations, you will get the loan from Bank')
            st.markdown(f'<img src="data:image/gif;base64,{data_url_yes}" alt="cat gif">', unsafe_allow_html=True)