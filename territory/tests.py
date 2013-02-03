"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from territory.models import Faction, Territory, Unit, Action


class DiplomacyTest(TestCase):
    def setUp(self):
        self.turn = 1
        self.usa = Faction.objects.create(code='US', name='USA')
        self.ru = Faction.objects.create(code='RU', name='Russia')
        self.uk = Faction.objects.create(code='UK', name='Britain')

        territories = {
            'A': {
                'connects': ['B', 'C'],
                'owner': 'US'
            },
            'B': {
                'connects': ['A', 'C', 'D', 'E'],
                'owner': 'RU'
            },
            'C': {
                'connects': ['A', 'B', 'E', 'F'],
                'owner': 'US'
            },

            'D': {
                'connects': ['B', 'E', 'G'],
                'owner': 'RU'
            },
            'E': {
                'connects': ['B', 'C', 'D', 'F', 'G', 'H'],
                'owner': None
            },
            'F': {
                'connects': ['C', 'E', 'H'],
                'owner': None
            },
            'G': {
                'connects': ['D', 'E', 'H'],
                'owner': 'UK'
            },
            'H': {
                'connects': ['E', 'G', 'H'],
                'owner': 'UK'
            }
        }

        self.ts = {}
        for code, ter in territories.items():
            t = Territory.objects.create(code=code, name=code)
            self.ts[code] = t
            if ter['owner']:
                t.owner = Faction.objects.get(code=ter['owner'])
                t.save()
                Unit.objects.create(faction=t.owner,
                    territory=t)
            for tc in ter['connects']:
                if Territory.objects.filter(code=tc).exists():
                    to = Territory.objects.get(code=tc)
                    t.connects.add(to)
                    self.assertTrue(t.connects_to(to))
                    self.assertTrue(to.connects_to(t))


    def make_moves(self, moves):
        map(self.parse_move, moves)

    def test_unit_placement(self):
        self.assertTrue(self.ts['A'].has_unit)
        self.assertFalse(self.ts['F'].has_unit)

    def test_connectivity(self):
        self.assertTrue(self.ts['A'].connects_to(self.ts['B']))
        self.assertFalse(self.ts['F'].connects_to(self.ts['A']))

    def test_basic_moves(self):
        Action.parse_move('C Move F')