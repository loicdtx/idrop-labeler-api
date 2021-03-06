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
| POST        | /idrop/v0/inventories/hits   | Get the number of features of POST inventories    |
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
| POST        | /idrop/v0/neighbours         | Seach inventory records in the neighbourhood      |
+-------------+------------------------------+---------------------------------------------------+
| GET         | /idrop/v0/experiments        | Get all experiments                               |
+-------------+------------------------------+---------------------------------------------------+
| POST        | /idrop/v0/windows            | Get the training windows of a given experiment    |
+-------------+------------------------------+---------------------------------------------------+
| PATCH       | /idrop/v0/windows            | Update the complete property of a list of windows |
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
            "speciesName": "sapelli",
            "comment": null
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
            "speciesName": "kossipo",
            "comment": null

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
- ``spatialFilter`` (object or null): A spatial filter object (must contain lat, lon, and radius (in meters) properties). Only inventory records that intersect with the circle created are returned.
  

Example query
"""""""""""""

.. code-block:: bash

    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"nSamples": 10, "isInterpreted": false, "speciesId": 1, "studyAreaId": 1, "spatialFilter": {"lat": 1.1309, "lon": 15.4678, "radius": 60}}' \
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
            "speciesName": "sapelli",
            "comment": null

          }, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }

-----

POST ``/idrop/v0/inventories/hits``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the number of hits (length of feature collection) of a given by a ``POST`` query to ``inventories``. Has exactly the same parameters as ``POST /idrop/v0/inventories``

Parameters
""""""""""

- ``nSamples`` (int or null): maximum number of samples returned
- ``isInterpreted`` (boolean or null): Restrict results to only samples that have (or not) already been interpreted (or skipped)
- ``speciesId`` (int or null): Restrict results to a single species
- ``studyAreaId`` (int or null): Restrict results to a single study area
- ``spatialFilter`` (object or null): A spatial filter object (must contain lat, lon, and radius (in meters) properties). Only inventory records that intersect with the circle created are returned.
  

Example query
"""""""""""""

.. code-block:: bash

    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"nSamples": null, "isInterpreted": false, "speciesId": 1, "studyAreaId": 1}' \
        http://0.0.0.0:5000/idrop/v0/inventories/hits

.. code-block:: json

    342

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
        "speciesName": "kossipo",
        "comment": null

      }, 
      "type": "Feature"
    }


-----

PATCH ``/idrop/v0/inventories/<id>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the ``isInterpreted`` and/or the ``comment`` fields of a single inventory record. 

Parameters
""""""""""

- ``isInterpreted`` (boolean): Value to assign to the ``isInterpreted`` key of the record ``id``
- ``comment`` (str): A string to add to the comment field of the inventory table


Example query
"""""""""""""


.. code-block:: bash

    curl -X PATCH \
            -H "Content-Type: application/json" \
            -d '{"isInterpreted": false,
                 "comment": "Hello world!"}' \
            http://0.0.0.0:5000/idrop/v0/inventories/2


.. code-block:: json

    {
      "id": 2, 
      "isInterpreted": false,
      "comment": "Hello world!"
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

POST ``/idrop/v0/neighbours``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Search inventory samples that are in the neighbourhood of another provided sample. The provided sample is automatically excluded from the featureCollection returned.


Parameters
""""""""""

- ``inventoryId`` (int): The id of the inventory sample around which the spatial search is performed
- ``distance`` (float): Search radius in meters
- ``speciesId`` (int, list of int or null): Optional list of speciesId to restrict restrict the search


Examples
""""""""


.. code-block:: bash

    curl -X POST \
            -H "Content-Type: application/json" \
            -d '{"inventoryId": 12, "distance": 200, "speciesId": [22, 3]}' \  # 22 and 3 corresponds to ids of SAP and AZO in species table
            http://0.0.0.0:5000/idrop/v0/neighbours


.. code-block:: json

        {"features": [{"geometry": {"coordinates": [15.4234, 1.1752], "type": "Point"},
                       "properties": {"dbh": 12,
                                      "id": 14,
                                      "isInterpreted": false,
                                      "quality": "D",
                                      "speciesCode": "SAP",
                                      "speciesId": 22,
                                      "comment": null,
                                      "speciesName": "sapelli"},
                       "type": "Feature"},
                      {"geometry": {"coordinates": [16.39673, 1.2927], "type": "Point"},
                       "properties": {"dbh": 10,
                                      "id": 15,
                                      "isInterpreted": false,
                                      "quality": "B",
                                      "speciesCode": "SAP",
                                      "speciesId": 22,
                                      "comment": null,
                                      "speciesName": "sapelli"},
                       "type": "Feature"},
                      {"geometry": {"coordinates": [16.23559, 1.29474],
                                    "type": "Point"},
                       "properties": {"dbh": 8,
                                      "id": 25189,
                                      "isInterpreted": false,
                                      "quality": "C",
                                      "speciesCode": "AZO",
                                      "speciesId": 3,
                                      "comment": null,
                                      "speciesName": "azobe"},
                       "type": "Feature"},
                      {"geometry": {"coordinates": [16.19604, 1.20542],
                                    "type": "Point"},
                       "properties": {"dbh": 15,
                                      "id": 25408,
                                      "isInterpreted": false,
                                      "quality": "B",
                                      "speciesCode": "AZO",
                                      "speciesId": 3,
                                      "comment": null,
                                      "speciesName": "azobe"},
                       "type": "Feature"}],
         "type": "FeatureCollection"}


-----

POST ``/idrop/v0/interpreted/filter``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Query a subset of the interpreted samples. Return a feature collection


Parameters
""""""""""

- ``nSamples`` (int or null): Maximum number of features in the returned feature collection
- ``speciesId`` (int or null): Restrict to a single species
- ``inventoryId`` (int or null): Restrict search results to a single inventoryId (resulting feature collection should have a max length of 1)
- ``spatialFilter`` (object or null): A spatial filter object (must contain lat, lon, and radius (in meters) properties). Only interpreted records that intersect with the circle created are returned.


Examples
""""""""


.. code-block:: bash

    curl -X POST \
            -H "Content-Type: application/json" \
            -d '{"nSamples": 10, "spatialFilter": {"lat": 1.1309, "lon": 15.4678, "radius": 60}}' \
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

GET ``/idrop/v0/experiments``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get all experiments. Return a list of objects


Examples
""""""""


.. code-block:: bash

    curl http://0.0.0.0:5005/idrop/v0/experiments


.. code-block:: json

    [{"comment":"Training windows of 1300 pixels covering aac_2019_1 and aac_2019_2","id":1,"name":"scenario_3_1300"}]


-----

POST ``/idrop/v0/windows``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Query training windows of a given experiment with option to merge spatially overlapping windows. Returns a FeatureCollection


Parameters
""""""""""

- ``experimentId`` (int): id of the experiment related to the desired windows
- ``union`` (bool): Whether spatially overlapping windows should be merged as a single polygon in the results


Examples
""""""""


.. code-block:: bash

    curl -X POST \                               
        -H "Content-Type: application/json" \
        -d '{"experimentId":1, "union":true}' \
        http://0.0.0.0:5005/idrop/v0/windows



.. code-block:: json

    {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    [
                        [
                            15.443013547112,
                            1.1058701327040001
                        ],
                        [
                            15.442168362512001,
                            1.1058701327040001
                        ],
                        [
                            15.442168362512001,
                            1.1067208358040002
                        ],
                        [
                            15.443013547112,
                            1.1067208358040002
                        ],
                        [
                            15.443013547112,
                            1.1058701327040001
                        ]
                    ]
                ],
                "type": "Polygon"
            },
            "properties": {
                "allComplete": false,
                "ids": [
                    352
                ]
            }
        },
        {
            "geometry": {
                "coordinates": [
                    [
                        [
                            15.446853314735998,
                            1.105818571404
                        ],
                        [
                            15.446008130135999,
                            1.105818571404
                        ],
                        [
                            15.446008130135999,
                            1.106669274504
                        ],
                        [
                            15.446853314735998,
                            1.106669274504
                        ],
                        [
                            15.446853314735998,
                            1.105818571404
                        ]
                    ]
                ],
                "type": "Polygon"
            },
            "properties": {
                "allComplete": false,
                "ids": [
                    30
                ]
            }
        }
    ],
    "type": "FeatureCollection"
    }

-----

PATCH ``/idrop/v0/windows``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the ``complete`` field of a list of windows. 

Parameters
""""""""""

- ``ids`` (array): The ``id``s of the windows to be updated
- ``complete`` (bool): Whether the ``complete`` property of the targetted windows should be set to ``true`` or ``false``


Example query
"""""""""""""


.. code-block:: bash

    curl -X PATCH \
        -H "Content-Type: application/json" \
        -d '{"ids": [7,8,9], "complete": true}' \
        http://0.0.0.0:5005/idrop/v0/windows


.. code-block:: json

    {"complete":true,"ids":[7,8,9]}

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
    # Create the database tables
    docker exec idrop-api python3 -c "from idb.db import init_db; init_db()"

    # Or if the container is part of a docker-compose you can run
    docker-compose run --rm --entrypoint "python3" idrop-api -c "from idb.db import init_db; init_db()"

