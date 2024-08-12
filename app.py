from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        ##Convert to bytes        
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()# encode to base64
            }
        ]
        return pdf_parts
    else:
      raise FileNotFoundError("No File Uploaded")

##Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Job-Fit Analyzer")
input_text=st.text_area("Job Description:", key="input") 
uploaded_file=st.file_uploader("Upload your resume(PDF).......", type=["pdf"]) 

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1=st.button("Tell me About the Resume")
submit2=st.button("How Can I Improvise my Skills")
submit3=st.button("Percentage Match")

input_prompt1="""
You are an experienced HR With Tech Experience in the field of any job role from data science or Full Stack Web development or Big Data Engineering or DEVOPS or Data Analyst, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the job role 
Highlight the strengths and weaknesses of the applicant in relation to the specified job role

"""
input_prompt2= """
You are an Technical Human Resource Manager with expertise in any field from these either data science or Full Stack Web development or Big Data Engineering or DEVOPS or Data Analyst
your role is to scrutinize the resume in the light of the job description provided.
Share your insights on the candidates suitability for the role provided
"""
input_prompt3="""
You are a skilled ATS(Applicant Tracking System) scanner with a deep understanding in the fieldd of any job role from data science or Full Stack Web development or Big Data Engineering or DEVOPS or Data Analyst and has deep ATS functionality
your task is to evaluate the resume against the provided job description.Give me the percentage match if the resume matches
against the job description.First the output should come as percentage and then keywords missing.
"""

if submit1:
  if uploaded_file is not None:
    pdf_content=input_pdf_setup(uploaded_file)
    response=get_gemini_response(input_prompt1,pdf_content,input_text)
    st.subheader("The Response is:")
    st.write(response)
  else:
    st.write("Please upload the resume")

if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)

    else:
        st.write("Please upload the resume")


if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)

    else:
        st.write("Please upload the resume")    
    



