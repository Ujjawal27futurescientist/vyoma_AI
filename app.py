import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (New Design)
st.markdown("""
<style>
    /* Main Background & Font */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #181B24;
        border-right: 1px solid #2D313F;
    }

    /* Header / Title Styling */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Input Fields & Text Area */
    .stTextArea textarea, .stTextInput input {
        background-color: #1E222D !important;
        color: #FFFFFF !important;
        border: 1px solid #2D313F !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4A90E2 !important;
        box-shadow: none !important;
    }

    /* Button Styling */
    button[kind="primary"], .stButton > button {
        background-color: #4A90E2 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    button[kind="primary"]:hover, .stButton > button:hover {
        background-color: #357ABD !important;
        transform: translateY(-2px);
    }

    /* Expander Styling */
    div[data-testid="stExpander"] {
        background-color: #181B24;
        border: 1px solid #2D313F;
        border-radius: 8px;
    }
    
    /* Metrics / Stats boxes if used */
    div[data-testid="stMetric"] {
        background-color: #1E222D;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2D313F;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.title("🎨 AI Image Studio")
st.markdown("Generate stunning images from text descriptions using state-of-the-art AI models.")

# Sidebar for Controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    model_choice = st.selectbox(
        "Select Model",
        ["Stable Diffusion XL", "DALL-E 3", "Midjourney V6 (Simulated)"],
        index=0
    )
    
    aspect_ratio = st.select_slider(
        "Aspect Ratio",
        options=["1:1", "16:9", "9:16", "4:3", "3:4"],
        value="1:1"
    )
    
    num_images = st.slider("Number of Images", 1, 4, 1)
    
    advanced_mode = st.expander("Advanced Options")
    with advanced_mode:
        guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
        steps = st.slider("Inference Steps", 10, 150, 50, 10)
        negative_prompt = st.text_area("Negative Prompt", placeholder="What to exclude from the image...")

# Main Content Area
prompt = st.text_area(
    "Enter your prompt", 
    height=100, 
    placeholder="Describe the image you want to create in detail..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button("✨ Generate Image", type="primary", use_container_width=True)

# Display Area
if generate_btn:
    if prompt:
        with st.spinner("Dreaming up your image..."):
            # ---------------------------------------------------------
            # TODO: INSERT YOUR IMAGE GENERATION LOGIC HERE
            # Example placeholder logic:
            import time
            time.sleep(2) # Simulating generation time
            
            # Placeholder image for demonstration
            st.image("https://placehold.co/1024x1024/1E222D/FFF?text=Generated+Image+Placeholder", use_column_width=True)
            # ---------------------------------------------------------
            
        st.success("Image generated successfully!")
        
        # Download / Action Buttons
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇️ Download", data=b"", mime="image/png", use_container_width=True)
        with c2:
            st.button("🔄 Variations", use_container_width=True)
        with c3:
            st.button("💾 Save to Gallery", use_container_width=True)
    else:
        st.warning("Please enter a prompt to generate an image.")

# Footer
st.markdown("---")
st.caption("Powered by Streamlit | AI Image Generation Demo v2.0")