import streamlit as st
import os
from pathlib import Path

# Updated to match your specific directory structure
BASE_DIR = Path.home() / ".openclaw"
WORKSPACE_DIR = BASE_DIR / "workspace"
LOGS_DIR = BASE_DIR / "logs" # Placeholder for logs

st.set_page_config(page_title="OpenClaw Health Monitor", layout="wide")
st.title("📟 OpenClaw Agent Dashboard")

col1, col2 = st.columns(2)

def read_file_content(file_path):
    # Ensure file_path is a Path object for is_file()
    path_obj = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not path_obj.is_file():
        return f"File not found: {path_obj}"
    try:
        return path_obj.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file {path_obj}: {e}"

# --- Sidebar for Navigation ---
st.sidebar.title("Navigation")
# Removed "Process Control" and simplified log options for isolation
menu_options = ["Memory Viewer", "Task Tracker", "Logs"]
choice = st.sidebar.selectbox("Go to", menu_options)

# --- Main Content Area ---
if choice == "Memory Viewer":
    st.header("Memory Viewer")
    st.subheader("~/.openclaw/MEMORY.md")
    st.code(read_file_content(WORKSPACE_DIR / "MEMORY.md"))

    st.subheader("~/.openclaw/SOUL.md")
    st.code(read_file_content(WORKSPACE_DIR / "SOUL.md"))

elif choice == "Task Tracker":
    st.header("Task Tracker")
    st.subheader("HEARTBEAT Status")
    heartbeat_content = read_file_content(WORKSPACE_DIR / "HEARTBEAT.md")
    st.text_area("HEARTBEAT.md Content", heartbeat_content, height=300)
    st.write("*(Task tracking requires parsing specific directives from HEARTBEAT.md to show a progress bar.)*")

elif choice == "Logs":
    st.header("Execution Logs")
    st.warning("Streaming live execution logs requires specific system configuration.")
    # Simplified log reading attempt
    gateway_log_path = LOGS_DIR / "gateway.log"
    if gateway_log_path.is_file():
        try:
            with open(gateway_log_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                if lines:
                    st.code("\n".join(lines[-15:])) # Show last 15 lines
                else:
                    st.info("Log file is empty.")
        except Exception as e:
            st.error(f"Error reading log file: {e}")
    else:
        st.info(f"Log file not found at {gateway_log_path}. Waiting for data...")

# --- Real-time Updates (Optional - basic refresh button) ---
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Content"):
    st.rerun()
