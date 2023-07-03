from common.py.component import Component, ComponentID
from common.py.component.roles import NodeRole

comp = Component(ComponentID("infra", "gate"), NodeRole(), module_name=__name__)
app = comp.app()

comp.run()
