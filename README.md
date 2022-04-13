Table Definition Generator
=============

Generates table definition based on input JSON file.

**Table of contents:**

[TOC]

Input Format
===================

Accepts JSON files with table definition defined as below:

**Example**

```json
{
  "test_table": {
    "name": "test_table_def",
    "comment": "Comment Will be used in Storage table metadata",
    "stereotype": "Stereotype May be included in table metadata if needed.",
    "shortname": "shortname May be included in table metadata if needed.",
    "destination_id": "in.c-de-test.test_table_def",
    "distribution": {
      "type": "HASH",
      "distributionColumnsNames": [
        "id"
      ]
    },
    "index": {
      "type": "CLUSTERED INDEX",
      "indexColumnsNames": [
        "id"
      ]
    },
    "columns": {
      "id": {
        "data_type": "INT",
        "order": 1,
        "comment": "Will be used in Storage table metadata",
        "nullable": false,
        "PK_Flag": true
      },
      "name": {
        "data_type": "NVARCHAR(200)",
        "order": 2,
        "comment": "Will be used in Storage table metadata",
        "nullable": true,
        "default": "'unnamed'",
        "PK_Flag": false
      }
    }
  },
  "test_table2": {
    "name": "test_table_def2",
    "comment": "Comment Will be used in Storage table metadata",
    "stereotype": "Stereotype May be included in table metadata if needed.",
    "shortname": "shortname May be included in table metadata if needed.",
    "destination_id": "in.c-de-test.test_table_def2",
    "distribution": {
      "type": "HASH",
      "distributionColumnsNames": [
        "id"
      ]
    },
    "index": {
      "type": "CLUSTERED INDEX",
      "indexColumnsNames": [
        "id"
      ]
    },
    "columns": {
      "id": {
        "data_type": "INT",
        "order": 1,
        "comment": "Will be used in Storage table metadata",
        "nullable": false,
        "PK_Flag": true
      },
      "name": {
        "data_type": "NVARCHAR(200)",
        "order": 2,
        "comment": "Will be used in Storage table metadata",
        "nullable": true,
        "default": "'unnamed'",
        "PK_Flag": false
      }
    }
  }
}
``` 

Prerequisites
=============

A KBC Project supporting Table Definitions feature.

Configuration
=============

- `Only newest files` - [OPTIONAL] Default `false`. Process only newest version of each file (by name).


### Example JSON configuration

```json
{"parameters": {
    "#api_token": "1234-xxx",
    "stack_url": "https://connection.eu-central-1.keboola.com/",
    "debug": true
  }
}
```

Output
======

List of tables, foreign keys, schema.

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to
your custom path in the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following
command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone git@bitbucket.org:kds_consulting_team/kds-team.app-table-definition-generator.git kds-team.app-table-definition-generator
cd kds-team.app-table-definition-generator
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers
documentation](https://developers.keboola.com/extend/component/deployment/)
