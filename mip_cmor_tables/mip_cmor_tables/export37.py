# (C) British Crown Copyright 2022, Met Office
# CC0-1.0 License
from collections import OrderedDict
from copy import copy
import json
import os

from mip_cmor_tables.controlled_vocab import CVCollection
from mip_cmor_tables import MIPTableCollection, ChecksummedJSON

CV_ORDER = [
    'required_global_attributes', 'version_metadata', 'license', 'activity_id', 
    'institution_id', 'source_id', 'source_type', 'frequency', 'grid_label', 
    'nominal_resolution', 'realm', 'table_id', 'DRS', 'mip_era', 'sub_experiment_id', 
    'experiment_id', 'product', 'tracking_id', 'further_info_url', 'realization_index', 
    'variant_label', 'data_specs_version', 'Conventions', 'forcing_index', 
    'initialization_index', 'physics_index']

def generate_37_tables(mip_table_location, cv_location, destination):
    table_collection = MIPTableCollection(mip_table_location)
    cv_collection = CVCollection(cv_location)

    mip_era = cv_collection.mip_era

    new_cv = OrderedDict([('CV',{})])
    checksums = {}
    for field in CV_ORDER:
        print(field)
        if field == 'version_metadata':
             new_cv['CV']['version_metadata'] = {'CV_collection_version': '0.0.1'}
             continue
        elif field == 'source_id':
            new_cv['CV']['source_id'] = {}
            for source_id, source_id_data in cv_collection.cvs[field].data[field].items():
                source_id_data['source'] = '{} ({}): \n{}'.format(
                    source_id,
                    source_id_data['release_year'],
                    '\n'.join(['{}:{}'.format(i,j['description']) for i, j in source_id_data['model_component'].items()])
                )
                for i in ['label', 'label_extended', 'model_component', 'release_year']:
                    del source_id_data[i]
                
                new_cv['CV']['source_id'][source_id] = source_id_data
        elif field == 'mip_era':
            new_cv['CV']['mip_era'] = [mip_era]
        elif field == 'experiment_id':
            new_cv['CV']['experiment_id'] = {}
            for expt_id, expt_data in cv_collection.cvs[field].data[field].items():
                for i in ['description', 'end_year', 'min_number_yrs_per_sim', 'start_year', 'tier']:
                    if i in expt_data:
                        del expt_data[i]
                new_cv['CV']['experiment_id'][expt_id] = expt_data
        else:
            try:
                new_cv['CV'][field] = table_collection.generic_cv[field]
            except KeyError:
                try:
                    new_cv['CV'][field] = cv_collection.cvs[field].data[field]
                    checksums[field] = cv_collection.cvs[field].checksum
                    #del new_cv['CV'][field]['Header']
                except KeyError:
                    raise RuntimeError('Key "{}" not found'.format(field))

    checksums['generic_cv'] = table_collection.generic_cv.checksum    
    #new_cv['Header']['component_checksums'] = checksums
    
    filename = os.path.join(destination, '{}_CV.json'.format(mip_era))
    with open(filename, 'w') as file_handle:
        json.dump(new_cv, file_handle, indent=4, separators=(',', ':'))

    #new_cv.write_json(os.path.join(destination, '{}_CV.json'.format(mip_era)), sort_keys=False)

    for i in table_collection.ANCIL_FILES:
        if i == 'generic_CV.json':
            continue
        filename = os.path.join(destination, '{}_{}'.format(mip_era, i))
        # slightly ugly, but functional:
        data = getattr(table_collection, i.replace('.json', '')).data
        del data['Header']
        with open(filename, 'w') as file_handle:
            json.dump(data, file_handle, sort_keys=True, indent=4)

    
    for table_name, table_dict in table_collection.tables.items():
        output_filename = os.path.join(destination, '{}_{}.json'.format(mip_era, table_name))
        table_dict['Header']['table_id'] = 'Table {}'.format(table_dict['Header']['table_id'])
        table_dict['Header']['mip_era'] = mip_era
        table_dict['Header']['cmor_version'] = '3.7.0'
        for variable in table_dict['variable_entry']:
            for key in ['branded_variable_name', 'provenance']:
                del table_dict['variable_entry'][variable][key]
            table_dict['variable_entry'][variable].update(table_dict['variable_entry'][variable]['validation'])
            del table_dict['variable_entry'][variable]['validation']
            old_style_dimensions = ' '.join(table_dict['variable_entry'][variable]['dimensions'])
            table_dict['variable_entry'][variable]['dimensions'] = old_style_dimensions
            table_dict['variable_entry'][variable]['modeling_realm'] = ' '.join(table_dict['variable_entry'][variable]['modeling_realm'])
        
        table_dict.write_json(output_filename)
        table_data = table_dict.data
        del table_data['Header']['checksum']
        with open(output_filename, 'w') as file_handle:
            json.dump(table_data, file_handle, sort_keys=True, indent=2)




if __name__ == '__main__':
    generate_37_tables('../Tables', '../../CMIP6Plus_CVs', '../out')

    
