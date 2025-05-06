from connectors.zenodo.component import ZenodoConnectorComponent

# Create and run the main component
comp = ZenodoConnectorComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
