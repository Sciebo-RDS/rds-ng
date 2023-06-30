from common.py.component import Component, ComponentID, ComponentRole

comp = Component(ComponentID("infra", "gate"), ComponentRole.SERVER | ComponentRole.CLIENT, module_name=__name__)
app = comp.app()

comp.run()
