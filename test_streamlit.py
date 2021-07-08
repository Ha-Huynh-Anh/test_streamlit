import streamlit as st
import pandas as pd

@st.cache
def get_sym_df(url1):
  sym_df = pd.read_csv(url1)
  sym_df = pd.DataFrame(sym_df)
  sym_df = sym_df.loc[:,('eng','viet')]
  return sym_df

url_sym_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/sym_df.csv'
sym_df = get_sym_df(url_sym_df)

sym_input_vie = st.multiselect('Các triệu chứng của bạn', sym_df.viet.values)
st.write(sym_input_vie)