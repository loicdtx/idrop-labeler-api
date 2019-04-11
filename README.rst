*****************
iDrop labeler API
*****************

*Interface between iDrop labeler client and iDrop db*


Resources
=========

+-------------+----------------------------------------+-----------------------------------------------------------------------+
| HTTP method | URI                                    | Action                                                                |
+=============+========================================+=======================================================================+
| GET         | http://[hostname]/idrop/v0/species     | Retrieve all available species                                        |
+-------------+----------------------------------------+-----------------------------------------------------------------------+
| GET         | http://[hostname]/idrop/v0/studyareas  | Retrieve all available study areas                                    |
+-------------+----------------------------------------+-----------------------------------------------------------------------+
| GET         | http://[hostname]/idrop/v0/inventories | Sample inventory points using optional filters defined in a JSON body |
+-------------+----------------------------------------+-----------------------------------------------------------------------+
| POST        | http://[hostname]/idrop/v0/interpreted | Create a record in the interpreted table                              |
+-------------+----------------------------------------+-----------------------------------------------------------------------+
| GET         | http://[hostname]/idrop/v0/interpreted | Sample interpreted records using optional filters                     |
+-------------+----------------------------------------+-----------------------------------------------------------------------+
| GET         | http://[hostname]/idrop/v0/rawsql      | Send a raw query to the database                                      |
+-------------+----------------------------------------+-----------------------------------------------------------------------+



Examples
========

Retrieve list of species
------------------------

Request

.. code-block:: bash

    curl -X GET https://[hostname]/idrop/v0/species

Response

.. code-block:: json

    {
    "species": [
        {"code": "SAP",
         "name": "sapelli",
         "id": 4},
        {"code": "KOS",
         "name": "kossipo",
         "id": 9}
    ]
    }


Get a random inventory point for a given species
------------------------------------------------

Request

.. code-block:: bash

    curl -X GET \
        -d '{"nSamples": 1, "studyAreaId": null, "speciesId": 4}' \
        http://[hostname]/idrop/v0/inventories


Response

.. code-block:: json

    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "speciesName": "sapelli",
            "speciesCode": "SAP",
            "speciesId": 4,
            "quality": "B",
            "dbh": 12,
            "id": 342
          },
          "geometry": {
            "type": "Point",
            "coordinates": [
              16.17414,
              1.43030
            ]
          }
        }
      ]
    }



Create a record in the interpreted table
----------------------------------------

Request

.. code-block:: bash

    curl -X POST \
    -d '{
      "type": "Feature",
      "properties": {
        "inventoryId": 342,
        "speciesId": 4
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              16.1716309,
              1.43037
            ],
            [
              16.1718508,
              1.43037
            ],
            [
              16.1718508,
              1.4305845
            ],
            [
              16.1716309,
              1.4305845
            ],
            [
              16.1716309,
              1.43037
            ]
          ]
        ]
      }
    }' \
    http://[hostname]/idrop/v0/interpreted


Response

.. code-block:: json

    {"interpretedId": 1}


HTTP status codes
=================

``200``: OK

``201``: Created

``400``: Bad request

``404``: Not found