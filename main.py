import calc_marks
from answer_key import answer_key_1, answer_key_2
import streamlit as st

st.set_page_config(page_title = 'JEE ADVANCED 2025 Score Calculator')
st.header("JEE ADVANCED 2025 Score Calculator")
st.write("Enter url to calculate score")
url1=st.text_input("Enter url of paper 1 ")
url2=st.text_input("Enter url of paper 2 ")

if st.button("Give Score"):
    try:
        p1 = calc_marks.calc_marks(url1, answer_key_1)
        p2 = calc_marks.calc_marks(url2, answer_key_2)
        l= [p1 + p2, p1, p2]
        st.write("Total Marks: ",l[0])
        st.write("Paper 1 : ",l[1])
        st.write("Paper 2: ",l[2])
    except:
        st.write('Please Enter Correct URL')