*****************
iDrop labeler API
*****************

*Interface between iDrop labeler client and iDrop db*


.. image:: https://travis-ci.org/loicdtx/idrop-labeler-api.svg?branch=master
    :target: https://travis-ci.org/loicdtx/idrop-labeler-api


Resources
=========

List of resources
-----------------

+-------------+------------------------------+---------------------------------------------------+
| HTTP method | URI                          | Action                                            |
+=============+==============================+===================================================+
| GET         | /idrop/v0/species            | Retrieve all available species                    |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/studyareas         | Retrieve all available study areas                |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/studyareas/<id>    | Retrieve a single study area by id                |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/inventories        | Get all inventory samples                         |
+-------------+------------------------------+---------------------------------------------------+
| POST        | /idrop/v0/inventories        | Get a subset of inventory samples using filters   |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/inventories/<id>   | Retrieve a single inventory item by id            |
+-------------+------------------------------+---------------------------------------------------+
| PATCH       | /idrop/v0/inventories/<id>   | Update an inventory sample (isInterpreted field)  |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/interpreted        | Get all interpreted records                       |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/interpreted/<id>   | Retrieve a single interpreted item by id          |
+-------------+------------------------------+---------------------------------------------------+
| PUT         | /idrop/v0/interpreted/<id>   | Update/replace an existing interpreted record     |
+-------------+------------------------------+---------------------------------------------------+
| POST        | /idrop/v0/interpreted        | Create a record in the interpreted table          |
+-------------+------------------------------+---------------------------------------------------+
| POST        | /idrop/v0/interpreted/filter | Sample interpreted records using optional filters |
+-------------+------------------------------+---------------------------------------------------+


Details
-------


GET ``idrop/v0/species``
^^^^^^^^^^^^^^^^^^^^^^^^

Get all species

Example query
"""""""""""""


.. code-block:: bash

    curl 0.0.0.0:5000/idrop/v0/species

.. code-block:: json

    {
      "species": [
        {
          "code": "SAP", 
          "id": 1, 
          "name": "sapelli"
        }, 
        {
          "code": "KOS", 
          "id": 2, 
          "name": "kossipo"
        }
      ]
    }


-----

GET ``/idrop/v0/studyareas`` 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a feature collection containing all study areas

Example query
"""""""""""""


.. code-block:: bash

    curl 0.0.0.0:5000/idrop/v0/studyareas


.. code-block:: json

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  15.426567415396372, 
                  1.2072162975867589
                ], 
                [
                  15.428939084211985, 
                  1.207078809539477
                ], 
                [
                  15.428994079430897, 
                  1.2039922028779992
                ], 
                [
                  15.42678052186966, 
                  1.2040059516827275
                ], 
                [
                  15.426567415396372, 
                  1.2072162975867589
                ]
              ]
            ], 
            "type": "Polygon"
          }, 
          "properties": {
            "id": 1, 
            "name": "test_zone"
          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }

-----

GET ``/idrop/v0/studyareas/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a single study area


Example query
"""""""""""""

.. code-block:: bash

    curl 0.0.0.0:5000/idrop/v0/studyareas/1


.. code-block:: json

    {
      "geometry": {
        "coordinates": [
          [
            [
              15.426567415396372, 
              1.2072162975867589
            ], 
            [
              15.428939084211985, 
              1.207078809539477
            ], 
            [
              15.428994079430897, 
              1.2039922028779992
            ], 
            [
              15.42678052186966, 
              1.2040059516827275
            ], 
            [
              15.426567415396372, 
              1.2072162975867589
            ]
          ]
        ], 
        "type": "Polygon"
      }, 
      "properties": {
        "id": 1, 
        "name": "test_zone"
      }, 
      "type": "Feature"
    }

-----

GET ``/idrop/v0/inventories``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a feature collection containing all inventory samples


Example query
"""""""""""""

.. code-block:: bash

    curl 0.0.0.0:5000/idrop/v0/inventories


.. code-block:: json

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              15.42773675239257, 
              1.2063405717582367
            ], 
            "type": "Point"
          }, 
          "properties": {
            "dbh": 12, 
            "id": 1, 
            "isInterpreted": false, 
            "quality": "B", 
            "speciesCode": "SAP", 
            "speciesId": 1, 
            "speciesName": "sapelli"
          }, 
          "type": "Feature"
        }, 
        {
          "geometry": {
            "coordinates": [
              15.429433048078712, 
              1.2056055102942422
            ], 
            "type": "Point"
          }, 
          "properties": {
            "dbh": 9, 
            "id": 4, 
            "isInterpreted": false, 
            "quality": "A", 
            "speciesCode": "KOS", 
            "speciesId": 2, 
            "speciesName": "kossipo"
          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }

-----

POST ``/idrop/v0/inventories``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Query a subset of the inventory samples by applying optional filters. Return a feature collection

Parameters
""""""""""

- ``nSamples`` (int or null): maximum number of samples returned
- ``isInterpreted`` (boolean or null): Restrict results to only samples that have (or not) already been interpreted (or skipped)
- ``speciesId`` (int or null): Restrict results to a single species
- ``studyAreaId`` (int or null): Restrict results to a single study area 
  

Example query
"""""""""""""

.. code-block:: bash

    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"nSamples": 10, "isInterpreted": false, "speciesId": 1, "studyAreaId": 1}' \
        http://0.0.0.0:5000/idrop/v0/inventories

.. code-block:: json

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              15.42773675239257, 
              1.2063405717582367
            ], 
            "type": "Point"
          }, 
          "properties": {
            "dbh": 12, 
            "id": 1, 
            "isInterpreted": false, 
            "quality": "B", 
            "speciesCode": "SAP", 
            "speciesId": 1, 
            "speciesName": "sapelli"
          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }

-----

GET ``/idrop/v0/inventories/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a single inventory record


Example query
"""""""""""""


.. code-block:: bash

    curl http://0.0.0.0:5000/idrop/v0/inventories/3


.. code-block:: json

    {
      "geometry": {
        "coordinates": [
          15.42757044889393, 
          1.2047939492208728
        ], 
        "type": "Point"
      }, 
      "properties": {
        "dbh": 13, 
        "id": 3, 
        "isInterpreted": true, 
        "quality": "A", 
        "speciesCode": "KOS", 
        "speciesId": 2, 
        "speciesName": "kossipo"
      }, 
      "type": "Feature"
    }


-----

PATCH ``/idrop/v0/inventories/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the ``isInterpreted`` field of a single inventory record. 

Parameters
""""""""""

- ``isInterpreted`` (boolean): Value to assign to the ``isInterpreted`` key of the record ``id``


Example query
"""""""""""""


.. code-block:: bash

    curl -X PATCH \
            -H "Content-Type: application/json" \
            -d '{"isInterpreted": false}' \
            http://0.0.0.0:5000/idrop/v0/inventories/2


.. code-block:: json

    {
      "id": 2, 
      "isInterpreted": false
    }

-----

GET ``/idrop/v0/interpreted``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get all interpreted samples as a feature collection


Example query
"""""""""""""

.. code-block:: bash

    curl http://0.0.0.0:5000/idrop/v0/interpreted


.. code-block:: json

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  15.427424, 
                  1.20515
                ], 
                [
                  15.427424, 
                  1.20515
                ], 
                [
                  15.427669, 
                  1.205149
                ], 
                [
                  15.427669, 
                  1.204943
                ], 
                [
                  15.427418, 
                  1.204948
                ], 
                [
                  15.427424, 
                  1.20515
                ]
              ]
            ], 
            "type": "Polygon"
          }, 
          "properties": {
            "id": 1, 
            "inventoryId": 3, 
            "speciesId": 2, 
            "speciesName": "kossipo"
          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }


-----

GET ``/idrop/v0/interpreted/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a single interpreted samples


Example query
"""""""""""""

.. code-block:: bash

    curl http://0.0.0.0:5000/idrop/v0/interpreted/1


.. code-block:: json

    {
      "geometry": {
        "coordinates": [
          [
            [
              15.427424, 
              1.20515
            ], 
            [
              15.427424, 
              1.20515
            ], 
            [
              15.427669, 
              1.205149
            ], 
            [
              15.427669, 
              1.204943
            ], 
            [
              15.427418, 
              1.204948
            ], 
            [
              15.427424, 
              1.20515
            ]
          ]
        ], 
        "type": "Polygon"
      }, 
      "properties": {
        "id": 1, 
        "inventoryId": 3, 
        "speciesId": 2, 
        "speciesName": "kossipo"
      }, 
      "type": "Feature"
    }

-----

POST ``/idrop/v0/interpreted``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new interpreted sample. Calling this resource also has the side effect of changing the ``isInterpreted`` field of the associated inventory sample to ``true``.

Parameters
""""""""""

- A geojson feature of type ``Polygon`` with the properties ``inventoryId`` and ``speciesId``.
  

Example query
"""""""""""""

.. code-block:: bash

    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
      "type": "Feature",
      "properties": {
        "inventoryId": 2,
        "speciesId": 1
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
    http://0.0.0.0:5000/idrop/v0/interpreted


.. code-block:: json

    {
      "interpretedId": 3
    }


-----

PUT ``/idrop/v0/interpreted/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update/replace an already existing interpreted samples


Parameters
""""""""""

- A geojson feature of type ``Polygon`` with the properties ``inventoryId`` and ``speciesId``.


Example query
"""""""""""""

.. code-block:: bash

    curl -X PUT \
    -H "Content-Type: application/json" \
    -d '{
      "type": "Feature",
      "properties": {
        "inventoryId": 2,
        "speciesId": 3
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
    http://0.0.0.0:5000/idrop/v0/interpreted


.. code-block:: json

    204 No Content


-----

POST ``/idrop/v0/interpreted/filter``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Query a subset of the interpreted samples. Return a feature collection


Parameters
""""""""""

- ``nSamples`` (int or null): Maximum number of features in the returned feature collection


Examples
""""""""


.. code-block:: bash

    curl -X POST \
            -H "Content-Type: application/json" \
            -d '{"nSamples": 10}' \
            http://0.0.0.0:5000/idrop/v0/interpreted/filter


.. code-block:: json

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  15.427424, 
                  1.20515
                ], 
                [
                  15.427424, 
                  1.20515
                ], 
                [
                  15.427669, 
                  1.205149
                ], 
                [
                  15.427669, 
                  1.204943
                ], 
                [
                  15.427418, 
                  1.204948
                ], 
                [
                  15.427424, 
                  1.20515
                ]
              ]
            ], 
            "type": "Polygon"
          }, 
          "properties": {
            "id": 1, 
            "inventoryId": 3, 
            "speciesId": 2, 
            "speciesName": "kossipo"
          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }


-----


HTTP status codes
=================

``200``: OK

``201``: Created

``400``: Bad request

``404``: Not found


Install
=======

You must first configure `idb <https://github.com/loicdtx/idrop-db>`_ (database setup and configuration file), then.


Locally
-------


.. code-block:: bash

    git clone git@github.com:loicdtx/idrop-labeler-api.git
    cd idrop-labeler-api
    pip install -r requirements.txt
    pip install -e .
    export FLASK_APP=api
    flask run


Using docker
------------

.. code-block:: bash

    git clone https://github.com/loicdtx/idrop-labeler-api.git
    cd idrop-labeler-api.git
    docker build -t idrop-api:latest .
    docker run --name idrop-api --rm -d -p 5000:5000 -v ~/.idb:/root/.idb idrop-api
