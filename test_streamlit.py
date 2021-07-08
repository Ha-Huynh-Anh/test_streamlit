import streamlit as st
import pandas as pd

@st.cache
def get_sym_df(url1):
  sym_df = pd.read_csv(url1)
  sym_df = pd.DataFrame(sym_df)
  sym_df = sym_df.loc[:,('eng','viet')]
  return sym_df

def trans_sym(list_sym):
    """
    translate sym from list vie to list eng
    input: ['Yếu mệt','Da nổi mẩn']
    output: ['lethargy', 'nodal_skin_eruptions']
    """
    list_eng = []
    for i in list_sym:
        if i in list(sym_df.viet):
            index = list(sym_df.viet).index(i)
            list_eng.append(list(sym_df.eng)[index])
    return list_eng

# convert to array format
def sym_to_vector(list_input_sym):
    #  to convert sym to vector
    sym_input_vector = []    
    for i in list(sym_df.eng): 
        if i in list_input_sym:
            sym_input_vector.append(1)
        else:
            sym_input_vector.append(0)
    return sym_input_vector

url_sym_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/sym_df.csv'
sym_df = get_sym_df(url_sym_df)

sym_input_vie = st.multiselect('Các triệu chứng của bạn', sym_df.viet.values)
st.write(sym_input_vie)
st.write(trans_sym(sym_input_vie))
st.write(sym_to_vector(trans_sym(sym_input_vie)))
