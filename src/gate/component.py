from common.py.component import Component, ComponentID


comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()


@comp.core.flask.route('/')
def hello():
    return str(comp)
