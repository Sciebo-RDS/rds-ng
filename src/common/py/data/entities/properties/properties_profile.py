from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from dataclasses_json import DataClassJsonMixin

### should probably be in a separate folder, is this is not specific to metadata but to general properties

ProfileID = Tuple[str, str]


@dataclass
class ProfileMetadata(DataClassJsonMixin):
    id: ProfileID
    displayLabel: str
    description: str
    context: Optional[str] = None

@dataclass
class ProfileClassInput(DataClassJsonMixin):
    id: str
    label: str
    type: str
    description: Optional[str] = None
    example: Optional[str] = None
    options: Optional[List[str]] = field(default_factory=list)
    hints: Optional[Dict] = None
    required: Optional[bool] = None


@dataclass
class ProfileClassRef(DataClassJsonMixin):
    classId: str
    required: Optional[bool] = False
    inline: Optional[bool] = False
    multiple: Optional[bool] = True

@dataclass
class ProfileClass(DataClassJsonMixin):
    id: str
    refs: List[ProfileClassRef] = field(default_factory=list)
    displayLabel: str = ""
    description: Optional[str] = None
    labelTemplate: str = ""
    required: Optional[bool] = False
    multiple: Optional[bool] = False
    example: Optional[str] = None
    input: List[ProfileClassInput] = field(default_factory=list)

ProfileClassDictionary = Dict[str, ProfileClass]
ProfileLayout = List[ProfileClass]

@dataclass
class PropertyProfile(DataClassJsonMixin):
    metadata: ProfileMetadata
    layout: ProfileLayout
    classes: ProfileClassDictionary = field(default_factory=dict)
    
