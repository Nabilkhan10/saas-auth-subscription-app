"""
Run the FastAPI application
"""

import uvicorn

if __name__ == "__main__":
    print("Starting SaaS Auth & Subscription App...")
    print("Server will be available at: http://localhost:8000")
    print("Press CTRL+C to stop the server\n")

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
