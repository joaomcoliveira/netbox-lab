#!/usr/bin/env python

"""
Unit tests for helper functions
"""

import yaml
import nb_lab.helpers as h


def test_validate_nb_url():
    """
    Test validation of NetBox URL
    """
    assert h.validate_nb_url(h.NB_URL)


def test_validate_nb_token():
    """
    Test validation of NetBox API token
    """
    assert h.validate_nb_token(h.NB_TOKEN)


def test_validate_nb_custom_field():
    """
    Test validation of NetBox custom field to update
    """
    assert h.validate_nb_custom_field(h.NB_CUSTOM_FIELD)


def test_validate_nornir_defaults_filepath():
    """
    Test validation of Nornir defaults filepath
    """
    assert h.validate_nornir_defaults_filepath(h.NORNIR_DEFAULTS_FILEPATH)


def test_validate_nb_filter_params():
    """
    Test validation of NetBox inventory filter params JSON file
    """
    assert h.validate_nb_filter_params("inventory/filter_params.json")


# @pytest.fixture(scope="module")
def defaults():
    """
    Test defaults yaml file
    """
    with open("inventory/defaults.yaml", "r") as handle:
        dft = yaml.safe_load(handle)
    return dft


def test_validate_default_username():
    """
    Test validation of Nornir's inventory default username
    """
    dft = defaults()
    assert h.validate_default_username(dft)


def test_validate_default_password():
    """
    Test validation of Nornir's inventory default password
    """
    dft = defaults()
    assert h.validate_default_password(dft)
