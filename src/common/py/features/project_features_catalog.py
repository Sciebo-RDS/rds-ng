from .project_feature import ProjectFeature
from ..utils import ItemsCatalog


@ItemsCatalog.define()
class ProjectFeaturesCatalog(ItemsCatalog[ProjectFeature]):
    """
    Global catalog of all registered backend types.

    This is a globally accessible list of all project features, associated with their respective IDs.
    """
