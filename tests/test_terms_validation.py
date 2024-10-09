from mip_cmor_tables.models.frequency import Frequency
from mip_cmor_tables.models.activity import Activity
from mip_cmor_tables.models.experiment import Experiment
from mip_cmor_tables.models.license import License
from mip_cmor_tables.models.source import Source
from mip_cmor_tables.models.source_type import SourceType
from mip_cmor_tables.models.sub_experiment import SubExperiment
from pathlib import Path
from pydantic import ValidationError
import pytest

import json

def validate_terms(input_dir, model):
    for p in input_dir.iterdir():
        if p.suffix==".json":
            try:
                # Load valid JSON into the model
               py_instance = model.model_validate_json(p.read_text())
            except ValidationError as exc:
                pytest.fail(f"ValidationError was raised for \nTerms : '{p.stem}'\nPath : {str(p)}\nError :  {exc.errors()[0]}")
 
def test_frequency():
    validate_terms(Path("datadescriptor/frequency/"),Frequency)

def test_activity():
    validate_terms(Path("datadescriptor/activity/"),Activity)

def test_experiment():
    validate_terms(Path("datadescriptor/experiment/"),Experiment)

def test_sub_experiment():
    validate_terms(Path("datadescriptor/sub_experiment/"),SubExperiment)


def test_model_component():
    validate_terms(Path("datadescriptor/source_type/"),SourceType)

def test_model_source():
    validate_terms(Path("datadescriptor/source/"),Source)

def test_model_license():
    validate_terms(Path("datadescriptor/license/"),License)

