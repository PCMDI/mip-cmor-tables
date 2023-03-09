# (C) British Crown Copyright 2022, Met Office
# CC0-1.0 License
"""
CV handling class
"""
import glob
import json
import logging
import os
from typing import Any, Dict, List, Optional
from warnings import warn

from mip_cmor_tables import ChecksummedJSON


class CVCollection(object):
    """
    Object to provide access to generic MIP tables and corresponding CVs

    :param location: location of Tables and generic CVs
    :type location: str
    :param validate_checksum: if false do not validate checksums on loading
    :type validate_checksum: bool (optional)    
    """
    EXPECTED_FILES: List[str] = [
        'activity_id', 'DRS', 'experiment_id', 'further_info_url', 'license', 
        'mip_era', 'required_global_attributes', 'source_id', 'sub_experiment_id', 
        'tracking_id']

    def __init__(self, location: str, validate_checksums: bool = True) -> None:
        self.logger = logging.getLogger(__name__)
        self.location = location
        self.identify_mip_era(validate_checksums)
        self.cvs = {}
        self.identify_mip_era(validate_checksums)
        self._get_vocab_json_files(validate_checksums=validate_checksums)
    
    def identify_mip_era(self, validate_checksums: bool):
        mip_era_files = glob.glob(os.path.join(self.location, '*_mip_era.json'))
        if len(mip_era_files) != 1:
            raise RuntimeError('Expected 1 mip_era file. Found: {}'.format(mip_era_files))
        mip_era_json = ChecksummedJSON(mip_era_files[0], validate=validate_checksums)
        self.mip_era = mip_era_json['mip_era']

    def _get_vocab_json_files(self, validate_checksums: bool) -> None:

        for component in self.EXPECTED_FILES:
            filename = '{}_{}.json'.format(self.mip_era, component)
            file_location = os.path.join(self.location, filename)
            if not os.path.exists(file_location):
                self.logger.critical('file "{}" not found'.format(file_location))
            self.cvs[component] = ChecksummedJSON(file_location, validate=validate_checksums)
        
    def save(self) -> None:
        """
        Write ancilliary files and MIP tables to their designated files 
        """
        for cv_name, cv in self.cvs.items():
            print(cv_name)
            file_location = os.path.join(self.location, '{}_{}.json'.format(self.mip_era, cv_name))
            cv.write_json(file_location)
