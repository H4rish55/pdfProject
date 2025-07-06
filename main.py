import streamlit as st 
from pdfminer.high_level import extract_text
import pdfplumber
from pypdf import PdfReader
import io
from PIL import Image
import pytesseract

st.set_page_config(page_title = "Pdf Reader", layout = "centered")

st.title("Pdf Reader")
st.markdown("Upload your pdf file.")

uploaded_file = st.file_uploader("Upload your pdf file", type=["pdf"])

analyze_horizontal_vertical = st.button("Analyze paragraph")
double_space_btn = st.button("Double Spacing")
table_Btn = st.button("Analyze Tables")

def horizontal_word(file):
    text = extract_text(file)
    words = text.split()
    longest_word = max(words, key=len)
    st.markdown(f"The longest word is {longest_word} , It has {len(longest_word)} characters.")

def horizontal_line(file):
    text = extract_text(file)
    lines = text.splitlines()
    longest_line = max(lines, key=len)
    st.markdown(f"The longest line is '{longest_line}', It has {len(longest_line)} characters.")

def horizontal_para(file):
    text = extract_text(file)
    lines = text.splitlines()
    para = []
    buf = []
    blank_space = 0
    for line in lines:
        if line.strip():
            buf.append(line.strip())
            blank_space = 0
        else:
            blank_space += 1
            if blank_space >= 1 and buf:
                para.append(" ".join(buf))
                buf = []
                blank_space = 0
    
    longest_para = max(para, key=len)
    st.markdown(f"The longest paragraph is '{longest_para}', It has {len(longest_para)} characters.")
    st.markdown(f"The number of paragraphs is {len(para)}")

def double_spacing(file):
    text = extract_text(file)
    lines = text.splitlines()
    para = []
    buf = []
    blank_space = 0
    for line in lines:
        if line.strip():
            buf.append(line.strip())
            blank_space = 0
        else:
            blank_space += 1
            if blank_space >= 2 and buf:
                para.append(" ".join(buf))
                buf = []
                blank_space = 0
    if buf:
        para.append(" ".join(buf))
    
    longest_para = max(para, key=len)
    st.markdown(f"The longest paragraph is '{longest_para}', It has {len(longest_para)} characters.")

if uploaded_file and analyze_horizontal_vertical:
    horizontal_word(uploaded_file)
    horizontal_line(uploaded_file)
    horizontal_para(uploaded_file)

if uploaded_file and double_space_btn:
    horizontal_word(uploaded_file)
    horizontal_line(uploaded_file)
    double_spacing(uploaded_file)

enter_index = st.text_input("Enter the index of the table you want to extract")

def table_extraction(file):
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            table = page.extract_tables()
            st.markdown(f"There are total of {len(table)} tables.")
            st.markdown(f"Table {int(enter_index)+ 1} has {len(table[int(enter_index)])} datas.")


if uploaded_file and table_Btn:
    table_extraction(uploaded_file)

analyze_Image = st.button("Analyze Image")

def Image_reader(file):
    reader = PdfReader(file)
    page = reader.pages[0]
    for img_obj in page.images:
        img_bytes = img_obj.data
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, use_container_width= True)
        text = pytesseract.image_to_string(img, lang='eng')
        st.markdown(f"The Text in the Image says '{text}'")

if uploaded_file and analyze_Image:
    Image_reader(uploaded_file)



