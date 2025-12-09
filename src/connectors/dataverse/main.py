from connectors.dataverse.component import DataverseConnectorComponent

# Create and run the main component
comp = DataverseConnectorComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
