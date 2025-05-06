from connectors.osf.component import OSFConnectorComponent

# Create and run the main component
comp = OSFConnectorComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
