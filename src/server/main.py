from server.component import ServerComponent

# Create and run the main component
comp = ServerComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
