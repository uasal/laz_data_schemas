#!/bin/python
import os
import yaml
import typing
import jsonschema
from jsonschema import validate, RefResolver, ValidationError

def validate_schema_yaml(configuration_file, _schema_template) -> bool:
    """
    Validate an existing configuration files against a schema using a yaml file. 
    The configuration file is a yaml file. 

    Parameters
    ----------

        configuration_file : `str`
            Configuration filename to be validated.

        schema_template : `dict`
            Configuration schema to be validated against.

    Raises
    ------

        ValidationError:
            If proposed validation file is not compatible with the schema.

    Returns
    -------

        output : `boolean`
            True if successful.
        config_data: : `dict` 
            Loaded yaml file in to schemma


    """

    status = False
    config_data = None
    # Read in the yaml file
    with open(configuration_file) as f:
        config_data = yaml.load(f, Loader=yaml.SafeLoader)
    print(f"Config data is: {config_data}")
    
    try:
        jsonschema.validate(config_data, _schema_template)
    except jsonschema.exceptions.ValidationError:
        print("Schema not valid.\n")
        raise

    status = True
    return status, config_data


def validate_schema_dict(data_dict: dict, schema_template: dict) -> bool:
    """
    Validate a dictionary against a schema.

    Parameters
    ----------
        data_dict : `dict`
            Dictionary containing information to be validated.

        schema_template : `dict`
            Configuration schema to be validated against.
    Raises
    ------
        ValidationError:
            If proposed validation file is not compatible with the schema.
    Returns
    -------
        output : `boolean`
            True if successful.

    """

    try:
        # Corrected call with the schema keyword argument
        validate(instance=data_dict, schema=schema_template)
        print("Data configuration is valid.")
        return True # Return True immediately upon success
    except jsonschema.exceptions.ValidationError as e:
        print(f"Configuration is invalid: {e.message}")
        raise # Re-raise the exception to stop execution





