from common.py.component import (
    BackendComponent,
    ComponentType,
    ComponentUnit,
)
from common.py.component.roles import NodeRole
from common.py.utils import UnitID

from gate.main import run_gate
from gate.settings.gate_settings import get_gate_settings


# Create the component and add its default settings
comp = BackendComponent.create(
    UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.GATE),
    NodeRole(),
    module_name=__name__,
)
app = comp.app()  # Expose a variable called 'app' for the WSGI launcher

comp.data.config.add_defaults(get_gate_settings())

# Finally, run the component and the gate
comp.run()
run_gate(comp)
