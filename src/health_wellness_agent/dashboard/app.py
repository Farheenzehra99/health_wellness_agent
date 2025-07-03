import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Set page config with dark theme
st.set_page_config(
    page_title="Health & Wellness Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and gradient styling
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Gradient name styling */
    .name-gradient {
        background: linear-gradient(45deg, #ff3366, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px !important;
        font-weight: 800 !important;
        text-align: center;
        padding: 20px 0;
    }
    
    /* Dark sidebar */
    .css-1d391kg {
        background-color: #1a1c23;
    }
    
    /* Other headings */
    h1, h2, h3 {
        background: linear-gradient(45deg, #0066ff, #ff3366);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    h4 {
        background: linear-gradient(45deg, #0066ff, #ff3366);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 400;
    }
    
    .stButton>button {
        background-color: #0066ff;
        color: white;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    
    .user-info {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
        /* Chat history button styling */
    .stButton>button {
        width: 100%;
        text-align: left;
        background-color: #1e2128;
        border: 1px solid #2d3139;
        margin: 2px 0;
        padding: 8px 12px;
        border-radius: 5px;
        color: #fafafa;
        font-size: 14px;
    }
    .stButton>button:hover {
        background-color: #2d3139;
        border-color: #0066ff;
    }
    
    /* Selected chat styling */
    .selected-chat {
        background-color: #1e2128;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #0066ff;
    }

</style>
""", unsafe_allow_html=True)

# Sidebar with chat history
with st.sidebar:
    st.markdown('<h3 class="name-gradient, font-weight:400 ">Made By:</h3>', unsafe_allow_html=True)
    st.markdown('<h3 class="name-gradient, font-weight:400 ">Syeda Farheen Zehra</h3>', unsafe_allow_html=True)
    st.markdown("### 💬 Chat History")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_chat' not in st.session_state:
        st.session_state.selected_chat = None
    
    # Display chat history as clickable items
    for idx, msg in enumerate(st.session_state.chat_history):
        if msg['role'] == 'user':
            # Create a clickable button for each chat
            if st.button(f"🗨 {msg['content'][:30]}...", key=f"chat_{idx}"):
                st.session_state.selected_chat = idx

    # Display selected chat
    if st.session_state.selected_chat is not None:
        st.markdown("### Selected Chat")
        idx = st.session_state.selected_chat
        if idx < len(st.session_state.chat_history):
            # Show user message
            user_msg = st.session_state.chat_history[idx]
            st.markdown(f"**You:** {user_msg['content']}")
            
            # Show AI response if available
            if idx + 1 < len(st.session_state.chat_history) and \
               st.session_state.chat_history[idx + 1]['role'] == 'assistant':
                ai_msg = st.session_state.chat_history[idx + 1]
                st.markdown(f"**Assistant:** {ai_msg['content']}")

# Main content
st.title("💪 AI Health & Wellness Planner")

# User Profile Section
with st.expander("📋 Your Profile", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Name", " ")
        age = st.number_input("Age", 15, 100, 25)
    with col2:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 60.0, 0.1)
        height = st.number_input("Height (cm)", 100, 220, 165)

    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    bmi_status = "Normal"
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    st.info(f"Your BMI: {bmi:.1f} ({bmi_status})")

# Get AI Recommendations
def get_ai_recommendations(age, weight, height, bmi, bmi_status):
    prompt = f"""As a health and wellness expert, provide personalized diet and exercise recommendations for a person with the following profile:
    - Age: {age} years
    - Weight: {weight} kg
    - Height: {height} cm
    - BMI: {bmi:.1f} ({bmi_status})
    
    Please provide specific recommendations in two categories:
    1. Diet recommendations
    2. Exercise recommendations
    
    Make the recommendations detailed but concise."""
    
    response = model.generate_content(prompt)
    return response.text

# Main chat interface
st.header("💬 Chat with Your Wellness Assistant")
user_input = st.chat_input("Ask me anything about your health and wellness...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        prompt = f"""As a health and wellness expert, respond to the following question. Consider the user's profile:
        - Age: {age} years
        - Weight: {weight} kg
        - Height: {height} cm
        - BMI: {bmi:.1f} ({bmi_status})

        User's question: {user_input}
        
        Provide a helpful and personalized response."""
        
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # Save to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# Get and display AI recommendations
if st.button("Get AI Recommendations"):
    with st.spinner("Generating personalized recommendations..."):
        recommendations = get_ai_recommendations(age, weight, height, bmi, bmi_status)
        st.markdown(recommendations)

# PDF Generation
def generate_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Add content to PDF
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, 800, "Health & Wellness Report")
    
    # User Profile
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Name: {user_name}")
    p.drawString(50, 730, f"Age: {age}")
    p.drawString(50, 710, f"Weight: {weight}kg")
    p.drawString(50, 690, f"Height: {height}cm")
    p.drawString(50, 670, f"BMI: {bmi:.1f} ({bmi_status})")
    
    # Add AI Recommendations
    recommendations = get_ai_recommendations(age, weight, height, bmi, bmi_status)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 630, "AI Recommendations:")
    p.setFont("Helvetica", 10)
    
    # Split recommendations into lines
    y_position = 610
    for line in recommendations.split('\n'):
        if line.strip():
            p.drawString(50, y_position, line[:100])
            y_position -= 15
    
    p.save()
    buffer.seek(0)
    return buffer

# PDF Download Button
if st.button("📄 Download Profile & Recommendations"):
    pdf = generate_pdf()
    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="wellness_report.pdf",
        mime="application/pdf"
    )