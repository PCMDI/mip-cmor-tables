# (C) British Crown Copyright 2022, Met Office
# CC0-1.0 License

from copy import deepcopy
import json
import os
import unittest
import warnings

from collection import ChecksummedJSON, MIPVariable, MIPTableCollection


class TestChecksummedJSON(unittest.TestCase):

    def setUp(self) -> None:
        # Calculated checksum
        self.checksum = 'md5: e9ec9d51de114c7c9fcb1ee72e226e71'
        self.data = {
            ChecksummedJSON.CHECKSUM_LOCATION: {
                ChecksummedJSON.CHECKSUM_KEY: self.checksum,
                'other': 'stuff'
            },
            'variables': {
                'tas': {
                    'this': 'thing'
                    },
                'pr': {
                    'this': 'thing'
                    },
            }
        }
    
    def test_simple(self) -> None:
        data_csj = ChecksummedJSON(self.data)
        self.assertDictEqual(data_csj['variables'], self.data['variables'])
        self.assertDictEqual(data_csj['Header'], self.data['Header'])

    def test_not_usable_data(self) -> None:
        self.assertRaises(RuntimeError, ChecksummedJSON, 1)
        self.assertRaises(RuntimeError, ChecksummedJSON, {1, 2, 3})

    def test_validation_fail(self) -> None:
        data = deepcopy(self.data)
        data['Header']['checksum'] = 'garbage'
        self.assertRaises(RuntimeError, ChecksummedJSON, data)

    def test_updating_checksum(self) -> None:
        data = deepcopy(self.data)
        data['Header']['checksum'] = 'garbage'
        # ignore warning that validation is not being done
        with warnings.catch_warnings(): 
            warnings.simplefilter('ignore')
            data_csj = ChecksummedJSON(data, validate=False)
        data_csj.update_checksum()
        self.assertEqual(data_csj.checksum, self.checksum)


class TestMIPVariable(unittest.TestCase):
    def setUp(self) -> None:
        self.test_tables_dir = os.path.join(os.path.dirname(__file__), 'TestTables')
        self.mip_table_collection = MIPTableCollection(self.test_tables_dir)

    def test_update_bad(self):
        mip_variable = MIPVariable(parent=self.mip_table_collection)
        bad_updates = {
            'dimensions': {'this': 'that'}, 
            'frequency': '1min',
            'modeling_realm': ['space'],
            'table_id': 'notable'
        }
        for update in bad_updates.items():
            # check via from_dict method
            self.assertRaises(AssertionError, mip_variable.from_dict, dict([update]))
        
            # check via attribute change and check method
            setattr(mip_variable, *update)
            self.assertRaises(AssertionError, mip_variable.check)
            setattr(mip_variable, update[0], None)

    def test_update_good(self):
        mip_variable = MIPVariable(parent=self.mip_table_collection)
    
        good_updates = {
            'dimensions': ['latitude', 'longitude', 'time'],
            'frequency': '6hr',
            'modeling_realm': ['atmos', 'seaIce'],
            'table_id': 'Testmon'
        }
        for update in good_updates.items():
            mip_variable.from_dict(dict([update]))
        
    def test_loaded_correctly(self):
        # load variable in testmon mip table
        variable = self.mip_table_collection.get_variable('Testmon', 'flashrate')
        # Read JSON from table and extract json information
        with open(os.path.join(self.test_tables_dir, 'Testmon.json')) as fh:
            testmon_raw = json.load(fh)
        json_raw_variable = testmon_raw['variable_entry']['flashrate']
        # Check each attribute against JSON
        for key, value in json_raw_variable.items():
            self.assertEqual(getattr(variable, key), value)

    def test_to_json(self):
        # load variable in testmon mip table
        variable = self.mip_table_collection.get_variable('Testmon', 'flashrate')
        # Read JSON from table and extract json information
        with open(os.path.join(self.test_tables_dir, 'Testmon.json')) as fh:
            testmon_raw = json.load(fh)
        json_raw_variable = testmon_raw['variable_entry']['flashrate']
        # compare to output of to_json method
        json_mip_variable = variable.to_json()
        self.assertDictEqual(json_raw_variable, json_mip_variable)


class TestMIPTableCollection(unittest.TestCase):
    def setUp(self) -> None:
        self.test_tables_dir = os.path.join(os.path.dirname(__file__), 'TestTables')
        self.mip_table_collection = MIPTableCollection(self.test_tables_dir)

    def test_tables_list(self):
        
        with open(os.path.join(self.test_tables_dir, 'generic_CV.json')) as fh:
            raw_generic_cv = json.load(fh)
        
        self.assertListEqual(raw_generic_cv['table_id'], list(self.mip_table_collection.tables.keys()))
        
if __name__ == '__main__':
    unittest.main()