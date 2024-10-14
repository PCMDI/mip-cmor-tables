
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
from mip_cmor_tables.models.activity import Activity
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


class Experiment(ConfiguredBaseModel):
    """
    an 'experiment' refers to a specific, controlled simulation conducted using climate models to investigate particular aspects of the Earth's climate system. These experiments are designed with set parameters, such as initial conditions, external forcings (like greenhouse gas concentrations or solar radiation), and duration, to explore and understand climate behavior under various scenarios and conditions.
    """

    id: str 
    validation_method: str = Field(default ="list")
    activity: List[str] = Field(default_factory=list)
    description: str 
    tier: Optional[int] 
    experiment_id: str 
    sub_experiment_id: Optional[List[str]] 
    experiment: str 
    required_model_components: Optional[List[str]] 
    additionnal_allowed_model_components: Optional[List[str]] = Field(default_factory=list) 
    start_year: Optional[int] 
    end_year: Optional[int] 
    min_number_yrs_per_sim: Optional[int] 
    parent_activity_id: Optional[List[str]] 
    parent_experiment_id: Optional[List[str]] 


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Experiment.model_rebuild()
