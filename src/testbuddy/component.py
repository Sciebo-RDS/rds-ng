from common.py.component import Component, ComponentID, ComponentRole

comp = Component(ComponentID("infra", "testbuddy"), ComponentRole.CLIENT, module_name=__name__)
app = comp.wsgi_app()
