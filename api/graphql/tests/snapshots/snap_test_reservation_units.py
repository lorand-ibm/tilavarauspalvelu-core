# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['ReservationUnitTestCase::test_getting_hauki_url 1'] = {
    'data': {
        'reservationUnitByPk': {
            'haukiUrl': {
                'url': 'https://test.com/resource/origin:3774af34-9916-40f2-acc7-68db5a627710/?hsa_source=origin&hsa_username=AnonymousUser]&hsa_created_at=2021-05-03 00:00:00+00:00&hsa_valid_until=2021-05-03 00:30:00+00:00&hsa_resource=origin:3774af34-9916-40f2-acc7-68db5a627710&hsa_signature=0e6e068c3b25d7eea2145bb052af903df0730f5536c6cd1739590046f88e9a31'
            },
            'name': 'Test name'
        }
    }
}

snapshots['ReservationUnitTestCase::test_getting_reservation_units 1'] = {
    'data': {
        'reservationUnits': {
            'edges': [
                {
                    'node': {
                        'contactInformation': '',
                        'description': '',
                        'equipment': [
                        ],
                        'images': [
                        ],
                        'location': None,
                        'maxPersons': None,
                        'name': 'Test name',
                        'purposes': [
                        ],
                        'requireIntroduction': False,
                        'reservationUnitType': {
                            'name': 'Test type'
                        },
                        'resources': [
                        ],
                        'services': [
                        ],
                        'spaces': [
                        ],
                        'termsOfUse': ''
                    }
                }
            ]
        }
    }
}
