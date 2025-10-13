from domo.component import DomoComponent

# Create and run the main component
comp = DomoComponent()
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.run()
