import json
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.db.models import Q, F
from singleton_models.models import SingletonModel

ML = 256

SUPPLYDEPOT = "Supply Center"
AIRBASE = "Airbase"
MINE = "Mine"
FACTORY = "Factory"
LAB = "Research Lab"

special_choices = (
    (SUPPLYDEPOT, SUPPLYDEPOT),
    (MINE,MINE),
    (FACTORY,FACTORY),
    (AIRBASE,AIRBASE),
    (LAB,LAB)
)

class Territory(models.Model):
    code = models.CharField(max_length=ML, primary_key=True, unique=True)
    name = models.CharField(max_length=ML)
    pts_s = models.CharField(max_length=ML * 2, blank=True)
    connects = models.ManyToManyField('Territory', related_name='t_connects', symmetrical=True)
    center_s = models.CharField(max_length=ML, blank=True)
    owner = models.ForeignKey('Faction', null=True, blank=True)
    special = models.CharField(max_length=ML, blank=True, null=True, choices=special_choices)
    special_type = models.CharField(max_length=ML, blank=True, null=True)

    @classmethod
    def convert_pt(cls, pt):
        return pt[0] * 1.7, (370 - pt[1]) * 1.7

    @classmethod
    def convert_points(cls, pts):
    #        return pts
        return map(Territory.convert_pt, pts)

    @property
    def s_code(self):
        return self.name.replace(' ', '')[:3]

    def to_json(self):
        return json.dumps({
            'code': self.code,
            's_code': self.s_code,
            'name': self.name,
            'points': self.pts,
            'connects': [x.code for x in self.connects.all()],
            'center': self.js_center(),
            'owner': self.owner.name if self.owner else '',
            'color': self.owner.color if self.owner else 'white',
            'special': self.special,
            'has_unit': self.has_unit,
            #            'has_order': self.order() is not None
        })

    @property
    def pts(self):
        """
        Turn a string into an ordered list of (x,y) tuples, the way God intended.
        """
        raw = self.pts_s.replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        return Territory.convert_points(
            [(float(raw[x * 2]), float(raw[(x * 2) + 1])) for x in range((len(raw) + 1) / 2)])

    def connects_to(self, t):
        return t in self.connects.all()

    def js_pts(self):
        return ",".join(["[%s,%s]" % (x[0], x[1]) for x in self.pts])

    def js_center(self):
        pre = (self.center_s.replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(','))
        return Territory.convert_pt((float(pre[0]) - 2, float(pre[1])))

    @property
    def has_unit(self):
        return Unit.live_units().filter(territory=self, alive=True).exists()

    @property
    def unit(self):
        return Unit.objects.get(territory=self, alive=True) if self.has_unit else None

    def order(self, turn=None):
        if not turn: turn = GameBoard.get_turn()
        p = Action.objects.filter(turn=turn, territory=self)
        return p[0] if p.exists() else None

    def __unicode__(self):
        return "[%s] %s <%s> (%s)" % (self.code, self.name, self.owner, self.has_unit)


class Faction(models.Model):
    code = models.CharField(max_length=ML, primary_key=True, unique=True)
    name = models.CharField(max_length=ML)
    color = models.CharField(max_length=ML, default='')

    def __unicode__(self):
        return "[%s] %s" % (self.code, self.name)


class Unit(models.Model):
    faction = models.ForeignKey('Faction')
    territory = models.ForeignKey('Territory')
    alive = models.BooleanField(default=True)
    special = models.CharField(max_length=ML, blank=True, default='')

    @classmethod
    def live_units(cls):
        return cls.objects.filter(alive=True)

    def order_for_unit(self, turn=None):
        if not turn: turn = GameBoard.get_turn()
        return self.territory.order(turn)

MOVE = 'Move'
SUPP = 'Supp'
HOLD = 'Hold'
SPEC = 'Spec'

types = (
    (MOVE, 'Move'),
    (SUPP, 'Support'),
    (HOLD, 'Hold'),
    (SPEC, 'Special')
    )

support_types = (
    (MOVE, 'Move'),
    (HOLD, 'Hold'),
    (SPEC, 'Special')
    )

E_UNHANDLED = -20
E_NOSUPPORTTARGET = -13
E_NOTYOURS = -12
E_NOTARGET = -11
E_NOUNIT = -10
F_NOSUPPDESTROY = -6
F_NODESTROY = -5
F_LOSE = -4
F_NOSWAP = -3
F_BOUNCE = -2
F_SUPPORTCUT = -1
V_PRELIM = 0
V_PENDING = 1
V_SUCCESS = 2

validation_phases = (
    (E_UNHANDLED, "Unimplemented"),
    (E_NOSUPPORTTARGET, "Support order without support destination"),
    (E_NOTYOURS, "Unit in territory not owned"),
    (E_NOTARGET, "Move order without destination"),
    (E_NOUNIT, "Unit disappeared"),
    (F_NOSUPPDESTROY, "Can't support the destruction of same-side unit"),
    (F_NODESTROY, "Can't destroy same-side unit"),
    (F_LOSE, "Lost conflict"),
    (F_NOSWAP, "Swap not allowed"),
    (F_BOUNCE, "Equal-strength combatants bounced"),
    (F_SUPPORTCUT, "Support cut"),
    (V_PRELIM, "Preliminary"),
    (V_PENDING, "Waiting on other moves"),
    (V_SUCCESS, "Succeeded"),
    )

def validation_str(v):
    for vs in validation_phases:
        if vs[0] == v: return vs[1]
    return "Unknown...?"


def done(v):
    return (v.validation_level < V_PRELIM) or (v.validation_level >= V_SUCCESS)


class Action(models.Model):
    faction = models.ForeignKey('Faction') #action faction, yeeeeaaaahh
    turn = models.IntegerField(blank=True, null=True)
    territory = models.ForeignKey('Territory', related_name='t_territory')
    type = models.CharField(max_length=ML, choices=types)
    target = models.ForeignKey('Territory', blank=True, null=True, related_name='t_move_to')
    special = models.CharField(max_length=ML, blank=True)
    support_type = models.CharField(max_length=ML, choices=types, blank=True)
    support_to = models.ForeignKey('Territory', blank=True, null=True, related_name='t_supp_to')
    validation_level = models.IntegerField(default=0, choices=validation_phases)

    @property
    def is_valid(self):
        return self.validation_level > 0

    @property
    def errored(self):
        return not self.is_valid

    def __unicode__(self):
        status = "{%s}" % validation_str(self.validation_level)#  if self.validation_level else ""
        initial = "%s %s %s %s" % (status, self.faction.code, self.territory.code, self.type)
        if self.type == MOVE:
            return "%s %s" % (initial, self.target.code)
        elif self.type == SUPP:
            if self.support_type == MOVE:
                return "%s %s %s %s" % (initial, self.target.code, self.support_type, self.support_to.code)
            else:
                return "%s %s %s" % (initial, self.target.code, self.support_type)
        else:
            return initial

    @classmethod
    def parse_move(cls, move, turn=None):
        """
        A simple parser for Diplomacy-esque move notation.
        # US A Supp B Move C
        # US A Hold
        # US A Move B
        # US A Spec
        """
        if not turn: turn = GameBoard.objects.get().turn
        tokens = move.split(' ')
        try:
            faction = Faction.objects.get(code=tokens[0])
            terr = Territory.objects.get(code=tokens[1])
        except:
            raise ValidationError("Bad parameters")
        type = tokens[2]
        if type == HOLD:
            return cls.objects.create(faction=faction, turn=turn,
                territory=terr,
                target=terr,
                type=HOLD)
        elif type == MOVE:
            to = Territory.objects.get(code=tokens[3])
            return cls.objects.create(faction=faction, turn=turn,
                territory=terr,
                type=MOVE,
                target=to)
        elif type == SUPP:
            tgt = Territory.objects.get(code=tokens[3])
            supp_type = tokens[4]
            if supp_type == HOLD:
                return cls.objects.create(faction=faction, turn=turn,
                    territory=terr,
                    type=SUPP,
                    support_type=HOLD,
                    target=tgt)
            elif supp_type == MOVE:
                dest = Territory.objects.get(code=tokens[5])
                return cls.objects.create(faction=faction, turn=turn,
                    territory=terr,
                    type=SUPP,
                    support_type=MOVE,
                    target=tgt,
                    support_to=dest
                )
        elif type == SPEC:
            special = tokens[3]
            return cls.objects.create(faction=faction, turn=turn,
                territory=terr,
                type=SPEC,
                special=special
            )
        else:
            raise RuntimeError('Unsupported move type.')

    def provides_support(self):
        """
        If a unit A attempts to move into a location with a unit B that's providing
        support, regardless of whether A's move succeeds, the support that B provides is cut.
        """
        return (self.type == SUPP and self.validation_level >= V_PRELIM
                and (not (self.support_type == MOVE and
                          self.target.has_unit and
                          self.support_to.has_unit and
                          (
                          self.support_to.unit.faction == self.target.unit.faction or #Can't support someone else in destroying themselves
                          self.support_to.unit.faction == self.faction)
                          # Can't support destroying yourself, even if it's someone else
            ))
                and (not Action.objects.filter(
            turn=self.turn,
            validation_level__gte=0,
            type=MOVE,
            target=self.territory
        ).exclude(territory=self.support_to).exclude(faction=self.faction).exists()))

    def supporters(self):
        supps = Action.objects.filter(
            turn=self.turn,
            type=SUPP,
            target=self.territory,
            support_type=self.type,
            validation_level__gte=V_PRELIM, # XXX check
        )
        if self.type == MOVE:
            supps = supps.filter(support_to=self.target)
        return filter(lambda x: x.provides_support(), supps)

    def validate(self, level):
        self.validation_level = level
        self.save()

    @property
    def support_strength(self):
        return len(self.supporters())

    def waiting_on(self):
        if not self.validation_level == V_PENDING: return None
        return Action.objects.get(turn=self.turn, territory=self.target, type=MOVE)

    def clean(self):
        if self.validation_level != V_PRELIM:
            # Already been validated
            return super(Action, self).clean()
        if not Unit.live_units().filter(territory=self.territory).exists():
            self.validation_level = E_NOUNIT
            # raise ValidationError('No unit in territory %s.' % self.territory.code)
        if not Unit.live_units().filter(territory=self.territory, faction=self.faction).exists():
            raise ValidationError('Unit in %s doesn\'t belong to %s.' % (self.territory.code, self.faction.code))

        if self.type == MOVE:
            if not self.target:
                raise ValidationError('Must select move target.')
            if not self.territory.connects_to(self.target):
                raise ValidationError('Territories %s and %s aren\'t adjacent.', self.territory.code, self.target.code)
        elif self.type == SUPP:
            if self.support_type and self.target:
                if not self.territory.connects_to(self.target):
                    raise ValidationError('Territory to support from must be adjacent.')
                if self.support_type == MOVE:
                    if not self.support_to:
                        raise ValidationError('Support moves must provide a valid destination.')
                    elif not self.territory.connects_to(self.support_to):
                        raise ValidationError('Territory to support to must be adjacent.')
        elif self.type == HOLD and not self.target:
            self.target = self.territory
        return super(Action, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Action, self).save(*args, **kwargs)


def resolve_conflict(opponents):
    """
    Resolves a multi-party conflict, sets validation level appropriately, and returns the winner.
    """

    if not opponents: return None
    elif len(opponents) == 1:
        opponents[0].validate(V_SUCCESS)
        return opponents[0]
    opps = sorted(opponents, key=lambda x: x.support_strength, reverse=True)
    if opps[0].faction == opps[1].faction:
        # This code should never get run, but it's here anyway.
        if opps[0].support_strength > opps[1].support_strength:
            map(lambda x: x.validate(F_NODESTROY),
                filter(lambda y: y.faction == opps[0].faction, opponents)
            )
    if opps[0].support_strength == opps[1].support_strength:
        for a in opponents:
            if a.validation_level >= V_PRELIM:
                if a.type == MOVE:
                    a.validate(F_BOUNCE)
                else:
                    a.validate(V_SUCCESS)
    else:
        opps[0].validate(V_SUCCESS)
        for a in opponents:
            if a == opps[0]: continue
            a.validate(F_LOSE)
    return opps[0]


class GameBoard(SingletonModel):
    turn = models.IntegerField(default=0)

    @classmethod
    def get_turn(cls):
        return cls.objects.get().turn

    def generate_holds(self):
        """
        Default action is to hold.
        """
        for u in Unit.live_units().all():
            if not Action.objects.filter(territory=u.territory, turn=self.turn).exists():
                a = Action.objects.create(territory=u.territory, type=HOLD, turn=self.turn, faction=u.faction)

                # here comes the big one

    def validate_all_moves(self):
        """
        Process all outstanding moves.
        """

        # First pass.

        def acts():
            return Action.objects.filter(turn=self.turn)

        if not acts().filter(validation_level=V_PRELIM):
            # Already processed...?
            return

        for a in acts().filter(validation_level=V_PRELIM):
            # Did we already fail or succeed elsewhere?
            if a.validation_level < V_PRELIM or a.validation_level == V_SUCCESS: continue
            if not Unit.live_units().filter(territory=a.territory, alive=True).exists():
                # Unit stopped existing for some reason.
                a.validate(E_NOUNIT)
                continue
            if a.type == SUPP:
                if a.provides_support():
                    a.validate(V_SUCCESS)
                elif a.support_to and a.support_to.has_unit and a.support_to.unit.faction and a.target.has_unit and (
                a.target.unit.faction == a.support_to.unit.faction or a.support_to.unit.faction == a.faction):
                    # Can't support the destruction of your own unit, or someone else's destruction of theirs
                    a.validate(F_NOSUPPDESTROY)
                else:
                    a.validate(F_SUPPORTCUT)
                continue
            if a.type == MOVE and acts().filter(target=a.territory, territory=a.target, type=MOVE).exists():
                # Swap detected.
                a.validate(F_NOSWAP)
                acts().get(target=a.territory, territory=a.target, type=MOVE).validate(F_NOSWAP)
                continue
            if not (Unit.live_units().filter(territory=a.target).exists() or acts().filter(target=a.target).exclude(
                id=a.id).exists()):
                # Unopposed move.  Just succeeds.
                a.validate(V_SUCCESS)
                for s in a.supporters(): s.validate(V_SUCCESS)
                continue
            if a.type == MOVE and a.target.has_unit and a.target.unit.faction == a.faction and not Action.objects.filter(
                turn=self.turn, territory=a.target, type=MOVE).exists():
                a.validate(F_NODESTROY)
                continue
            if a.type == MOVE and acts().filter(territory=a.target, type=MOVE).exists():
                # Opposed move into an occupied square with someone moving out.  Need to determine whether the move succeeds.
                a.validate(V_PENDING)
                continue
            else:
                if a.type == MOVE and Unit.live_units().filter(territory=a.target, faction=a.faction).exists():
                    a.validate(F_NODESTROY)
                    continue
                    # Opposed move into an empty or non-moving square,
                # or we're holding.  Resolve the conflict.
                actz = acts().filter(Q(Q(target=a.target) & ~Q(type=SUPP)) | Q(Q(territory=a.target) & ~Q(type=MOVE)))
                if actz:
                    resolve_conflict(actz)
                continue

                #            print "Unhandled case! %s" % a
                #            a.validate(E_UNHANDLED)

        # By this point nothing should be in V_PRELIM.
        unproc = acts().filter(validation_level=V_PRELIM).count()
        assert unproc == 0, "Still %s unprocessed moves!" % unproc

        # Second pass.

        def iterate():
            waiters = {}
            for w in acts().filter(validation_level=V_PENDING):
                # If the guy I was waiting on succeeded, I might succeed
                if done(w.waiting_on()):
                    if w.waiting_on().validation_level == V_SUCCESS:
                        # Guy moved; fight with anyone else trying to take this spot
                        resolve_conflict(acts().filter(type=MOVE, target=w.target))
                    else:
                        print "got here with %s" % w
                        # we fight with the guy whose move just failed
                        resolve_conflict(acts().filter(Q(Q(target=w.target) & Q(type=MOVE)) | Q(id=w.waiting_on().id)))


                # Detect cycles.
                # Everything just succeeds if 3+ units are involved.
                waiters[w.id] = w.waiting_on().id

                if w.waiting_on().id in waiters:
                    # Cycle?
                    # Position swaps always fail
                    if waiters[w.waiting_on().id] == w:
                        # We check this above too, but it's here for completeness.
                        w.validate(F_BOUNCE)
                        w.waiting_on().validate(F_BOUNCE)
                        continue
                    else:
                        found = False
                        x = w.waiting_on()
                        # Make sure we're in a cycle.
                        while x.id in waiters:
                            if x.id == w.id:
                                found = True
                                break
                            x = x.waiting_on()
                        if found:
                            x = w.waiting_on()
                            while x.id in waiters:
                                next = x.waiting_on()
                                x.validate(V_SUCCESS)
                                if x.id == w.id:
                                    break
                                x = next
            return len(waiters)

        it = 1
        for i in range(len(acts())):
            it = iterate()
            if it == 0: break

        assert it == 0, "Iteration limit reached; failed to find solution"
        bad_acts = acts().filter(Q(validation_level__lt=V_SUCCESS) & Q(validation_level__gte=V_PRELIM))
        assert len(bad_acts) == 0, "Some moves didn't succeed or fail"

    def process_moves(self):
        def acts(): return Action.objects.filter(turn=self.turn)

        # No unprocessed moves
        assert acts().filter(validation_level__lt=V_SUCCESS, validation_level__gte=V_PRELIM).count() == 0

        successes = acts().filter(validation_level=V_SUCCESS)
        for a in successes.filter(type=MOVE):
            #assert(successes.filter(target=a.target).exclude(a))
            u = Unit.live_units().filter(territory=a.territory, faction=a.faction)[0]
            u.territory = a.target
            u.save()
            u.territory.owner = u.faction
            u.territory.save()

        bad_us = Unit.live_units().exclude(territory__owner__code=F('faction'))
        for u in bad_us:
            u.alive = False
            u.save()

    def execute_turn(self, debug=False):
        if debug:
            self.print_board()

        self.generate_holds()
        self.validate_all_moves()
        self.process_moves()
        self.turn += 1
        self.save()

        if debug:
            self.print_turn()
            self.print_board()

    def print_turn(self):
        for a in Action.objects.filter(turn=self.turn - 1): print a

    def print_board(self):
        for t in Territory.objects.all(): print t
