from common.py.component import (
    BackendComponent,
    ComponentType,
    ComponentUnit,
)
from common.py.component.roles import NodeRole
from common.py.utils import UnitID

from gate.main import run_gate
from gate.settings.default_settings import get_default_settings


# Create the component, add its default settings, and finally run it

comp = BackendComponent.create(
    UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.GATE),
    NodeRole(),
    module_name=__name__,
)
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.data.config.add_defaults(get_default_settings())

comp.run(run_gate)
