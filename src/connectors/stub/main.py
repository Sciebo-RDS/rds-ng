from connectors.stub.component import StubConnectorComponent

# Create and run the main component
comp = StubConnectorComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
