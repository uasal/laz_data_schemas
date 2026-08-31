import typing
import yaml
import os
from jsonschema import validate, RefResolver, ValidationError
from importlib.resources import files
from laz_data_schemas.core_schema import CoreSchemas
import numpy as np

class EscImageSchemas:
    """
    This class contains the definitions for the image interfaces,
    for the coronograph science camera

    In all cases, efforts have been made to follow the FITS standard
    (https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf).

    Units shall be consistent with AstroPy units.
    """

    RESOURCE_PACKAGE = 'laz_data_schemas.schemas'
    REFERENCE_FILE = 'core_schema.yaml'
    IMAGE0_FILE = 'esc_image0_schema.yaml'
    IMAGE1_FILE = 'esc_image1_schema.yaml'
    IMAGE2_FILE = 'esc_image2_schema.yaml'
    IMAGE3_FILE = 'esc_image3_schema.yaml'    


    def get_sci_level0_schema(self) -> dict[str, typing.Any]:
        """
        Defines the dictionary structure and default values associated 
        with each Level 0 image schema.
        
        Returns
        -------
        image_dict : dict
        Schema converted into a template dictionary structure.
        """
        try:
            # Get path object for Level 0 schema file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE1A_FILE
        
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE1A_FILE}' was not found.")
            return {}

        image_dict = {}
        data_schema = None

        # Extract schema properties and set up template default items
        main_properties = schema_yaml.get('properties', {})

        for key, values in main_properties.items():
            if key == 'data':
                data_schema = values.get('items')
            else:
                if 'properties' in values and 'value' in values['properties']:
                    item = {
                        'value': values['properties'].get('value'),
                        'description': values.get('description', '')
                    }
                    image_dict[key] = item        

        image_dict['data'] = data_schema
    
        return image_dict
    

    def get_sci_level1_schema(self) -> dict[str, typing.Any]:
        """
        Defines the dictionary structure and default values associated 
        with each Level 1 image schema.
        
        Returns
        -------
        image_dict : dict
        Schema converted into a template dictionary structure.
        """
        try:
            # Get path object for Level 1 schema file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE1B_FILE
        
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE1B_FILE}' was not found.")
            return {}

        image_dict = {}
        data_schema = None
        error_schema = None
        dq_schema = None

        # Extract schema properties and set up template default items
        main_properties = schema_yaml.get('properties', {})

        for key, values in main_properties.items():
            if key == 'data':
                data_schema = values.get('items')
            elif key == 'error':
                error_schema = values.get('items')
            elif key == 'dq':
                dq_schema = values.get('items')
            else:
                if 'properties' in values and 'value' in values['properties']:
                    item = {
                        'value': values['properties'].get('value'),
                        'description': values.get('description', '')
                    }
                    image_dict[key] = item        

        image_dict['data'] = data_schema
        image_dict['error'] = error_schema
        image_dict['dq'] = dq_schema
    
        return image_dict


    def get_sci_level2_schema(self) -> dict[str, typing.Any]:
        """
        Defines the dictionary structure and default values associated 
        with each Level 1 image schema.
        
        Returns
        -------
        image_dict : dict
        Schema converted into a template dictionary structure.
        """
        try:
            # Get path object for Level 1 schema file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE2_FILE
        
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE1B_FILE}' was not found.")
            return {}

        image_dict = {}
        data_schema = None
        error_schema = None
        dq_schema = None

        # Extract schema properties and set up template default items
        main_properties = schema_yaml.get('properties', {})

        for key, values in main_properties.items():
            if key == 'data':
                data_schema = values.get('items')
            elif key == 'error':
                error_schema = values.get('items')
            elif key == 'dq':
                dq_schema = values.get('items')
            else:
                if 'properties' in values and 'value' in values['properties']:
                    item = {
                        'value': values['properties'].get('value'),
                        'description': values.get('description', '')
                    }
                    image_dict[key] = item        

        image_dict['data'] = data_schema
        image_dict['error'] = error_schema
        image_dict['dq'] = dq_schema
    
        return image_dict
    
        
    def get_sci_level3_schema(self) -> dict[str, typing.Any]:
        """
        Definites the metadata (fits headers) associated with each Level 2
        taken by the coronagraph science camera.


        Return:
        -------
        image_dict : dictionary
          schema converted into a dictionary

        """

        try:
            # Get the path object for the reference file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE3_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                schema_yaml = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE3_FILE}' was not found.")
            return {}, None

        
        image_dict = {}
        data_schema = None
        error_schema = None
        dq_schema = None
        
        # Loop over properties defined in the schema to extract default values
        # set any defaults defined in schema.
        # loop over the level0 schema
        main_properties = schema_yaml.get('properties', {})

        for key,values in main_properties.items():
            if key == 'data':
                data_schema = values['items']
            elif key == 'error':
                error_schema = values['items']
            elif key == 'dq':
                dq_schema = values['items']
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

        image_dict['data'] = data_schema
        image_dict['error'] = error_schema
        image_dict['dq'] = dq_schema
        
        return image_dict



    def validate_level0_schema(self, data_dict):
        """
        Validate a dictionary against the Level 0 schema, including external references. 

        Parameters
        ----------
        data_dict : `dict`
          Dictionary containing information to be validated.

        Returns
        -------
        output : `boolean`
          True if successful, False if validation fails.
        """
        # 1. Load Core Schema Reference
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.REFERENCE_FILE
            with open(schema_path, 'r') as file:
                core_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return False

        # 2. Load Level 0 Schema
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE1A_FILE
            with open(schema_path, 'r') as file:
                main_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE1A_FILE}' was not found.")
            return False

        # 3. Validate the core schema metadata block
        CoreSchema = CoreSchemas()
        if not CoreSchema.validate_core_schema(data_dict.get('meta', {})):
            print('Level1 image meta data did not validate')
            return False

        # 4. Prepare data payload for validation (convert NumPy arrays to lists)
        #data_to_validate = data_dict.copy()
        #if isinstance(data_to_validate.get('data'), np.ndarray):
        #    data_to_validate['data'] = data_to_validate['data'].tolist()  ## THIS TAKES TOO LONG

        # 4. Fast NumPy validation + lightweight slice for jsonschema
        payload_to_validate = data_dict.copy()
        raw_data = payload_to_validate.get('data')

        if isinstance(raw_data, np.ndarray):
            # Instant C-level type/shape checks via NumPy
            if raw_data.ndim != 2:
                print(f"Validation Error: Data array must be 2D, got {raw_data.ndim}D")
                return False
            
            # Pass a 1x1 list slice so jsonschema validates array structure in <1 ms
            payload_to_validate['data'] = raw_data[:1, :1].tolist() if raw_data.size > 0 else []        
        # 5. Resolve core_schema.yaml reference and validate main payload
        try:
            resolver = RefResolver(
                base_uri='esc_image1A_schema.yaml',
                referrer=main_schema,
                store={'core_schema.yaml': core_schema}
            )
            validate(instance=payload_to_validate, schema=main_schema, resolver=resolver)
            return True 
        except ValidationError as e:
            print(f"Validation of Image1A failed. Error: {e.message}")
            return False


    def validate_level1_schema(self, data_dict):
        """
        Validate a dictionary against the Level 1 schema, including external references. 

        Parameters
        ----------
        data_dict : `dict`
          Dictionary containing information to be validated.

        Returns
        -------
        output : `boolean`
          True if successful, False if validation fails.
        """
        # 1. Load Core Schema Reference
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.REFERENCE_FILE
            with open(schema_path, 'r') as file:
                core_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return False

        # 2. Load Level 1 Schema
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE1B_FILE
            with open(schema_path, 'r') as file:
                main_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE1B_FILE}' was not found.")
            return False

        # 3. Validate the core schema metadata block
        CoreSchema = CoreSchemas()
        if not CoreSchema.validate_core_schema(data_dict.get('meta', {})):
            print('Level1 image meta data did not validate')
            return False


        # 4. Prepare data payload for validation (convert NumPy arrays to lists)
        payload_to_validate = data_dict.copy()
        for array_key in ['data', 'error', 'dq']:
            if isinstance(payload_to_validate.get(array_key), np.ndarray):
                payload_to_validate[array_key] = payload_to_validate[array_key].tolist()
            
        # 5. Resolve core_schema.yaml reference and validate main payload
        try:
            resolver = RefResolver(
                base_uri='esc_image1B_schema.yaml',
                referrer=main_schema,
                store={'core_schema.yaml': core_schema}
            )
            validate(instance=payload_to_validate, schema=main_schema, resolver=resolver)
            return True 
        except ValidationError as e:
            print(f"Validation of Image1B failed. Error: {e.message}")
            return False


    def validate_level2_schema(self, data_dict):
        """
        Validate a dictionary against the Level 2 schema, including external references. 

        Parameters
        ----------
        data_dict : `dict`
          Dictionary containing information to be validated.

        Returns
        -------
        output : `boolean`
          True if successful, False if validation fails.
        """
        # 1. Load Core Schema Reference
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.REFERENCE_FILE
            with open(schema_path, 'r') as file:
                core_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return False

        # 2. Load Level 2 Schema
        try:
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE2_FILE
            with open(schema_path, 'r') as file:
                main_schema = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE2_FILE}' was not found.")
            return False

        # 3. Validate the core schema metadata block
        CoreSchema = CoreSchemas()
        if not CoreSchema.validate_core_schema(data_dict.get('meta', {})):
            print('Level2 image meta data did not validate')
            return False

        # 4. Prepare data payload for validation (convert NumPy arrays to lists)
        payload_to_validate = data_dict.copy()
        for array_key in ['data', 'error', 'dq']:
            if isinstance(payload_to_validate.get(array_key), np.ndarray):
                payload_to_validate[array_key] = payload_to_validate[array_key].tolist()
                
        # 5. Resolve core_schema.yaml reference and validate main payload
        try:
            resolver = RefResolver(
                base_uri='esc_image2_schema.yaml',
                referrer=main_schema,
                store={'core_schema.yaml': core_schema}
            )
            validate(instance=payload_to_validate, schema=main_schema, resolver=resolver)
            return True 
        except ValidationError as e:
            print(f"Validation of Image1B failed. Error: {e.message}")
            return False                

        
    def validate_level3_schema(self, data_dict):
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
                core_schema = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.REFERENCE_FILE}' was not found.")
            return {}, None
        
        try:
            # Get the path object for theimage file
            schema_path = files(self.RESOURCE_PACKAGE) / self.IMAGE3_FILE
            
            # Use the Path object for opening the file
            with open(schema_path, 'r') as file:
                main_schema = yaml.safe_load(file)
        except FileNotFoundError:
            # ... (error handling)
            print(f"Error: The resource '{self.RESOURCE_PACKAGE}/{self.IMAGE3_FILE}' was not found.")
            return {}, None

        # Validate the core schema
        CoreSchema = CoreSchemas()
        valid = CoreSchema.validate_core_schema(data_dict['meta'])
        
        if valid is False:
            print('Level3 image meta data did not validate')
            return False
        
        
        # The resolver maps schema URIs (like 'core_schema.yaml') to their content
        resolver = RefResolver(
            base_uri='esc_image1_schema.yaml',  # The base URI of the main schema
            referrer=main_schema,
            store={'core_schema.yaml': core_schema}  # The store holds the content of the external schema
        )
        try:
            # Use the resolver during validation
            validate(instance=data_dict, schema=main_schema, resolver=resolver)
            #print(" Image1 is valid!")
            return True 
        except ValidationError as e:
            print(f"Validation of Image1a failed. Error: {e.message} ")
            return False
        

    def get_image0_schema(self) -> dict[str, typing.Any]:        
        """
        """

        # instantiate core schema
        CoreSchema = CoreSchemas()
        core_dict = CoreSchema.get_sci_core_schema()
        
        image_dict = self.get_sci_level0_schema()

        image = {}
        image['meta'] = core_dict
        image['image'] = image_dict
        return image



    def get_image1_schema(self) -> dict[str, typing.Any]:        
        """
        """

        # instantiate core schema
        CoreSchema = CoreSchemas()
        core_dict = CoreSchema.get_sci_core_schema()
        
        image_dict = self.get_sci_level1_schema()

        image = {}
        image['meta'] = core_dict
        image['image'] = image_dict
        return image
    


    def get_image2_schema(self) -> dict[str, typing.Any]:        
        """
        """

        # instantiate core schema
        CoreSchema = CoreSchemas()
        core_dict = CoreSchema.get_sci_core_schema()
        
        image_dict = self.get_sci_level2_schema()

        image = {}
        image['meta'] = core_dict
        image['image'] = image_dict
        return image
    
    
