import streamlit as st
import qrcode
from PIL import Image
import io
import cv2
import numpy as np
from PIL import Image

# Set page config and title 
st.set_page_config(page_title="📱 QR Code Scanner", page_icon="📱", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes shine {
        0% { background-position: -100% 50%; }
        100% { background-position: 200% 50%; }
    }
    .floating-emoji {
        display: inline-block;
        font-size: 4em;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.3));
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FF6B6B);
        background-size: 300% 300%;
        animation: gradientBG 5s ease infinite;
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 30px;
        padding: 1.2rem 3.5rem;
        border: none;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: translateY(-7px) scale(1.05);
        box-shadow: 0 15px 25px rgba(0,0,0,0.3);
    }
    .scan-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 4rem;
        border-radius: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border: 4px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .scan-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            transparent,
            rgba(255,255,255,0.1),
            transparent,
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    .stFileUploader {
        border: 4px dashed #4ECDC4;
        border-radius: 25px;
        padding: 30px;
        transition: all 0.5s ease;
        background: rgba(255,255,255,0.8);
    }
    .stFileUploader:hover {
        border-color: #FF6B6B;
        background: rgba(78, 205, 196, 0.15);
        transform: scale(1.03);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .sidebar .stRadio > label {
        background: rgba(78, 205, 196, 0.15);
        padding: 20px;
        border-radius: 20px;
        margin: 10px 0;
        transition: all 0.4s ease;
        border: 2px solid transparent;
    }
    .sidebar .stRadio > label:hover {
        background: rgba(78, 205, 196, 0.25);
        transform: translateX(8px);
        border-color: #4ECDC4;
    }
    .success-message {
        animation: pop 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    @keyframes pop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with enhanced gradient background
st.sidebar.markdown("""
    <div style='
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        padding: 30px;
        border-radius: 25px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        border: 3px solid rgba(255,255,255,0.2);
    '>
        <h2 style='text-align: center; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);'>✨ Scanner Options ✨</h2>
    </div>
""", unsafe_allow_html=True)
scan_option = st.sidebar.radio(
    "Choose Scan Method",
    ["Upload Image 📤", "Use Camera 📸"]
)

# Enhanced title and description with animation
st.markdown("""
    <div style='text-align: center;'>
        <span class='floating-emoji'>📱</span>
        <h1 style='
            display: inline-block;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4em;
            margin: 25px;
            text-shadow: 4px 4px 8px rgba(0,0,0,0.1);
        '>
            QR Code Scanner
        </h1>
        <span class='floating-emoji'>🔍</span>
    </div>
""", unsafe_allow_html=True)

# Enhanced scanner container
with st.container():
    st.markdown('<div class="scan-container">', unsafe_allow_html=True)
    
    if scan_option == "Upload Image 📤":
        uploaded_file = st.file_uploader("Choose a QR code image...", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded QR Code ✨', use_container_width=True)
                
                img_array = np.array(image)
                qr_detector = cv2.QRCodeDetector()
                data, bbox, _ = qr_detector.detectAndDecode(img_array)
                
                if data:
                    st.markdown(f"""
                        <div class='success-message' style='
                            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.3));
                            padding: 20px;
                            border-radius: 15px;
                            border-left: 5px solid #4CAF50;
                            margin: 20px 0;
                        '>
                            <h3 style='color: #4CAF50;'>🎉 Decoded QR Code Content:</h3>
                            <p style='font-size: 1.2em; color: #2E7D32;'>{data}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ No QR code found in the image")
                    
            except Exception as e:
                st.error(f"⚠️ Error processing image: {str(e)}")
    
    else:  # Enhanced Camera option
        camera_placeholder = st.empty()
        if st.button("📸 Start Camera", key="camera_button"):
            try:
                cap = cv2.VideoCapture(0)
                qr_detector = cv2.QRCodeDetector()
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to access camera")
                        break
                        
                    data, bbox, _ = qr_detector.detectAndDecode(frame)
                    
                    if data:
                        st.markdown(f"""
                            <div class='success-message' style='
                                background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.3));
                                padding: 20px;
                                border-radius: 15px;
                                border-left: 5px solid #4CAF50;
                                margin: 20px 0;
                            '>
                                <h3 style='color: #4CAF50;'>🎉 Decoded QR Code Content:</h3>
                                <p style='font-size: 1.2em; color: #2E7D32;'>{data}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        break
                        
                    camera_placeholder.image(frame, channels="BGR", use_column_width=True)
                    
                cap.release()
                
            except Exception as e:
                st.error(f"⚠️ Error accessing camera: {str(e)}")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Instructions
with st.expander("✨ How to Use ✨"):
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.15), rgba(255, 107, 107, 0.15));
        padding: 30px;
        border-radius: 25px;
        border-left: 6px solid #4ECDC4;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    '>
        <h3 style='color: #FF6B6B; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>✨ QR Scanner Guide:</h3>
        <ol style='color: #333; font-size: 1.2em; line-height: 1.8;'>
            <li>📱 Select your preferred scanning method from the sidebar</li>
            <li>📤 Upload a clear QR code image or use your camera</li>
            <li>🎯 Ensure the QR code is well-lit and centered</li>
            <li>✨ Get your results instantly with beautiful animations!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("<hr style='height: 3px; background: linear-gradient(45deg, #FF6B6B, #4ECDC4);'>", unsafe_allow_html=True)
st.markdown("""
    <div style='
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 25px;
        font-size: 1.3em;
    '>
        <h4>✨ Created with ❤️ by Dilsher Khaskheli ✨</h4>
        <p style='font-size: 0.8em; opacity: 0.8;'>Making QR scanning beautiful and efficient</p>
    </div>
""", unsafe_allow_html=True)
