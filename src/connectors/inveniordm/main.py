from connectors.inveniordm.component import InvenioRDMConnectorComponent

# Create and run the main component
comp = InvenioRDMConnectorComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
