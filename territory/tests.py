"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from territory.models import *

class DiplomacyTest(TestCase):
    def setUp(self):
        self.gameboard = GameBoard.objects.create(turn=1)
        self.turn = GameBoard.get_turn
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


    def move_from(self, terr, turn=None):
        if not turn: turn=self.gameboard.turn-1
        return Action.objects.get(territory=terr, turn=turn)

    def moves_to(self, terr):
        return Action.objects.filter(target=terr, turn=self.gameboard.turn-1)

    def assertMoveResult(self, terr, result):
        mv = self.move_from(terr)
        self.assertEqual((mv, validation_str(result)), (mv, validation_str(mv.validation_level)))

    def assertMoveResults(self, moves):
        for m in moves:
            self.assertMoveResult(m[0], m[1])

    def make_moves(self, moves):
        return map(Action.parse_move, map(lambda x: x.strip(), moves.strip().split("\n")))

    def test_unit_placement(self):
        self.assertTrue(self.ts['A'].has_unit)
        self.assertFalse(self.ts['F'].has_unit)

    def test_connectivity(self):
        self.assertTrue(self.ts['A'].connects_to(self.ts['B']))
        self.assertFalse(self.ts['F'].connects_to(self.ts['A']))

    def test_move_parsing_and_validating(self):
        self.make_moves("""
        US C Move F
        US A Spec Arglefraster
        UK G Move E
        RU D Supp G Move E
        RU B Hold
        """)
        self.assertRaises(Action.InvalidMoveError, Action.parse_move, 'US Q Hold') # Non-territory
        self.assertRaises(Action.InvalidMoveError, Action.parse_move, 'US E Hold') # No unit there
        self.assertRaises(Action.InvalidMoveError, Action.parse_move, 'US H Hold') # Not US's unit
        self.assertRaises(Action.InvalidMoveError, Action.parse_move, 'UK H Supp B Hold') # H and B not adjacent
        self.assertRaises(Action.InvalidMoveError, Action.parse_move, 'UK H Supp D Move B') # H and B not adjacent
        self.assertRaises(RuntimeError, Action.parse_move, 'UK H Foo')

    def assertOwns(self, faction, terrs):
        return self.assertTrue(sorted(terrs), sorted(list(Territory.objects.filter(owner__code=faction).values_list('code', flat=True))))

    def assertUnits(self, faction, terrs):
        return self.assertListEqual(sorted(terrs), sorted(list(Unit.live_units().filter(faction__code=faction).values_list('territory__code', flat=True))))

    def test_s_code(self):
        a = Territory.objects.get(code='A')
        a.name = 'Arglefraster'
        a.save()

        self.assertEqual('Arg', a.s_code)

    def test_no_unit(self):
        a = Action.parse_move('RU B Move E')
        Unit.objects.get(territory__code='B').delete()

        self.gameboard.execute_turn()

        a = Action.objects.get(target__code='E',territory__code='B')

        self.assertEqual(E_NOUNIT, a.validation_level)

    def test_support(self):
        # Basic support
        a = Action.parse_move("RU B Move E")
        s = Action.parse_move("RU D Supp B Move E")
        self.assertTrue(s.provides_support())
        self.assertEqual([s], a.supporters())
        self.assertEqual(1, a.support_strength)

        # Unrelated support doesn't change anything
        _ = Action.parse_move("US C Supp A Hold")
        self.assertTrue(s.provides_support())
        self.assertEqual([s], a.supporters())
        self.assertEqual(1, a.support_strength)

        # Supporting the wrong action doesn't help
        u = Action.parse_move("US A Supp B Hold")
        self.assertTrue(u.provides_support())
        self.assertTrue(s.provides_support())
        self.assertEqual([s], a.supporters())
        self.assertEqual(1, a.support_strength)

        # Cut support
        c = Action.parse_move("UK G Move D")
        self.assertFalse(s.provides_support())
        self.assertEqual([], a.supporters())
        self.assertEqual(0, a.support_strength)

        self.gameboard.execute_turn()

        self.assertOwns('RU', ['B','D','E'])
        self.assertUnits('RU', ['D', 'E'])
        self.assertUnits('US', ['A', 'C'])
        self.assertUnits('UK', ['G', 'H'])

    def test_bounce(self):
        Action.parse_move("RU B Move E")
        Action.parse_move("UK G Move E")

        self.gameboard.execute_turn()

        a = Action.objects.get(faction__code='RU',type=MOVE)
        b = Action.objects.get(faction__code='UK',type=MOVE)

        self.assertEqual(F_BOUNCE, a.validation_level)
        self.assertEqual(F_BOUNCE, b.validation_level)

        self.make_moves("""
        RU D Supp B Hold
        RU B Hold
        US A Move B
        US C Supp A Move B
        """)

        self.gameboard.execute_turn()
        self.assertUnits('RU', ['B', 'D'])
        self.assertUnits('US', ['A', 'C'])

    def test_no_swap(self):
        Action.parse_move("RU D Move G")
        Action.parse_move("UK G Move D")

        self.gameboard.execute_turn()

        a = Action.objects.get(faction__code='RU', type=MOVE)
        b = Action.objects.get(faction__code='UK', type=MOVE)

        self.assertEqual(F_NOSWAP, a.validation_level)
        self.assertEqual(F_NOSWAP, b.validation_level)

    def test_hold(self):
        # No moves -- everyone holds

        self.gameboard.execute_turn()

        for m in ['A','B','C','D','G','H']:
            self.assertEqual(HOLD, self.move_from(m).type)
            self.assertMoveResult(m, V_SUCCESS)

    def test_no_destruction(self):
        """
        A standoff does not destroy a unit in the location where the standoff takes place.
        """
        self.make_moves("""
        US C Move F
        US A Move C
        RU B Move E
        """)

        self.gameboard.execute_turn()

        self.make_moves("""
        US F Move E
        US C Supp F Move E
        UK G Move E
        UK H Supp G Move E
        """)

        self.gameboard.execute_turn()

        self.assertUnits('RU',['D','E'])

    def test_cant_destroy_own_unit(self):
        Unit.objects.create(faction=self.ru, territory=Territory.objects.get(code='E'))

        self.make_moves("""
        UK G Supp D Move E
        RU D Move E
        """)

        self.gameboard.execute_turn()

        self.assertMoveResult('D', F_NODESTROY)
        self.assertMoveResult('G', F_NOSUPPDESTROY)
        self.assertMoveResult('E', V_SUCCESS)

    def test_three_way_standoff(self):
        self.make_moves("""
        US C Move F
        US A Move C
        """)
        self.gameboard.execute_turn()

        self.make_moves("""
        US F Move E
        US C Supp F Move E
        UK G Move E
        UK H Supp G Move E
        RU D Move E
        RU B Supp D Move E
        """)

        self.gameboard.execute_turn()

        self.assertFalse(Territory.objects.get(code='E').has_unit)

    def test_three_way_swap(self):
        self.make_moves("""
        RU B Move A
        US A Move C
        US C Move B
        """)

        self.assertUnits('RU',['B','D'])
        self.assertUnits('US',['A','C'])

        self.gameboard.execute_turn()

        self.assertUnits('RU',['A','D'])
        self.assertUnits('US',['B','C'])

    def test_destruction(self):
        self.make_moves("""
        US A Move B
        US C Supp A Move B
        RU B Hold
        """)

        self.assertUnits('RU', ['B', 'D'])
        self.assertUnits('US', ['A', 'C'])

        self.gameboard.execute_turn()

        self.assertUnits('RU', ['D'])
        self.assertUnits('US', ['B', 'C'])

    def test_bounce_on_moveout(self):
        self.make_moves("""
        RU B Move E
        US A Move B
        RU D Move B
        """)

        self.gameboard.execute_turn()

        self.assertEqual(V_SUCCESS, self.move_from('B').validation_level)

        for m in self.moves_to('B'):
            self.assertEqual(F_BOUNCE, m.validation_level)

    def test_cant_cut_support_against_self(self):
        self.make_moves("""
        RU D Move E
        """)

        self.gameboard.execute_turn()

        self.make_moves("""
        RU B Move C
        RU E Supp B Move C
        US C Move E
        """)

        self.gameboard.execute_turn(debug=True)

        print self.move_from('C')

        self.assertMoveResult('C', F_LOSE)
        self.assertMoveResult('B', V_SUCCESS)

    def test_cant_support_own_destruction(self):
        self.make_moves("""
        RU B Move A
        US C Supp B Move A
        US A Hold
        """)

        a = self.move_from('C', turn=1)

        self.gameboard.execute_turn()

        self.assertFalse(self.move_from('C').provides_support())

        self.assertMoveResult('B', F_BOUNCE)
        self.assertMoveResult('A', V_SUCCESS)
        self.assertMoveResult('C', F_NOSUPPDESTROY)

    def test_support_cut_from_destroyed_unit(self):
        # Support is cut if the supporting unit is destroyed.
        Unit.objects.create(faction=self.ru, territory=Territory.objects.get(code='E'))
        Unit.objects.create(faction=self.ru, territory=Territory.objects.get(code='F'))

        self.make_moves("""
        RU F Move C
        RU E Supp F Move C
        US A Move B
        US C Supp A Move B
        """)

        self.gameboard.execute_turn()

        self.assertMoveResult('F', V_SUCCESS)
        self.assertMoveResult('E', V_SUCCESS)
        self.assertMoveResult('C', F_SUPPORTCUT)
        self.assertMoveResult('A', F_BOUNCE)

    def test_self_attack_does_not_cut_support(self):
        Unit.objects.create(faction=self.ru, territory=Territory.objects.get(code='E'))
        self.make_moves("""
        RU B Move C
        RU E Supp B Move C
        RU D Move E
        """)

        self.gameboard.execute_turn()

        self.assertMoveResults([
            ('B', V_SUCCESS),
            ('E', V_SUCCESS),
            ('D', F_NODESTROY)
        ])

    def test_chained_move_fail(self):
        # A failed move can stop others from moving.
        self.make_moves("""
        US C Move A
        US A Move B
        RU B Move D
        RU D Move G
        UK G Move H
        UK H Hold
        """)

        self.gameboard.execute_turn()

        self.assertMoveResults([
            ('C', F_BOUNCE),
            ('A', F_BOUNCE),
            ('B', F_BOUNCE),
            ('D', F_BOUNCE),
            ('G', F_NODESTROY),
            ('H', V_SUCCESS)
        ])