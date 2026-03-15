import streamlit as st
import os
import subprocess
import psutil
import time
import sys

# --- Configuration ---
MEMORY_FILE = os.path.expanduser("~/.openclaw/MEMORY.md")
SOUL_FILE = os.path.expanduser("~/.openclaw/SOUL.md")
HEARTBEAT_FILE = os.path.expanduser("~/.openclaw/HEARTBEAT.md")
# For logs, we'll simulate it or try to access recent output if possible.
# Direct access to agent's stdout/stderr stream over time is complex.
# We'll start with showing recent system messages if available, or a placeholder.

# --- Helper Functions ---

def read_file_content(file_path):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def get_current_process_pid():
    # This attempts to find the PID of the streamlit process itself, or the parent python process.
    # Finding the exact 'OpenClaw' agent PID can be tricky as it typically runs the agent as a child process.
    # We'll try to find the python process that is currently running this script.
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if this process is running streamlit or is the parent python process
            if 'streamlit' in ' '.join(proc.info['cmdline']) and current_pid in proc.children(recursive=True):
                return proc.pid
            if sys.executable in ' '.join(proc.info['cmdline']) and proc.pid == current_pid:
                return current_pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

def stop_gateway_process():
    pid_to_stop = get_current_process_pid()
    if pid_to_stop:
        try:
            st.warning(f"Attempting to stop process with PID: {pid_to_stop}")
            parent_process = psutil.Process(pid_to_stop)
            # In a real scenario, you might want to be more specific about which process to kill.
            # For this example, we'll try to terminate the Streamlit process itself.
            parent_process.terminate() # Send SIGTERM
            parent_process.wait(timeout=5) # Wait for termination
            st.success(f"Process PID {pid_to_stop} terminated.")
            # To really stop OpenClaw, we might need to kill child processes or the parent OpenClaw shell.
            # This is a simplified attempt.
            return True
        except psutil.NoSuchProcess:
            st.error(f"Process PID {pid_to_stop} not found.")
            return False
        except psutil.AccessDenied:
            st.error(f"Permission denied to terminate process PID {pid_to_stop}. Please run with elevated privileges or manually kill.")
            return False
        except Exception as e:
            st.error(f"Error stopping process PID {pid_to_stop}: {e}")
            return False
    else:
        st.error("Could not find the relevant process PID to stop.")
        return False

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="OpenClaw Dashboard")
st.title("OpenClaw Dashboard")

# --- Sidebar for Navigation ---
st.sidebar.title("Navigation")
menu_options = ["Memory Viewer", "Task Tracker", "Logs", "Process Control"]
choice = st.sidebar.selectbox("Go to", menu_options)

# --- Main Content Area ---
if choice == "Memory Viewer":
    st.header("Memory Viewer")
    st.subheader("~/.openclaw/MEMORY.md")
    st.code(read_file_content(MEMORY_FILE))

    st.subheader("~/.openclaw/SOUL.md")
    st.code(read_file_content(SOUL_FILE))

elif choice == "Task Tracker":
    st.header("Task Tracker")
    st.subheader("HEARTBEAT Status")
    heartbeat_content = read_file_content(HEARTBEAT_FILE)
    st.text_area("HEARTBEAT.md Content", heartbeat_content, height=300)
    # Basic progress bar simulation based on HEARTBEAT.md interpretation
    # This part requires more specific logic for parsing HEARTBEAT.md tasks.
    # For now, we'll display content and a placeholder.
    st.write("*(Task tracking requires parsing specific directives from HEARTBEAT.md to show a progress bar.)*")

elif choice == "Logs":
    st.header("Execution Logs")
    st.write("*(Displaying recent execution logs)*")
    # This is a placeholder. Accessing live logs is complex.
    # We could potentially try to read a log file if OpenClaw writes to one,
    # or use subprocess to capture output if this were a wrapper.
    # For now, a simple message.
    st.warning("Streaming live execution logs requires specific system configuration.")
    st.text("Last 20 active messages from the system would appear here.")
    # Example: Displaying recent system messages from this session's context if available.
    # This might need access to session history or a persistent log.
    # Example: st.text(subprocess.run(['tail', '-n', '20', '/path/to/agent.log'], capture_output=True, text=True).stdout)

elif choice == "Process Control":
    st.header("Process Control")
    st.warning("Use this with caution. Stopping the gateway process will abruptly end the OpenClaw agent.")
    if st.button("Stop Gateway Process"):
        st.session_state['stop_process'] = True # Trigger backend action

    if 'stop_process' in st.session_state and st.session_state['stop_process']:
        if stop_gateway_process():
            st.success("Gateway process termination initiated. The dashboard may become unresponsive.")
            # Note: Streamlit apps might not gracefully exit on termination signals this way.
        else:
            st.error("Failed to stop the gateway process. Check permissions or try manually.")
        st.session_state['stop_process'] = False # Reset state

# --- Real-time Updates (File Watching Simulation) ---
# This is a basic way to force a re-run to check for file changes.
# A more robust solution might involve background threads or specific Streamlit rerun mechanisms.
# For now, we rely on user interaction or the simple "Stop Gateway" action to trigger a refresh potentially.
# To make it more real-time, one would typically use components or background checks.
# Let's add a simple refresh mechanism.
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Content"):
    st.rerun()
