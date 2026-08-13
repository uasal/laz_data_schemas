import typing
import yaml
import os
import jsonschema
from jsonschema import validate, RefResolver, ValidationError
from importlib.resources import files

class SatSchemas:
    """
    This class contains the definitions for the image interfaces,
    for the coronograph science camera

    In all cases, efforts have been made to follow the FITS standard
    (https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf).

    Units shall be consistent with AstroPy units.

    """

    RESOURCE_PACKAGE = 'laz_data_schemas.schemas'
    REFERENCE_FILE = 'reference_schema.yaml'
    IMAGE_FILE = 'sat_image_schema.yaml'
    
    def get_sat_meta_schema(self) -> dict[str, typing.Any]:
        """
        Defines the metadata (fits headers) associated with all data.


        Returns:
        -------
        meta_dict : dictionary
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
        meta_dict = {}
        main_properties = schema_yaml.get('properties', {})
        # Loop over top-level properties defined in the schema
        for key, values in main_properties.items():
            # Check if the property has a nested 'properties' dictionary
            if 'properties' in values:
                meta_dict[key] = {}
                sub_properties = values['properties']

                # Extract 'value' and 'description' properties
                value_info = sub_properties.get('value', {})
                desc_info = sub_properties.get('description', {})

                # Extract default value, if it exists
                if 'default' in value_info:
                    meta_dict[key]['value'] = value_info['default']
                elif 'type' in value_info:
                    # If no default, use the type to provide a placeholder
                    meta_dict[key]['value'] = f"<{value_info['type']}>"
                else:
                    meta_dict[key]['value'] = None
                
                # Extract description
                meta_dict[key]['description'] = desc_info.get('default', '')

        return meta_dict


    def validate_meta_schema(self, data_dict):
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
            print("Data is not valid against the Sat meta Schema.")
            print("Validation Error:", err.message)
            return False
        except Exception as e:
            print("An unexpected error occurred during validation.")
            print("Error:", e)
            return False


    
    def get_sat_image_schema(self) -> dict[str, typing.Any]:
        """
        Definites the metadata (fits headers) associated with sat image
        for the esc instrument

        Return:
        -------
        image_dict : dictionary
          schema converted into a dictionary

        """

        try:
            # Get the path object for the image file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE_FILE}' was not found.")
            return {}, None
        
        
        image_dict = {}
        sat_schema = None
        nonlin_schema = None
        
        # Loop over properties defined in the schema to extract default values
        # set any defaults defined in schema.
        # loop over the level1a schema
        main_properties = schema_yaml.get('properties', {})

        for key,values in main_properties.items():
            if key == 'sat':
                sat_schema = values['items']
            elif key == 'nonlin':
                nonlin_schema = values['items']
            else:
                # Check if the 'properties' key exists and contains a 'value' key
                if 'properties' in values and 'value' in values['properties']:
                    # Now the print statement will be reached
                    #print('Value', values['properties']['value']) 
                
                    # Build model dictionary
                    item = {}
                    item['value'] = values['properties'].get('value')
                    item['description'] = values.get('description', '')
                    image_dict[key] = item        

        image_dict['sat'] = sat_schema
        image_dict['nonlin'] = nonlin_schema
        return image_dict

    
    def validate_sat_image_schema(self, data_dict):
        """
        Validate a dictionary against a schema, including external references. 

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
                meta_schema = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return {}, None

        try:
            # Get the path object for theimage file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                main_schema = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE_FILE}' was not found.")
            return {}, None

        valid = self.validate_meta_schema(data_dict['meta'])
        if valid is False:
            print('Saturation meta data did not validate')
            return False
        
        # The resolver maps schema URIs (like 'sat_schema.yaml') to their content
        resolver = RefResolver(
            base_uri='sat_image_schema.yaml',  # The base URI of the main schema
            referrer=main_schema,
            store={'reference_schema.yaml': meta_schema}  # The store holds the content of the external schema
        )
        try:
            # Use the resolver during validation
            validate(instance=data_dict, schema=main_schema, resolver=resolver)
            #print(" Image1 is valid!")
            return True 
        except ValidationError as e:
            print(f"Validation of Image1a failed. Error: {e.message} ")
            return False


    def get_sat_schema(self) -> dict[str, typing.Any]:        
        """
        """
        meta_dict = self.get_sat_meta_schema()
        
        image_dict = self.get_sat_image_schema()

        sat = {}
        sat['meta'] = meta_dict
        sat['image'] = image_dict

        
        return sat
