import json
from dataclasses import dataclass
from typing import List, Optional

import dataconf


@dataclass
class Column:
    data_type: str
    order: int
    name: str = ''
    comment: Optional[str] = None
    nullable: bool = False
    default = None
    PK_Flag: bool = False


@dataclass
class Distribution:
    type: str
    distributionColumnsNames: List[str]


@dataclass
class Index:
    type: str
    indexColumnsNames: List[str]


@dataclass
class SapiTableDefinition:
    external_id: str
    name: str
    destination_id: str
    columns: List[Column]
    distribution: Distribution
    index: Index
    comment: str = None
    stereotype: str = None
    shortname: str = None


def _dataclass_from_dict(configuration: dict, clazz):
    json_conf = json.dumps(configuration)
    return dataconf.loads(json_conf, clazz)


def _build_columns_from_dict(cfg: dict):
    columns = []
    for k in cfg:
        default = cfg[k].pop('default', None)
        column = _dataclass_from_dict(cfg[k], Column)
        column.name = k
        column.default = default
        columns.append(column)
    return columns


def _build_tablecfg_from_dict(external_id: str, cfg: dict):
    columns = _build_columns_from_dict(cfg['columns'])
    distribution = _dataclass_from_dict(cfg['distribution'], Distribution)
    index = _dataclass_from_dict(cfg['index'], Index)
    table = SapiTableDefinition(external_id=external_id,
                                name=cfg['name'],
                                destination_id=cfg['destination_id'],
                                columns=columns,
                                distribution=distribution,
                                index=index,
                                comment=cfg.get('comment'),
                                stereotype=cfg.get('stereotype'),
                                shortname=cfg.get('shortname'),
                                )

    return table


def load_definitions_from_dict(definitions: dict) -> List[SapiTableDefinition]:
    """
    Load Sapi table definition configuration from the dict object.
    Args:
        definitions:

    Returns:

    """
    result_definitions = list()
    for k in definitions:
        def_obj = _build_tablecfg_from_dict(k, definitions[k])
        result_definitions.append(def_obj)
    return result_definitions
