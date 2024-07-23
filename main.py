import uvicorn  # Import the Uvicorn server

# Check if the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Uvicorn server
    uvicorn.run(
        'app:app',  # The application instance to run (module_name:variable_name)
        host="127.0.0.1",  # The host address to bind to
        port=8000,  # The port to listen on
        reload=True  # Enable auto-reload for code changes (useful for development)
    )
