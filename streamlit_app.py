import streamlit as st
import openai
from PIL import Image

# App Config
st.set_page_config(page_title="AI Image Generator & Monetization", page_icon="🎨", layout="centered")

# Initialize Session State for Credits
if 'credits' not in st.session_state:
    st.session_state.credits = 2  # 2 Free Credits for Users

# Sidebar Navigation / Pricing & Monetization
st.sidebar.title("💎 Upgrade Plan")
st.sidebar.write("Get unlimited AI image generations!")
st.sidebar.info("Price: Rs. 300 / Month")

st.sidebar.subheader("📲 Easypaisa Payment")
st.sidebar.write("Scan the QR code below or send payment to:")
st.sidebar.code("0300-1234567 (Laraib Ahmed)")

# Display Easypaisa QR Code if uploaded/available
try:
    qr_image = Image.open("1000079554.jpg")
    st.sidebar.image(qr_image, caption="Scan & Pay via Easypaisa", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("Easypaisa QR code image (1000079554.jpg) will appear here once uploaded.")

st.sidebar.subheader("🔑 Enter Activation Code")
activation_input = st.sidebar.text_input("Enter code after payment:")
if st.sidebar.button("Activate Unlimited"):
    if activation_input == "VIP2026":
        st.session_state.credits = 9999
        st.sidebar.success("Activated Unlimited Access!")
    else:
        st.sidebar.error("Invalid Code. Pay via Easypaisa to get code.")

# Main App Interface
st.title("🎨 AI Image & Video Generator")
st.write(f"🎁 Free Credits Left: **{st.session_state.credits}**")

# OpenAI API Key Input
user_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

prompt = st.text_area("Describe the image you want to generate:", placeholder="A futuristic cyberpunk city at sunset...")

if st.button("Generate Image"):
    if st.session_state.credits <= 0:
        st.error("❌ You have run out of free credits! Please upgrade via Easypaisa from the sidebar.")
    elif not user_api_key:
        st.warning("⚠️ Please enter your OpenAI API key to proceed.")
    elif not prompt:
        st.warning("⚠️ Please enter a prompt.")
    else:
        try:
            openai.api_key = user_api_key
            with st.spinner("✨ Generating your masterpiece with DALL-E 3..."):
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                st.image(image_url, caption=prompt, use_container_width=True)
                st.session_state.credits -= 1
                st.success(f"Image generated successfully! Credits remaining: {st.session_state.credits}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
