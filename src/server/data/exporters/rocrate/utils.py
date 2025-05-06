from dataclasses import asdict
from typing import Callable, List
from urllib.parse import quote

from rocrate.model.contextentity import ContextEntity
from rocrate.model.data_entity import DataEntity
from rocrate.model.root_dataset import RootDataset
from rocrate.rocrate import ROCrate

from common.py.data.entities.project.project import Project


def with_files(func: Callable) -> Callable:
    """
    A decorator that processes files metadata associated with a project and adds them to a crate.

    Args:
        func (Callable): The function to be decorated. It should return a crate object.

    Returns:
        Callable: The wrapped function that processes files metadata and adds them to the crate.

    The wrapped function expects the following keyword arguments:
        project (Project): An object that contains project features with resources metadata and shared objects.

    """
    def wrapper(*args, **kwargs):
        crate = func(*args, **kwargs)

        for key, propertyObjects in kwargs["project"].features.resources_metadata.metadata.items():
            file: DataEntity = crate.add_file(key, dest_path=quote(key.removeprefix("/"))) # pyright: ignore[reportAssignmentType]

            for po in propertyObjects: 
                refObjects = [o for o in kwargs["project"].features.shared_objects if o.id in po.refs]

                # add simple values
                for k, v in po.value.items():
                    file[k] = v

                # add references
                for o in refObjects:
                    file[o.type] =  [ContextEntity(crate=crate, identifier=id) for id in file.get(o.type, [])] + [ContextEntity(crate=crate, identifier=o.id)]
        return crate
    return wrapper

def with_context_entities(func: Callable) -> Callable:
    """
    A decorator that adds context entities to the crate returned by the decorated function.

    This decorator processes shared objects from the project's features and adds them as context entities to the crate.
    It also handles references between shared objects by updating the properties of the context entities accordingly.

    Args:
        func (Callable): The function to be decorated. It should return a crate object.

    Returns:
        Callable: The wrapped function that adds context entities to the crate.

    The wrapped function expects the following keyword arguments:
    project (Project): An object that contains project features with shared objects.

    """
    def wrapper(*args, **kwargs):
        crate = func(*args, **kwargs)

        for sharedObject in kwargs["project"].features.shared_objects:
            properties = {"@type": sharedObject.type} | asdict(sharedObject).get("value", {})
            entity: ContextEntity = crate.add(ContextEntity(crate=crate, identifier=quote(sharedObject.id), properties=properties)) # pyright: ignore[reportAssignmentType]

            # add references
            refObjects = [o for o in kwargs["project"].features.shared_objects if o.id in sharedObject.refs]
            for o in refObjects:
                entity[o.type] =  [ContextEntity(crate=crate, identifier=id) for id in entity.get(o.type, [])] + [ContextEntity(crate=crate, identifier=quote(o.id))]
        return crate
    return wrapper

def with_project_metadata(func: Callable) -> Callable:
    """
    A decorator that adds project metadata to the root dataset of a crate.

    This decorator wraps a function that returns a crate object and modifies
    the root dataset of the crate by adding metadata from the project's features.

    Args:
        func (callable): The function to be decorated. It should return a crate object.

    Returns:
        callable: The wrapped function that adds project metadata to the crate's root dataset.

    The wrapped function expects the following keyword arguments:
    project (Project): An object that contains project features with project metadata and shared objects.
    """
    def wrapper(*args, **kwargs):
        crate = func(*args, **kwargs)

        root: RootDataset = crate.dereference("./")

        for m in [m for m in kwargs["project"].features.project_metadata.metadata if "datacite" in m.id]: # HACK

            # add simple values
            for k, v in m.value.items():
                root[k] = v

            # add references
            refObjects = [o for o in kwargs["project"].features.shared_objects if o.id in m.refs]
            for o in refObjects:
                root[o.type] =  [ContextEntity(crate=crate, identifier=id) for id in root.get(o.type, [])] + [ContextEntity(crate=crate, identifier=o.id)]
        return crate
    return wrapper

def with_context(func: Callable) -> Callable:
    """
    A decorator that adds the context URLs of all ProjectMetadataFeature profiles marked GLOBAL to the metadata of the crate object returned by the decorated function.

    Args:
        func (callable): The function to be decorated. It should return an object that has a 'metadata' attribute with an 'extra_contexts' list.

    Returns:
        callable: The wrapped function that appends an extra context URL to the crate's metadata.

    TODO: Add contexts for future profiles (custom, object resources etc.)
    """
    def get_global_contexts() -> List[str]:
        from common.py.data.entities.metadata import (MetadataProfileContainer,
                                                      filter_containers)
        from common.py.data.entities.project.features.project_metadata_feature import \
            ProjectMetadataFeature

        from ....component import ServerComponent
        
        profile_containers = ServerComponent.instance().server_data.profile_containers
        filtered_containers = filter_containers(
            profile_containers,
            category=ProjectMetadataFeature.feature_id,
            role=MetadataProfileContainer.Role.GLOBAL,
        )
        return [
            i.profile.metadata.context
            for i in filtered_containers
            if i.profile.metadata.context is not None
        ]
    
    def wrapper(*args, **kwargs):
        crate = func(*args, **kwargs)
        
        # add future contexts here
        contexts = [*get_global_contexts()]
        crate.metadata.extra_contexts.extend(contexts)

        return crate
    return wrapper


@with_context
@with_files
@with_context_entities
@with_project_metadata
def make_ro_crate(project: Project) -> ROCrate:
    """
    Returns a Research Object Crate (RO-Crate) for the given project.

    This function is decorated with several wrappers to ensure that
    the necessary context, files, context entities, and project metadata are
    included in the RO-Crate.

    Args:
        project (Project): The project for which the RO-Crate is to be created.

    Returns:
        ROCrate: An instance of the ROCrate class representing the generated RO-Crate.
    """
    return ROCrate()