#!/bin/python

import yaml
import typing
import jsonschema
from jsonschema import validate

class SchemaValidator:

    def __init__(self, schema_path):
        """
        Initialize the Schema Class with a schema file and load it

        """
        with open(schema_path, 'r') as f:
            try:
                schema = yaml.safe_load(f)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Schema file not found at: {schema_path}")
                exit()
            self.schema = schema

    def load_and_validate_config(self, yaml_path):
        """ Load YAML file schema and validate it with schema."""

        with open(yaml_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        try:
            validate(instance=yaml_data, schema=self.schema)
            print("YAML configuration is valid.")
            return yaml_data
        except jsonschema.exceptions.ValidationError as e:
            print(f"YAML configuration is invalid: {e.message}")
            return None

    def validate_config(self, data):
        """ Validate a data (dictionary)  with schema."""

        try:
            validate(instance=data, schema=self.schema)
            print("Data configuration is valid.")
            return data
        except jsonschema.exceptions.ValidationError as e:
            print(f"YAML configuration is invalid: {e.message}")
            return None
        
# Test below - pull into unit test
#schema_file = 'esc_visit_schema.yaml'
#config_file = '/Users/morrison/Coronagraph_Mission/esc_pipeline/src/esc_pipeline/visits/Program_1231/program_1231_001_R01.yaml'

#visit = SchemaValidator(schema_file)
#loaded_config = visit.load_and_validate_config(config_file)

#if loaded_config:
#    print(f"Loaded config: {loaded_config}")

    
