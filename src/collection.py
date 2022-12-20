# (C) British Crown Copyright 2022, Met Office
# CC0-1.0 License

from copy import deepcopy
from dataclasses import asdict, dataclass, field
import hashlib
import json
import logging
import os
from typing import Any, Dict, List, Optional
from warnings import warn
from _collections_abc import dict_keys, dict_values

# Following files to be ignored. Primarily for development
FILES_TO_IGNORE = ['CMIP6Plus_CV.json']  


class MIPTableCollection(object):
    """
    Object to provide access to generic MIP tables and corresponding CVs

    :param location: location of Tables and generic CVs
    :type location: str
    :param validate_checksum: if false do not validate checksums on loading
    :type validate_checksum: bool (optional)    
    """
    CV_FILENAME: str = 'generic_CV.json'
    COORDINATE_FILENAME: str = 'coordinate.json'
    FORMULATERMS_FILENAME: str = 'formula_terms.json'
    GRIDS_FILENAME: str = 'grids.json'
    ANCIL_FILES: List[str] = [CV_FILENAME, 'coordinate.json', 'formula_terms.json', 'grids.json']

    def __init__(self, location: str, validate_checksums: bool = True) -> None:
        self.logger = logging.getLogger(__name__)
        self.location = location
        self.tables = {}
        self._get_mip_table_json_files(location)
        self._load_ancil(validate_checksums)
        self._load_tables(validate_checksums)

    def _get_mip_table_json_files(self, location: str) -> None:
        json_files = []
        for filename in os.listdir(location):
            if not filename.endswith('.json') or filename in FILES_TO_IGNORE:
                self.logger.debug('Ignoring file "{}"'.format(filename))
            else:
                json_files.append(filename)

        for ancil in self.ANCIL_FILES:
            if ancil not in json_files:
                self.logger.critical('Ancil file "{}" not found'.format(ancil))
            else:
                json_files.remove(ancil)
        self._mip_table_json_files = json_files
    
    def _load_json(self, filename: str, validate_checksums: bool) -> None:
        file_location = os.path.join(self.location, filename)
        return ChecksummedJSON(file_location, validate=validate_checksums)

    def _load_ancil(self, validate_checksums: bool) -> None:
        self.generic_cv = self._load_json(self.CV_FILENAME, validate_checksums=validate_checksums)
        self.coordinate = self._load_json(self.COORDINATE_FILENAME, validate_checksums=validate_checksums)
        self.formula_terms = self._load_json(self.FORMULATERMS_FILENAME, validate_checksums=validate_checksums)
        self.grids = self._load_json(self.GRIDS_FILENAME, validate_checksums=validate_checksums)
        
    def _load_tables(self, validate_checksums: bool) -> None:
        for table in self._mip_table_json_files:
            try:    
                table_dict = self._load_json(table, validate_checksums=validate_checksums)
            except KeyError as err:
                raise RuntimeError('Failed to load json from file "{}": "{}"'.format(table, err))
            table_id = table_dict['Header']['table_id']
            if table_id != table.replace('.json', ''):
                raise RuntimeError('"table_id" field in {} inconsistent with file name'.format(table))
            self.tables[table_id] = table_dict

    def get_variable(self, mip_table: str, variable_name: str):
        """
        Return a MIPVariable object corresponding to the table and variable name given
        
        :param mip_table: MIP table name
        :type mip_table: str
        :param variable_name: Variable name
        :type variable_name: str
        :returns MIPVariable:

        """
        mip_table_data = self.tables[mip_table]['variable_entry'][variable_name]
        return MIPVariable(parent=self, table_id=mip_table, name=variable_name, **mip_table_data)
    
    def update_variable(self, mip_variable) -> None:
        """
        Update the variable definition held in the collection with the variable supplied
        """
        pass


    def save(self) -> None:
        """
        Write ancilliary files and MIP tables to their designated files 
        """
        for table in self.tables.values():
            if not os.path.exists(table.filename):
                warn('Table file "{}" does not exist, writing as new file'.format(table.filename))
        self.generic_cv.write_json(self.generic_cv.filename)
        self.coordinate.write_json(self.coordinate.filename)
        self.formula_terms.write_json(self.formula_terms.filename)
        self.grids.write_json(self.grids.filename)

        for table in self.tables.values():
            table.write_json(table.filename)


class ChecksummedJSON(object):

    CHECKSUM_KEY: str = 'checksum'
    CHECKSUM_LOCATION: str = 'Header'

    def __init__(self, data_source: str or Dict or List, validate: bool = True):
        """
        Class to load/hold/save a JSON dictionary with a checksum. The checksum is
        stored within a "Header" dictionary (CHECKSUM_LOCATION) under the key 
        "checksum" (CHECKSUM_KEY). The checksum is computed by
           (a) removing the checksum entry itself and 
           (b) passing a json dump of the data to the hashlib.md5 function. 
        This checksum is then compared to the stored value by the validate method

        :param data_source: file name to be read or dictionary/list containing equivalent information
        :type data_source: str or dict or list
        :param validate: If true validate the data after loading and raise a RuntimeError if this fails
        :type validate: bool

        """
        self.filename = None
        if isinstance(data_source, str):
            self.filename = data_source
            self.read_json(data_source)
        elif isinstance(data_source, (dict, list)):
            self.data = data_source
        else:
            raise RuntimeError('Could not work out what to do with data of type "{}"'.format(type(data_source)))
        if validate:
            self.validate_checksum()
        else:
            if isinstance(data_source, str):
                warn('Header checksum not validated when loading data from {}'.format(data_source))
            else:
                warn('Header checksum not validated when reading supplied data')

    def read_json(self, filename: str) -> None:
        """
        Read JSON from specified file
        """
        with open(filename) as file_handle:
            self.data = json.load(file_handle)
    
    @property
    def checksum(self):
        """
        Stored checksum.
        """
        return self.data[self.CHECKSUM_LOCATION][self.CHECKSUM_KEY]

    def update(self, data):
        self.data.update(data)

    def validate_checksum(self) -> None:
        """
        Validate the recorded checksum against the rest of the data. 
        Raises a RuntimeError on failure.
        """
        
        if self.checksum is None:
            raise KeyError('No checksum to validate')
        
        # take copy of dictionary
        dictionary_copy = deepcopy(self.data)
        # remove checksum
        del dictionary_copy[self.CHECKSUM_LOCATION][self.CHECKSUM_KEY]
        # calculate checksum
        checksum = checksum_object(dictionary_copy)

        if self.checksum != checksum:
            msg = ('Expected checksum   "{}"\n'
                   'Calculated checksum "{}"').format(self.checksum, checksum)
            raise RuntimeError(msg)

    def update_checksum(self) -> None:
        """
        Recompute MD5 checksum and update.
        """
        # take copy of dictionary
        dictionary_copy = deepcopy(self.data)
        # remove checksum
        if self.CHECKSUM_LOCATION in dictionary_copy:
            try:
                del dictionary_copy[self.CHECKSUM_LOCATION][self.CHECKSUM_KEY]
            except KeyError:
                pass
        else:
            dictionary_copy[self.CHECKSUM_LOCATION] = {}
        # calculate checksum
        checksum = checksum_object(dictionary_copy)
        self.data[self.CHECKSUM_LOCATION][self.CHECKSUM_KEY] = checksum

    def write_json(self, filename: str, sort_keys: bool = True, indent: int = 2, **kwargs):
        """
        Write data to file "filename" other keywords passed to json.dump.
        Note: no attempt to address encoding is made here
        """
        self.update_checksum()
        with open(filename, 'w') as file_handle:
            json.dump(self.data, file_handle, sort_keys=sort_keys, indent=indent, **kwargs)

    def __getitem__(self, key: Any) -> Any:
        return self.data[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.data[key] = value

    def keys(self) -> dict_keys:
        return self.data.keys()

    def values(self) -> dict_values:
        return self.data.values()
        


@dataclass
class MIPVariable:

    OUTPUT_FIELDS = [
        'branded_variable_name',
        'cell_measures',
        'cell_methods',
        'comment',
        'dimensions',
        'frequency',
        'long_name',
        'modeling_realm',
        'out_name',
        'positive',
        'provenance',
        'standard_name',
        'type',
        'units',
        'validation'
    ]
    FLAGS = ['flag_meanings', 'flag_values']

    parent: Optional[MIPTableCollection] = None
    branded_variable_name: Optional[str] = None
    cell_measures: Optional[str] = None
    cell_methods: Optional[str] = None
    comment: Optional[str] = None
    dimensions: List[str] = field(default_factory=list)
    frequency: Optional[str] = None
    long_name: Optional[str] = None
    modeling_realm: Optional[str] = None
    name: Optional[str] = None
    out_name: Optional[str] = None
    positive: Optional[str] = None
    provenance: dict= field(default_factory=dict)
    standard_name: Optional[str] = None
    table_id: Optional[str] = None
    type: Optional[str] = None
    units: Optional[str] = None
    validation: dict = field(default_factory=dict)

    flag_meanings: Optional[str] = None
    flag_values: Optional[str] = None

    def __post_init__(self):
        self.check()
    
    def check(self):
        fields_to_check = {}
        for key, value in asdict(self).items():
            if value is not None and value:
                fields_to_check[key] = value

        self.check_against_miptablecollection(fields_to_check)

    def from_dict(self, data):
        if self.parent is None:
            raise RuntimeError('parent must be set to a MIPTableCollection before continuing')
        self.check_against_miptablecollection(data)
        for k, v in data.items():
            self.__setattr__(k, v)

    @staticmethod
    def _assert(test: bool, message: str) -> None:
        assert test, message

    def check_against_miptablecollection(self, data: dict) -> None:
        """
        Check a dictionary of fields to update the MIPVariable with 
        """
        # branded variable name check
        # cell_measures check
        # cell_methods_check
        # dimensions check
        if 'dimensions' in data:
            self._assert(
                isinstance(data['dimensions'], list), 
                'dimensions must be a list'
            )
            #for i in data['dimensions']:
            #    self._assert(
            #        i in self.parent.coordinate['axis_entry'],
            #        'Dimensions "{}" not found in the coordinates.json file'.format(i)
            #    )
        #frequency
        if 'frequency' in data:
            self._assert(
                isinstance(data['frequency'], str),
                'frequency must be a string'
            )
            self._assert(
                data['frequency'] in self.parent.generic_cv['frequency'],
                'frequency must be as specified in the frequency CV'
            )
        # long_name
        # modeling_realm
        if 'modeling_realm' in data:
            self._assert(
                all([i in self.parent.generic_cv['realm'] for i in data['modeling_realm']]),
                'All modeling_realm entries must be specified in the realm CV'
            )
        # name & out_name
        if 'out_name' in data and 'name' in data:
            self._assert(
                data['out_name'] == data['name'],
                'Avoid out_name != name'
            )
        # table id
        if 'table_id' in data:
            self._assert(
                data['table_id'] in self.parent.generic_cv['table_id'],
                'table_id must be included in the table_id CV'
            )
        # type
        # units  - udunits2 check?
        # validation 
        validation_keys = {"ok_max_mean_abs", "ok_min_mean_abs", "valid_max", "valid_min"}
        if 'validation' in data:
            self._assert(
                set(data['validation'].keys()) == validation_keys,
                'All validation keys must be specified if any are included'
            )

    def to_json(self) -> Dict:
        self.check()
        all_data = asdict(self)
        result = {i:all_data[i] for i in self.OUTPUT_FIELDS}
        if self.flag_values:
            result.update({i:all_data[i] for i in self.FLAGS})
        return result

        
class VariableJSONEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, MIPVariable):
            return object.to_json()
        else:
            return object


def checksum_object(obj):
    """
    Convert an object to a utf8 string (json representation), 
    MD5 checksum it and return the result as a string
    """
    obj_str = json.dumps(obj, sort_keys=True)
    checksum_hex = hashlib.md5(obj_str.encode('utf8')).hexdigest()
    return 'md5: {}'.format(checksum_hex)
        
