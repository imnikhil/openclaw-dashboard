import streamlit as st
import os
from pathlib import Path

# Updated to match your specific directory structure
BASE_DIR = Path.home() / ".openclaw"
WORKSPACE_DIR = BASE_DIR / "workspace"
LOGS_DIR = BASE_DIR / "logs" # Note: Specific log file handling is not implemented in this snippet

st.set_page_config(page_title="OpenClaw Health Monitor", layout="wide")
st.title("📟 OpenClaw Agent Dashboard")

col1, col2 = st.columns(2)

def show_md(file_path, title):
 with st.expander(title, expanded=True):
 if file_path.is_file(): # Use is_file() to check if it's a file
 st.markdown(file_path.read_text())
 else:
 st.info(f"Waiting for {title} data...")

with col1:
 show_md(WORKSPACE_DIR / "SOUL.md", "🧠 Agent Soul")
 show_md(WORKSPACE_DIR / "IDENTITY.md", "👤 Agent Identity")

with col2:
 show_md(WORKSPACE_DIR / "HEARTBEAT.md", "💓 Live Heartbeat")
 # Show the latest log entries
 gateway_log = LOGS_DIR / "gateway.log" # Assuming gateway.log exists in logs directory
 with st.expander("📝 System Logs", expanded=True):
 if gateway_log.is_file(): # Check if log file exists
 try:
 with open(gateway_log, 'r', encoding='utf-8') as f:
 lines = f.read().splitlines()
 st.code("\n".join(lines[-15:])) # Show last 15 lines
 except Exception as e:
 st.error(f"Error reading log file: {e}")
 else:
 st.info(f"Waiting for log data at {gateway_log}...")

# --- Real-time Updates (Optional - basic refresh button) ---
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Content"):
 st.rerun()
