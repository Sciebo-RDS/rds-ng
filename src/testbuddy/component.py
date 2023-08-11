# pylint: disable=all
from common.py.component import Component
from common.py.component.roles import LeafRole
from common.py.utils import UnitID

comp = Component(UnitID("infra", "testbuddy"), LeafRole(), module_name=__name__)
app = comp.app()

comp.run()
