import json

from api import app


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

INTERPRETED_FEATURE_2 = {'geometry': {
        'coordinates': [[(15.427424, 1.205150),
                         (15.427424, 1.205150),
                         (15.427669, 1.205149),
                         (15.427669, 1.204943),
                         (15.427418, 1.204948),
                         (15.427424, 1.205150)]],
        'type': 'Polygon'},
    'properties': {'inventoryId': 3, 'speciesId': 1},
    'type': 'Feature'}


def idrop_api(client, endpoint, verb='get', body=None):
    """Wrapper to facilitate interaction with the API"""
    response = getattr(client, verb)(HOST + endpoint, data=json.dumps(body),
                                     content_type='application/json')
    status = response.status_code
    data = response.json
    return (status, data)


def test_get_species():
    # Species
    status, sp = idrop_api(client, 'species')
    assert status == 200
    assert isinstance(sp['species'], list)


def test_get_studyareas():
    # Study areas
    status, sa = idrop_api(client, 'studyareas')
    assert status == 200
    assert isinstance(sa['features'], list)
    assert [x in sa['features'][0] for x in ['geometry', 'properties', 'type']]


def test_get_single_studyarea():
    # Single study area
    status, sa = idrop_api(client, 'studyareas/1')
    assert status == 200
    assert isinstance(sa, dict)
    assert 'properties' in sa
    assert 'geometry' in sa
    assert sa['geometry']['type'] == 'Polygon'


def test_get_inventories():
    # Inventories
    status, inv = idrop_api(client, 'inventories')
    assert status == 200
    assert isinstance(inv, dict)
    assert inv['type'] == 'FeatureCollection'
    assert len(inv['features']) == 4


def test_get_inventories_filter_0():
    # Inventories with json body
    status, inv = idrop_api(client, 'inventories', verb='post',
                            body={'nSamples': 2,
                                  'studyAreaId': 1,
                                  'speciesId': None})
    assert status == 200
    assert len(inv['features']) == 2


def test_get_inventories_filter_0_hits():
    # Inventories with json body
    status, c = idrop_api(client, 'inventories/hits', verb='post',
                            body={'nSamples': 2,
                                  'studyAreaId': 1,
                                  'speciesId': None})
    assert status == 200
    assert c == 2

def test_get_inventories_filter_1():
    # Inventories with json body
    status, inv = idrop_api(client, 'inventories', verb='post',
                            body={'nSamples': None,
                                  'studyAreaId': None,
                                  'speciesId': 2})
    assert status == 200
    assert len(inv['features']) == 2


def test_get_single_inventory():
    # Single inventory point
    status, inv = idrop_api(client, 'inventories/1')
    assert status == 200
    assert inv['type'] == 'Feature'
    assert inv['geometry']['type'] == 'Point'
    assert inv != idrop_api(client, 'inventories/2')[1]


def test_insert_interpreted():
    # Insert a geometry
    status, interp = idrop_api(client, 'interpreted', verb='post',
                               body=INTERPRETED_FEATURE)
    assert status == 201
    assert interp == {'interpretedId': 1}
    assert idrop_api(client, 'inventories/3')[1]['properties']['isInterpreted'] is True


def test_get_interpreted():
    # Get all interpreted records
    # These are not independent from test_post_methods
    status, interp = idrop_api(client, 'interpreted')
    assert status == 200
    assert isinstance(interp, dict)
    assert interp['type'] == 'FeatureCollection'
    assert len(interp['features']) == 1


def test_get_interpreted_filter():
    status, interp = idrop_api(client, 'interpreted/filter', verb='post',
                               body={'nSamples': 1})
    assert status == 200
    assert isinstance(interp, dict)
    assert interp['type'] == 'FeatureCollection'
    assert len(interp['features']) == 1


def test_get_interpreted_filter_2():
    # New feature idb 0.0.3, only tests that passing the filters does not fail,
    # but test db does not contain enough samples for real tests
    status, interp = idrop_api(client, 'interpreted/filter', verb='post',
                               body={'speciesId': 2, 'inventoryId': 3})
    assert status == 200
    assert isinstance(interp, dict)
    assert interp['type'] == 'FeatureCollection'
    assert len(interp['features']) == 1


def test_get_single_interpreted():
    status, interp = idrop_api(client, 'interpreted/1')
    assert status == 200
    assert isinstance(interp, dict)
    assert [x in interp for x in ['geometry', 'properties', 'type']]
    assert interp['properties']['speciesId'] == 2


def test_update_interpreted():
    status, interp = idrop_api(client, 'interpreted/1', verb='put',
                               body=INTERPRETED_FEATURE_2)
    assert status == 204
    assert interp == None
    # Check successful update
    status, interp_2 = idrop_api(client, 'interpreted/1')
    assert interp_2['properties']['speciesId'] == 1


def test_update_inventory():
    # Simulate a skip
    status, inv = idrop_api(client, 'inventories/2', verb='patch',
                            body={'isInterpreted': True})
    assert status == 200
    assert inv == {'id': 2, 'isInterpreted': True}
    assert idrop_api(client, 'inventories/2')[1]['properties']['isInterpreted'] is True


def test_update_inventory_2():
    # Add a comment
    status, inv = idrop_api(client, 'inventories/2', verb='patch',
                            body={'comment': 'Hello world!'})
    assert status == 200
    assert inv == {'id': 2, 'comment': 'Hello world!'}
    assert idrop_api(client, 'inventories/2')[1]['properties']['isInterpreted'] is True
    assert idrop_api(client, 'inventories/2')[1]['properties']['comment'] is 'Hello world!'


def test_get_inventories_filter_2():
    # New test now that some records have been interpreted
    status, inv = idrop_api(client, 'inventories', verb='post',
                            body={'nSamples': None,
                                  'studyAreaId': None,
                                  'isInterpreted': False,
                                  'speciesId': None})
    assert status == 200
    assert len(inv['features']) == 2



