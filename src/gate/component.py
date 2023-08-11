# pylint: disable=all
from common.py.component import Component
from common.py.component.roles import NodeRole
from common.py.utils import UnitID

comp = Component(UnitID("infra", "gate"), NodeRole(), module_name=__name__)
app = comp.app()

comp.run()
