#!/usr/bin/env python
# -------------------------------------------------------------------
# Unit tests for helper functions
# -------------------------------------------------------------------

import os
from dotenv import load_dotenv
import nb_lab.helpers as h

# Load environmental variables from .env file
load_dotenv()

# Define constants as static values that won't change
NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")
NB_CUSTOM_FIELD = os.getenv("NB_CUSTOM_FIELD")

# Test validation of NetBox URL
def test_nb_url():
    assert h.validate_nb_url(NB_URL)

# Test validation of NetBox API Token
def test_nb_token():
    assert h.validate_nb_token(NB_TOKEN)

# Test validation of NetBox custom field to update
def test_nb_custom_field():
    assert h.validate_nb_custom_field(NB_CUSTOM_FIELD)
