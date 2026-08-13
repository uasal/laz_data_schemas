import typing
import os
import yaml
import jsonschema
from jsonschema import validate, ValidationError
from importlib.resources import files

class CoreSchemas:
    """
    This class contains the definitions for the core schema
    for the coronograph science camera, the
    LLOWFS, and the context camera. These are values that are common
    to all the instruments and are written to the Primary header of
    the output fits files. 

    In all cases, efforts have been made to follow the FITS standard
    (https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf).

    Units shall be consistent with AstroPy units.

    This schema does not allow additional fields: additionalProperties is False
    This schema requires some fields (for now): IMGTYPE

    Note:Validating a YAML-formatted JSON schema is a two-step process: 
    first, you parse the YAML into a Python dictionary, and then you 
    use a validation library to check your data against that dictionary.
    """

    RESOURCE_PACKAGE = 'laz_data_schemas.schemas'
    REFERENCE_FILE = 'core_schema.yaml'
    
    def get_sci_core_schema(self) -> dict[str, typing.Any]:
        """
        Defines the metadata (fits headers) associated with all data.

        Returns:
        -------
        core_dict : dictionary
          Schema converted to dictionary
        """
        try:
            # Get the path object for the reference file
            schema_path = files(self.RESOURCE_PACKAGE) / self.REFERENCE_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return {}, None
        
        
        # Convert the yaml information in a dictionary. Set up values and descriptions and default
        # values. 
        core_dict = {}
        main_properties = schema_yaml.get('properties', {})
        # Loop over top-level properties defined in the schema
        for key, values in main_properties.items():
            # Check if the property has a nested 'properties' dictionary
            if 'properties' in values:
                core_dict[key] = {}
                sub_properties = values['properties']

                # Extract 'value' and 'description' properties
                value_info = sub_properties.get('value', {})
                desc_info = sub_properties.get('description', {})

                # Extract default value, if it exists
                if 'default' in value_info:
                    core_dict[key]['value'] = value_info['default']
                elif 'type' in value_info:
                    # If no default, use the type to provide a placeholder
                    core_dict[key]['value'] = f"<{value_info['type']}>"
                else:
                    core_dict[key]['value'] = None
                
                # Extract description
                core_dict[key]['description'] = desc_info.get('default', '')


        return core_dict


    def validate_core_schema(self, data_dict):
        """
        Validate a dictionary against a schema 

        Parameters
        ----------
        data_dict : `dict`
        Dictionary containing information to be validated.

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
            # Get the path object for the reference file
            schema_path = files(self.RESOURCE_PACKAGE) / self.REFERENCE_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                schema = yaml.safe_load(file)

        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return {}, None

        try:
            jsonschema.validate(instance=data_dict, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print("Data is not valid against the Core Schema.")
            print("Validation Error:", err.message)
            return False
        except Exception as e:
            print("An unexpected error occurred during validation.")
            print("Error:", e)
            return False



