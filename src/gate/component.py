from common.py.app import RDSApp

app = RDSApp(module_name=__name__)
flask = app.core.flask

    
@flask.route('/')
def hello():
    return str(app)
