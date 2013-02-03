from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from singleton_models.models import SingletonModel

ML = 256

class GameBoard(SingletonModel):
    turn = models.IntegerField(default=0)

    # here comes the big one
    def execute_turn(self):
        """
        Process all outstanding moves and populate new game state.
        """
        # For now, pretend all moves succeed.
        actions = Action.objects.filter(validation_level__gte=0, turn=self.turn)
        for a in actions:
            if a.type == MOVE:
                if not Unit.objects.filter(territory=a.territory).exists():
                    a.validation_level = E_NOUNIT
                    continue
                    # OK, move the unit

class Territory(models.Model):
    code = models.CharField(max_length=ML, primary_key=True, unique=True)
    name = models.CharField(max_length=ML)
    pts_s = models.CharField(max_length=ML * 2, blank=True)
    connects = models.ManyToManyField('Territory', related_name='t_connects', symmetrical=True)
    center_s = models.CharField(max_length=ML, blank=True)
    owner = models.ForeignKey('Faction', null=True, blank=True)

    @property
    def pts(self):
        """
        Turn a string into an ordered list of (x,y) tuples, the way God intended.
        """
        raw = self.pts_s.replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        return [(float(raw[x * 2]), float(raw[(x * 2) + 1])) for x in range((len(raw) + 1) / 2)]

    def connects_to(self, t):
        return t in self.connects.all()

    @property
    def has_unit(self):
        return Unit.objects.filter(territory=self, alive=True).exists()

    def __unicode__(self):
        return "[%s] %s <%s>" % (self.code, self.name, self.owner)


class Faction(models.Model):
    code = models.CharField(max_length=ML, primary_key=True, unique=True)
    name = models.CharField(max_length=ML)

    def __unicode__(self):
        return "[%s] %s" % (self.code, self.name)


class Unit(models.Model):
    faction = models.ForeignKey('Faction')
    territory = models.ForeignKey('Territory')
    alive = models.BooleanField(default=True)
    special = models.CharField(max_length=ML, blank=True, default='')

MOVE = 'Move'
SUPP = 'Supp'
HOLD = 'Hold'
SPEC = 'Spec'

move_types = (
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

E_NOUNIT = -1
V_PRELIM = 0
V_SUCCESS = 1

validation_phases = (
    (E_NOUNIT, "No unit present"),
    (V_PRELIM, "Preliminary"),
    (V_SUCCESS, "Successful"),
    )

class Action(models.Model):
    turn = models.IntegerField(blank=True, null=True)
    territory = models.ForeignKey('Territory', related_name='t_territory')
    type = models.CharField(max_length=ML, choices=move_types)
    target = models.ForeignKey('Territory', blank=True, null=True, related_name='t_move_to')
    special = models.CharField(max_length=ML, blank=True)
    support_type = models.CharField(max_length=ML, choices=move_types, blank=True)
    support_to = models.ForeignKey('Territory', blank=True, null=True, related_name='t_supp_to')
    validation_level = models.IntegerField(default=0, choices=validation_phases)

    @property
    def is_valid(self):
        return self.validation_level > 0

    @property
    def errored(self):
        return not self.is_valid

    def __unicode__(self):
        initial = "%s %s" % (self.territory.code, self.type)
        if self.type == MOVE:
            return "%s %s" % (initial, self.target.code)
        elif self.type == SUPP:
            if self.support_type == MOVE:
                return "%s %s %s %s" % (initial, self.target.code, self.support_type, self.support_to)
            else:
                return "%s %s %s" % (initial, self.target.code, self.support_type)
        else:
            return initial

    @classmethod
    def parse_move(cls, move, turn=GameBoard.objects.get().turn):
        """
        A simple parser for Diplomacy-esque move notation.
        # A Supp B Move C
        # A Hold
        # A Move B
        # A Spec
        """
        tokens = move.split(' ')
        terr = Territory.objects.get(code=tokens[0])
        type = tokens[1]
        if type == HOLD:
            return cls.objects.create(turn=turn,
                territory=terr,
                move_type=HOLD)
        elif type == MOVE:
            to = Territory.objects.get(code=tokens[2])
            return cls.objects.create(turn=turn,
                territory=terr,
                move_type=MOVE,
                target=to)
        elif type == SUPP:
            tgt = Territory.objects.get(code=tokens[2])
            supp_type = tokens[3]
            if supp_type == HOLD:
                return cls.objects.create(turn=turn,
                    territory=terr,
                    move_type=SUPP,
                    support_type=HOLD,
                    target=tgt)
            elif supp_type == MOVE:
                dest = Territory.objects.get(code=tokens[4])
                return cls.objects.create(turn=turn,
                    territory=terr,
                    move_type=SUPP,
                    support_type=MOVE,
                    target=tgt,
                    support_to=dest
                )
        elif type == SPEC:
            special = tokens[2]
            return cls.objects.create(turn=turn,
                territory=terr,
                move_type=SPEC,
                special=special
            )
        else:
            raise RuntimeError('Unsupported move type.')

    def support_strength(self):
        supporters =  Action.objects.filter(
            turn = self.turn,
            type = SUPP,
            target = self.territory,
            support_type = self.type,
            validation_level__gte=V_PRELIM, # XXX check
        )
        if self.type == MOVE:
            supporters = supporters.filter(support_to=self.target)


    def clean(self):
        if self.type == MOVE:
            if not self.target:
                raise ValidationError('Must select move target.')
            if not self.territory.connects_to(self.target):
                raise ValidationError('Those territories aren\'t adjacent.')
        elif self.type == SUPP:
            if self.support_type and self.target:
                if not self.territory.connects_to(self.target):
                    raise ValidationError('Territory to support from must be adjacent.')
                if self.support_type == MOVE:
                    if not self.support_to:
                        raise ValidationError('Support moves must provide a valid destination.')
                    elif not self.territory.connects_to(self.support_to):
                        raise ValidationError('Territory to support to must be adjacent.')

