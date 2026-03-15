# OpenClaw Dashboard

A local dashboard application for the OpenClaw agent, providing quick access to key functionalities and information.

## Features
*   **Memory Viewer:** Easily access and view your  and  files.
*   **Task Tracker:** Monitor tasks parsed from  (basic display).
*   **Logs:** View recent execution logs (placeholder).
*   **Process Control:** A 'Stop Gateway' button to terminate the OpenClaw process (use with caution).

## Key Technical Tips
*   **Real-time Updates:** The dashboard aims to reflect changes in memory files. May require manual refresh or updates.
*   **The Kill Switch:** Includes functionality to attempt termination of the OpenClaw agent process.

## How to Install
Follow these steps to set up and run the dashboard:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/imnikhil/openclaw-dashboard.git
    cd openclaw-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scriptsctivate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the dashboard:**
    ```bash
    streamlit run app.py
    ```

The dashboard will be accessible at http://localhost:8501.

## Contributing
Contributions are welcome! Please open issues or submit pull requests to the repository.

## License
This project is licensed under the MIT License.
