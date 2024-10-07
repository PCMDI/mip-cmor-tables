from mip_cmor_tables.models.frequency import Frequency
from pathlib import Path
from pydantic import ValidationError
import pytest

import json
input_dir = Path("datadescriptor/frequency/")


def test_terms():
    for p in input_dir.iterdir():
        if p.suffix==".json":
            try:
                # Load valid JSON into the model
               py_instance = Frequency.model_validate_json(p.read_text())
            except ValidationError as exc:
                pytest.fail(f"ValidationError was raised for \nTerms : '{p.stem}'\nPath : {str(p)}\nError :  {exc.errors()[0]}")
            
