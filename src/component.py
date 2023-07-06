'''
Template Component main class.

'''
import json
import logging
from dataclasses import asdict
from typing import List, Tuple

from kbcstorage.dataclasses.tables import Column, ColumnDefinition
from kbcstorage.tables import Tables
from keboola.component.base import ComponentBase
from keboola.component.dao import FileDefinition
from keboola.component.exceptions import UserException
# configuration variables
from requests import HTTPError

from sapi_definition import load_definitions_from_dict, SapiTableDefinition

KEY_STACK_URL = 'stack_url'
KEY_API_TOKEN = '#api_token'

KEY_NEWEST_FILES_BY_NAME = 'newest_files'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_API_TOKEN]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()
        self._client: Tables

    def _init_client(self):
        stack_url = self.configuration.parameters.get(KEY_STACK_URL) \
                    or f'https://{self.environment_variables.stack_id}'
        token = self.configuration.parameters[KEY_API_TOKEN]
        if not token:
            raise UserException(
                "The Storage token is not filled in. Please enter a valid Storage Token to the configuration.")
        self._client = Tables(root_url=stack_url, token=token)

    def run(self):
        '''
        Main execution code
        '''

        # check for missing configuration parameters
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        self._init_client()
        params = self.configuration.parameters

        newest = params.get(KEY_NEWEST_FILES_BY_NAME, False)
        input_definitions = self.get_input_files_definitions(only_latest_files=newest)
        self._validate_file_format(input_definitions)

        for f in input_definitions:
            self._create_sapi_table_definition(f)

    def _create_sapi_table_definition(self, definition_file: FileDefinition):
        with open(definition_file.full_path, 'r') as inp:
            sapi_definition_dict = json.load(inp)
        definition_configurations = load_definitions_from_dict(sapi_definition_dict)

        results = []
        for sapi_definition in definition_configurations:
            bucket, name = self._get_table_destination(sapi_definition)

            pkey, columns = self._build_columns(sapi_definition)

            logging.info(f'Creating table definition {sapi_definition.name}')
            logging.debug(f'Creating table definition {asdict(sapi_definition)}')

            try:
                distribution_dict = asdict(sapi_definition.distribution) if sapi_definition.distribution else None
                index_dict = asdict(sapi_definition.index) if sapi_definition.index else None

                result = self._client.create_definition(bucket_id=bucket, name=name,
                                                        primary_keys=pkey, columns=columns,
                                                        distribution=distribution_dict,
                                                        index=index_dict
                                                        )
                results.append(result)
            except HTTPError as e:
                msg = e.response.json().get('errors') or e.response.text
                if e.response.status_code in [401, 403]:
                    raise UserException(f"Failed to perform the requesst, please check your Storage Token."
                                        f" Code: {e.response.status_code} "
                                        f"Errors: {msg}") from e
                else:
                    raise UserException(f"Failed to create the table. Status: {e.response.status_code} "
                                        f"Errors: {msg}") from e

    def _validate_file_format(self, input_definitions):
        invalid = [f for f in input_definitions if not f.name.endswith('.json')]
        if invalid:
            raise UserException(f'Only JSON files are required on the input. '
                                f'Some files have invalid format: {invalid}')

    def _get_table_destination(self, sapi_definition: SapiTableDefinition):
        name = sapi_definition.name
        split_dest = sapi_definition.destination_id.split('.')
        bucket = f'{split_dest[0]}.{split_dest[1]}'

        return bucket, name

    def _split_length_from_datatype(self, datatype: str):
        length = None
        typestr = datatype
        if len(datatype.split('(')) == 2:
            length = datatype.split('(')[1].replace(')', '')
            typestr = datatype.split('(')[0]
        return typestr, length

    def _build_columns(self, sapi_definition: SapiTableDefinition) -> Tuple[List[str], List[Column]]:
        pkey_columns = [c.name for c in sapi_definition.columns if c.PK_Flag]

        columns = []
        for c in sapi_definition.columns:
            typestr, length = self._split_length_from_datatype(c.data_type)
            column_def = Column(name=c.name,
                                definition=ColumnDefinition(type=typestr,
                                                            length=length,
                                                            nullable=c.nullable,
                                                            default=c.default))
            columns.append(column_def)
        return pkey_columns, columns


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
