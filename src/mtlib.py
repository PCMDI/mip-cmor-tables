#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 16:25:51 2022

This MIP Table library (mtlib) collates a number of functions which will be
useful in mip table management

@author: @durack1, @matthew-mizielinski
"""

# %% imports
import json
import hashlib
from copy import deepcopy


def _checksum(obj):
    obj_str = json.dumps(obj, sort_keys=True)
    checksum_hex = hashlib.md5(obj_str.encode('utf8')).hexdigest()
    return 'md5: {}'.format(checksum_hex)


def branded_variable_name(variable):
    # Order of terms after variable label
    functions = [interval_label, realm_label,
                 temporal_label, vertical_label, horizontal_label]
    return '{}_{}'.format(variable['out_name'], '-'.join([f(variable) for f in functions]))


def calculate_checksum(dictionary, overwrite=True, checksum_location='Header'):
    """
    Calculate the checksum for dictionary and add it to the Header

    Parameters
    ----------
    dictionary: dict
        The dictionary to set the checksum for.
    overwrite: bool
        Overwrite the existing checksum (default True).
    checksum_location: str
        sub-dictionary to look for in /add the checksum to.

    Raises
    ------
    RuntimeError
        If the ``checksum`` key already exists and ``overwrite`` is
        False.
    """
    if 'checksum' in dictionary[checksum_location]:
        if not overwrite:
            raise RuntimeError('Checksum already exists.')
        del dictionary[checksum_location]['checksum']
    checksum = _checksum(dictionary)
    dictionary[checksum_location]['checksum'] = checksum


def horizontal_label(variable):
    dimensions = set(variable['dimensions'].split(' '))
    latlon = {'latitude', 'longitude'}
    ant = {'xant', 'yant'}
    gre = {'xgre', 'ygre'}
    latbas = {'latitude', 'basin'}

    if (latlon.intersection(dimensions) == latlon or
        ant.intersection(dimensions) == ant or
            gre.intersection(dimensions) == gre):
        # simple lat lon
        result = 'hxy'
    elif ('latitude' in dimensions and
          'longitude' not in dimensions and
          'basin' not in dimensions):
        # zonal means, but not by basin
        result = 'hy'
    elif not {'latitude', 'yant', 'ygre', 'gridLatitude', 'site', 'oline', 'oline'}.intersection(dimensions):
        # spatial means means
        result = 'hm'
    elif latbas.intersection(dimensions) == latbas:
        # basin means
        result = 'hys'
    elif 'site' in dimensions:
        # CF sites
        result = 'hxys'
    elif 'oline' in dimensions or 'siline' in dimensions:
        # transports
        result = 'ht'
    else:
        raise KeyError('Could not determine label for "{}"'.format(
            variable['dimensions']))

    return result


INTERVAL_LOOKUP = {
    'subhrPt': 'subhr',
    '1hr': '1hr',
    '1hrCM': '1hrCM',
    '1hrPt': '1hr',
    '3hr': '3hr',
    '3hrPt': '3hr',
    '6hr': '6hr',
    '6hrPt': '6hr',
    'day': 'day',
    'mon': 'mon',
    'monC': 'mon',
    'monPt': 'mon',
    'yr': 'yr',
    'yrPt': 'yr',
    'dec': 'dec',
    'fx': 'fx',
}


def interval_label(variable):
    return INTERVAL_LOOKUP[variable['frequency']]


REALM_LOOKUP = {
    'atmos': 'ap',
    'atmosChem': 'ac',
    'aerosol': 'ae',
    'land': 'ld',
    'landIce': 'li',
    'ocean': 'op',
    'ocnBgchem': 'oc',
    'seaIce': 'si',
}


def realm_label(variable):
    # not taking into account secondary realms, will have errors
    return REALM_LOOKUP[variable['modeling_realm'].split(' ')[0]]


TIME_LOOKUP = {
    'time': 'tav',
    'time1': 'tpt',
    'time2': 'tcla',
    'time3': 'tcld',
}


def temporal_label(variable):
    # default of "none" to cover fixed field case
    label = 'none'
    for dim in variable['dimensions'].split(' '):
        if dim in TIME_LOOKUP:
            label = TIME_LOOKUP[dim]
            break
    return label


def validate_checksum(dictionary, checksum_location='Header'):
    """
    Validate the checksum in the ``dictionary``.

    Parameters
    ----------
    dictionary: dict
        The dictionary containing the ``checksum`` to validate.
    checksum_location: str
        sub-dictionary to look for in /add the checksum to.

    Raises
    ------
    KeyError
        If the ``checksum`` key does not exist.
    RuntimeError
        If the ``checksum`` value is invalid.
    """
    if 'checksum' not in dictionary[checksum_location]:
        raise KeyError('No checksum to validate')
    dictionary_copy = deepcopy(dictionary)
    del dictionary_copy[checksum_location]['checksum']
    checksum = _checksum(dictionary_copy)
    if dictionary[checksum_location]['checksum'] != checksum:
        msg = ('Expected checksum   "{}"\n'
               'Calculated checksum "{}"').format(dictionary[checksum_location]['checksum'],
                                                  checksum)
        raise RuntimeError(msg)


VERTICAL_LOOKUP = {
    'sdepth': 'l',
    'olevel': 'l',
    'alevel': 'l',
    'alevhalf': 'l',
    'olevhalf': 'l',
    'rho': 'rhon',
    'height2m': 'h02',
    'height10m': 'h010',
    'height100m': 'h0100',
    'sdepth1': 'z01s',
    'sdepth10': 'z010',
    'depth0m': 'z00',
    'depth100m': 'z0100',
    'depth300m': 'z0300',
    'depth700m': 'z0700',
    'depth2000m': 'z02000',
    'olayer100m': 'z0100',
    'p10': 'p010',
    'p100': 'p0100',
    'p220': 'p0220',
    'p500': 'p0500',
    'p560': 'p0560',
    'pl700': 'p0700',
    'p840': 'p0840',
    'p850': 'p0850',
    'p1000': 'p01000',
    'alt16': 'z16',
    'alt40': 'z40',
    'plev3': 'p3',
    'plev4': 'p4',
    'plev8': 'p8',
    'plev7c': 'p7c',
    'plev7h': 'p7h',
    'plev19': 'p19',
    'plev27': 'p27',
    'plev39': 'p39',
}


def vertical_label(variable):
    for dim in variable['dimensions'].split(' '):
        if dim in VERTICAL_LOOKUP:
            return VERTICAL_LOOKUP[dim]
    # default:
    return 'z0'
