
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




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


class Variable(ConfiguredBaseModel):
    """
    
    a variable refers to a specific type of climate-related quantity or measurement that is simulated and stored in a data file. These variables represent key physical, chemical, or biological properties of the Earth system and are outputs from climate models.
    Each variable captures a different aspect of the climate system, such as temperature, precipitation, sea level, radiation, or atmospheric composition.
    Examples of Variables: tas: Near-surface air temperature (often measured at 2 meters above the surface) pr: Precipitation psl: Sea level pressure zg: Geopotential height rlut: Top-of-atmosphere longwave radiation siconc: Sea ice concentration co2: Atmospheric CO2 concentration

    """

    id: str 
    cmip_acronym: str 
    validation_method: str = Field(default = "list")
    long_name: str 
    standard_name: Optional[str] 
    type: str 
    units: Optional[str] 


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Variable.model_rebuild()
