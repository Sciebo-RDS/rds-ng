from common.py.app import RDSApp


rds = RDSApp("rds.gate", module_name=__name__)
app = rds.wsgi_app()

@rds.core.flask.route('/')
def hello():
    return str(rds)
