from gate.component import GateComponent

# Create and run the main component
comp = GateComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
