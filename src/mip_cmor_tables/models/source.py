
from __future__ import annotations 
from datetime import (
    datetime,
    date
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    ClassVar,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic.version import VERSION  as PYDANTIC_VERSION 
if int(PYDANTIC_VERSION[0])>=2:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        RootModel,
        field_validator
    )
else:
    from pydantic import (
        BaseModel,
        Field,
        validator
    )

metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "allow",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass



class Source(ConfiguredBaseModel):
    """
    a 'source' refers to a numerical representations of the Earth's climate system. They simulate the interactions between the atmosphere, oceans, land surface, and ice. These models are based on fundamental physical, chemical, and biological processes and are used to understand past, present, and future climate conditions. Each source or model is typically associated with a specific research institution, center, or group. For instance, models like 'EC-Earth' are developed by a consortium of European institutes, while 'GFDL-CM4' is developed by the Geophysical Fluid Dynamics Laboratory (GFDL) in the United States.
    """

    id: str 
    validation_method: str = Field(default = "list")
    activity_participation: Optional[List[str]] 
    cohort: List[str] = Field(default_factory=list)
    organisation_id: List[str] = Field(default_factory=list)
    label : str
    label_extended: Optional[str] 
    license: Optional[Dict] = Field(default_factory=dict) 
    model_component: Optional[dict] 
    release_year: Optional[int] 

# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Source.model_rebuild()
