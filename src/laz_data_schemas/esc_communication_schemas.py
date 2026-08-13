import typing
import yaml


class EscCommunicationSchemas:
    def get_telemetry_schema() -> dict[str, typing.Any]:
        """
        Defines telemetry for coronograph instrument.
        Each output is a key-value object

        Returns
        -------
            output: `dict`
                Dictionary of the schema

        """

        schema_yaml = """
        $schema: http://json-schema.org/draft-07/schema#
        $id: get_telemetry_schema.yaml
        title: ETC Telemetry Schema v0.0.1
        description: Definition of the telemetry streams coming from the instrument.
        properties:
            temp1:
                type: number
                description: Temperature of item X (TBR)
                units: K
                frequency: Hz
            dm_pwr:
                type: number
                description: Power draw from DM (TBR)
                units: Watts
        """

        return yaml.safe_load(schema_yaml)

    def get_event_schema() -> dict[str, typing.Any]:
        """
        Defines events for coronograph instrument.
        Each output is a key-value object

        Returns
        -------
            output: `dict`
                Dictionary of the schema

        """

        schema_yaml = """
        $schema: http://json-schema.org/draft-07/schema#
        $id: get_event_schema.yaml
        title: ETC Event Schema v0.0.1
        description: Definition of the events published by the instrument.
        properties:
            led_src_pwr:
                type: boolean
                description: LED powered on?
                units: dimensionless
            filter_pos:
                type: integer
                description: Filter wheel position
                units: dimensionless
            filter_inpos:
                type: boolean
                description: Filter wheel in commanded position?
                units: dimensionless
            llowfs_src_pwr: 
                type: boolean
                description: LLOWFS camera powered on?
                units: dimensionless
            llowfs_corr:
                type: number
                description: LLOWFS correction frequency
                units: Hz
            llowfs_alg:
                type: list
                description: LLOWFS algorithm
                enum: ['TBR1', 'TBR2']
            llowfs_loop_closed:
                type: boolean
                description: LLOWFS loop closed?
                units: dimensionless

        """

    def get_command_schema() -> dict[str, typing.Any]:
        """
        Defines commands for coronograph instrument.
        Each value is a key-value object.

        TBR if this is required as it is architecture dependent.

        Returns
        -------
            output: `dict`
                Dictionary of the schema

        """

        return NotImplementedError()
