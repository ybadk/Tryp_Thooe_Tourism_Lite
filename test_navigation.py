import streamlit as st

st.title("Navigation Test")

# Test the navigation links
nav_links = [
    ("Places Gallery", "gallery", '🏛️'),
    ("Individual Places", "individual_places", '📁'),
    ("Booking Form", "booking", '📝'),
    ("Weather Guide", "weather_guide", '🌤️'),
    ("Analytics", "analytics", '📊'),
    ("Contact Info", "contact", '📞'),
    ("AI Chat Assistant", "chat", '🤖'),
    ("Email Secretary", "email_secretary", '📧'),
]

st.write("Available Navigation Links:")
for text, key, icon in nav_links:
    st.write(f"{icon} {text} ({key})")

# Test current section
if 'current_section' not in st.session_state:
    st.session_state.current_section = None

st.write(f"Current section: {st.session_state.current_section}")

# Test buttons
for text, key, icon in nav_links:
    if st.button(f"{icon} {text}", key=f"test_{key}"):
        st.session_state.current_section = key
        st.rerun()

if st.session_state.current_section == 'email_secretary':
    st.success("Email Secretary section is working!")
    st.write("This means the navigation is properly configured.") 