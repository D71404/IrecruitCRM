import streamlit as st
from models.database import Database
from models.auth import Auth
from fastapi import FastAPI
import uvicorn
from threading import Thread

# Create FastAPI app for health checks
app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Run FastAPI in a separate thread
def run_health_check():
    uvicorn.run(app, host="0.0.0.0", port=8080)

Thread(target=run_health_check, daemon=True).start()

import pages.dashboard as dashboard
import pages.candidates as candidates
import pages.clients as clients
import pages.jobs as jobs
import pages.timesheets as timesheets
import pages.tasks as tasks
import pages.reports as reports
import pages.user_management as user_management
import pages.login as login
from components.navigation import render_navigation, handle_logout
import importlib
import sys

# Initialize database
db = Database()

# Initialize session state variables and validate session
if ('authenticated' not in st.session_state or 
    'user' not in st.session_state or 
    'session_id' not in st.session_state):
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.session_id = None
elif st.session_state.authenticated and st.session_state.user:
    # Validate session on each page load
    auth = Auth()
    if not auth.validate_session(st.session_state.user['id'], st.session_state.session_id):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.session_id = None

# Add custom CSS for sidebar navigation
st.markdown("""
    <style>
    /* Mobile-friendly styles */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* Adjust form layouts */
        form {
            padding: 1rem !important;
        }

        /* Make tables scrollable horizontally */
        .stDataFrame {
            overflow-x: auto !important;
        }

        /* Adjust button sizes */
        .stButton > button {
            width: 100% !important;
            margin: 0.5rem 0 !important;
        }

        /* Optimize navigation */
        [data-testid="stSidebarNav"] {
            min-width: unset !important;
        }
    }

    /* Full width layout */
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hide file paths */
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    .css-1dp5vir {
        visibility: hidden;
    }
    .css-1aehpvj {
        display: none;
    }
    .css-1vq4p4l {
        padding-top: 1rem;
    }

    /* Style form fields and labels */
    .stTextInput > label, .stTextArea > label, .stSelectbox > label, .stFileUploader > label {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: #2c3338 !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }

    /* Required field indicator */
    .stTextInput > label[aria-label*="*"], 
    .stTextArea > label[aria-label*="*"],
    .stSelectbox > label[aria-label*="*"] {
        font-weight: 600 !important;
    }

    /* Input field styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        font-size: 1rem !important;
        padding: 0.75rem !important;
        border: 1px solid #cfd8dc !important;
        border-radius: 6px !important;
        background-color: #ffffff !important;
        width: 100% !important;
        color: #2c3338 !important;
    }

    /* Focus state */
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #169e81 !important;
        box-shadow: 0 0 0 2px rgba(22, 158, 129, 0.1) !important;
    }

    /* Style navigation items */
    .stRadio > label {
        font-size: 1.4rem;
        font-weight: 500;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        border-radius: 4px;
        transition: background-color 0.2s;
        display: block;
        background-color: rgba(255, 255, 255, 0.05);
    }

    /* Increase emoji/icon sizes */
    .stRadio label:before {
        font-size: 1.6rem;
        margin-right: 0.75rem;
        vertical-align: middle;
    }

    .stRadio > label:hover {
        background-color: #f0f2f6;
    }

    /* Hide radio button circles */
    .stRadio input {
        display: none;
    }

    /* Custom styling for sidebar */
    .css-1d391kg {
        padding-top: 2rem;
    }

    /* Improve content layout */
    .stApp {
        margin: 0 auto;
    }

    [data-testid="stSidebarNav"] {
        min-width: 200px;
    }

    /* Button styling */
    button {
        background-color: #169e81 !important;
    }
    button:hover {
        background-color: #138a71 !important;
    }

    /* Responsive table styling */
    .dataframe {
        width: 100% !important;
        font-size: 0.9rem !important;
    }

    @media screen and (max-width: 480px) {
        /* Further adjustments for very small screens */
        .block-container {
            padding: 0.5rem !important;
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            font-size: 16px !important; /* Prevent zoom on iOS */
        }

        /* Make sure buttons are easily tappable */
        .stButton > button {
            min-height: 44px !important;
        }

        /* Adjust form layout */
        form {
            padding: 1rem 0.5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Navigation menu with icons and better organization
pages = {
    "📊 Dashboard": dashboard,
    "👥 Candidates": candidates,
    "🏢 Clients": clients,
    "💼 Jobs": jobs,
    "📝 Timesheets": timesheets,
    "✅ Tasks": tasks,
    "📈 Reports": reports,
    "👤 User Management": user_management
}

# Check if user is authenticated
if not st.session_state.authenticated:
    login.render()
else:
    # Add logo to the top left
    st.image("pixelcut-export.jpeg", width=200)

    # Render navigation with logout button
    render_navigation()

    # Create sidebar navigation
    selected_page = st.sidebar.radio("", list(pages.keys()), label_visibility="collapsed")

    # Function to reload a module
    def reload_module(module):
        try:
            importlib.reload(module)
        except Exception as e:
            st.error(f"Error reloading module: {str(e)}")

    # Handle logout if requested
    if st.session_state.get('logout_requested', False):
        if handle_logout():
            st.rerun()

    # Render selected page with error handling
    try:
        # Get the selected module
        selected_module = pages[selected_page]

        # Reload the module to ensure fresh content
        reload_module(selected_module)

        # Render the page
        selected_module.render()
    except Exception as e:
        st.error(f"Error rendering page: {str(e)}")
        st.error("Please try refreshing the page or contact support if the issue persists.")