import json

from app import app


client = app.test_client()

HOST = '/idrop/v0/'

INTERPRETED_FEATURE = {'geometry': {
        'coordinates': [[(15.427424, 1.205150),
                         (15.427424, 1.205150),
                         (15.427669, 1.205149),
                         (15.427669, 1.204943),
                         (15.427418, 1.204948),
                         (15.427424, 1.205150)]],
        'type': 'Polygon'},
    'properties': {'inventoryId': 3, 'speciesId': 2},
    'type': 'Feature'}


def idrop_api(client, endpoint, verb='get', body=None):
    """Wrapper to facilitate interaction with the API"""
    response = getattr(client, verb)(HOST + endpoint, data=json.dumps(body),
                                     content_type='application/json')
    status = response.status_code
    data = response.json
    return (status, data)


def test_get_methods():
    # Species
    status, sp = idrop_api(client, 'species')
    assert status == 200
    assert isinstance(sp['species'], list)
    # Study areas
    status, sa = idrop_api(client, 'studyareas')
    assert status == 200
    assert isinstance(sa['features'], list)
    # Single study area
    status, sa = idrop_api(client, 'studyareas/1')
    assert status == 200
    assert isinstance(sa, dict)
    assert 'properties' in sa
    assert 'geometry' in sa
    assert sa['geometry']['type'] == 'Polygon'
    # Inventories
    status, inv = idrop_api(client, 'inventories')
    assert status == 200
    assert isinstance(inv, dict)
    assert inv['type'] == 'FeatureCollection'
    assert len(inv['features']) == 1
    # Inventories with json body
    status, inv = idrop_api(client, 'inventories', body={'nSamples': 2,
                                                         'studyAreaId': 1,
                                                         'speciesId': None})
    assert status == 200
    assert len(inv['features']) == 2
    # Single inventory point
    status, inv = idrop_api(client, 'inventories/1')
    assert status == 200
    assert inv['type'] == 'Feature'
    assert inv['geometry']['type'] == 'Point'
    assert inv != idrop_api(client, 'inventories/2')[1]


def test_post_methods():
    # Insert a geometry
    status, interp = idrop_api(client, 'interpreted', verb='post',
                               body=INTERPRETED_FEATURE)
    assert status == 201
    assert interp == {'interpretedId': 1}
    assert idrop_api(client, 'inventories/3')[1]['properties']['isInterpreted'] is True


def test_get_interpreted():
    # These are not independent from test_post_methods
    status, interp = idrop_api(client, 'interpreted', body={'nSamples': 1})
    assert status == 200
    assert isinstance(interp, dict)
    assert len(interp) == 1


def test_put_methods():
    # Simulate a skip
    status, inv = idrop_api(client, 'inventories/2', verb='put',
                            body={'isInterpreted': True})
    assert status == 200
    assert inv == {'id': 2, 'isInterpreted': True}
    assert idrop_api(client, 'inventories/2')[1]['properties']['isInterpreted'] is True

