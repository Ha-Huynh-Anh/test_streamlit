import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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

#train_df
@st.cache(allow_output_mutation=True)
def get_train_df(url1):
  train_df = pd.read_csv(url1)
  train_df = pd.DataFrame(train_df)
  train_df['vector'] = train_df.iloc[:,-133:-1].apply(lambda x: list(x), axis=1) ## sau nay nen tong quat hoa cac con so 133, 1, ...
  return train_df

# convert all into list
def get_disease(train_df, input_array):
    
    # cal similarity
    train_df['similar'] = train_df.vector.apply(lambda x: cosine_similarity(input_array,np.array([x]))[0][0])

    # disease result
    dis_result = train_df[train_df['similar'] > 0]
    dis_result = pd.DataFrame(dis_result)
    return dis_result.groupby('prognosis').max('similar').iloc[:,-1].sort_values(ascending=False)   

url_train_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/train_df.csv'
url_sym_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/sym_df.csv'
sym_df = get_sym_df(url_sym_df)
train_df = get_train_df('https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/train_df.csv')


sym_input_vie = st.multiselect('Các triệu chứng của bạn', sym_df.viet.values)
sym_input_eng = trans_sym(sym_input_vie)
input_array = np.array([sym_to_vector(sym_input_eng)])
st.write(get_train_df(train_df,input_array))

