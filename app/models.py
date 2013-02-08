# coding=utf-8
import hashlib

from django.db import models
from django.forms import ModelForm, Textarea
from datetime import datetime

ML = 256

class ConsortiumApp(models.Model):
    name = models.CharField(max_length=ML)
    email = models.EmailField(max_length=ML)
    phone = models.CharField(max_length=ML, blank=True)
    do_not_call = models.TextField(blank=True, verbose_name="Times not to call (or other considerations)")
    time_constraints = models.TextField(blank=True,
        verbose_name="Are there any significant constraints on your time during game?")
    new_player = models.TextField(blank=True,
        verbose_name="If you are a new(ish) player, where might we know you from?")
    genders = models.TextField(blank=True, verbose_name="What genders are you willing to play?  Prefer to play?")
    wargame_ok = models.TextField(blank=True,
        verbose_name="Do you want to participate in a wargame based on Diplomacy?")
    typecast = models.TextField(blank=True, verbose_name="If you have one, what is your typecast?  Do you want it?")
    punts = models.TextField(blank=True, verbose_name="Is there anything that would make you punt game?")
    how_cast = models.TextField(blank=True, verbose_name="Tell us how to cast you.")
    disc_guns = models.IntegerField(blank=True, null=True, default=0,
        verbose_name="How many working (or repairable) disc guns do you own?")
    device = models.TextField(blank=True,
        verbose_name="Do you have a smartphone, tablet, and/or laptop you would use in game, and if so, what kind(s)?")
    sms_ok = models.TextField(blank=True, verbose_name="Are you OK with receiving (infrequent) SMS alerts?")
    zephyr = models.TextField(blank=True, verbose_name="Are you generally reachable on zephyr?")
    mechanics = models.TextField(blank=True,
    verbose_name="Are there any types of plots or mechanics you particularly like or dislike?")

    spy_plots = models.TextField(blank=True,
        verbose_name="Briefly describe any 'spy plots' you've played before, and how you liked them.")
    public_secret = models.TextField(blank=True,
        verbose_name="Do you prefer public authority, secret authority, or working under others?")
    motivations = models.TextField(blank=True,
        verbose_name="Do you want motivations like idealism, altruism, fanaticism, extreme views, etc.?")
    die_for = models.TextField(blank=True,
        verbose_name="What percentage of your goals and motivations do you want to be willing to die for?")
    teammate = models.TextField(blank=True,
        verbose_name="You have a teammate.  You don't know who they are, and have no mechanic for finding them. "+\
                     " You expect others want to find and kill you both.  You need your teammate's help."+\
                     " How might you proceed?")
    campus = models.TextField(blank=True,
        verbose_name="You need to search a portion of campus for something.  Whom do you take with you, and why?")
    changing_minds = models.TextField(blank=True,
        verbose_name="What is your preferred method of changing people's minds?")
    what_else = models.TextField(blank=True, verbose_name="What else should we know?")

    saved_on = models.DateTimeField(blank=True, null=True)
    apped_on = models.DateTimeField(blank=True, null=True)

    submitted = models.BooleanField(default=False)
    app_id = models.CharField(blank=True, max_length=ML)

    def __unicode__(self):
        return "%s <%s> %s" % (self.name, self.email,
                               "Final" if self.submitted else "Temp")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.app_id = hashlib.sha1(str(datetime.now())).hexdigest()[:6]
        return super(ConsortiumApp, self).save(*args, **kwargs)


class AppForm(ModelForm):
    class Meta:
        model = ConsortiumApp
        large = {'cols': None, 'rows': 6}

        attrs = {'cols': None, 'rows': 4}
        small = {'cols': None, 'rows': 2}
        tiny = {'cols': None, 'rows': 1}

        exclude = ('saved_on', 'apped_on', 'submitted', 'app_id')
        widgets = {
            "do_not_call": Textarea(attrs=small),
            "time_constraints": Textarea(attrs=attrs),
            "new_player": Textarea(attrs=attrs),
            "genders": Textarea(attrs=small),
            "device": Textarea(attrs=small),
            "sms_ok": Textarea(attrs=small),
            "zephyr": Textarea(attrs=small),
            "wargame_ok": Textarea(attrs=small),
            "typecast": Textarea(attrs=attrs),
            "punts": Textarea(attrs=attrs),
            "how_cast": Textarea(attrs=attrs),
            "spy_plots": Textarea(attrs=attrs),
            "public_secret": Textarea(attrs=attrs),
            "motivations": Textarea(attrs=attrs),
            "die_for": Textarea(attrs=attrs),
            "teammate": Textarea(attrs=large),
            "campus": Textarea(attrs=large),
            "changing_minds": Textarea(attrs=large),
            "what_else": Textarea(attrs=attrs),
        }

    explanations = {
        "do_not_call": "This will be specified on the playerlist (unless you tell us not to). The GMs are unlikely to call you unless there's a problem.",
        "time_constraints": "If you can't play certain days, aren't available at certain times, or have pre-existing commitments, we need to know.<br />We will have a few time-constrained parts available.  If you can only make the first weekend, for example, we may still be able to cast you. Apply anyway!",
        "new_player": "Don't assume we know who you are. If there's any doubt whatsoever, tell us who you are, especially if you're an MIT underclassman.",
        "device": "We're trying to gauge the prevalence of these devices in the Guild playerbase. While this game will have a webapp, we have attempted to minimize the amount of time you'll need to spend on it.",
        "sms_ok": "We won't spam you. If we use this at all, it'll be for things you need to know, and it'll all be viewable in some other way. If you have some constraint ('nights only', 'less than 5 per day is fine'), tell us.",
        "zephyr": "Same as above -- trying to gauge how many use it.",
        "disc_guns": "The Guild has a very limited supply of disc guns. "
                     "We expect to be able to provide everyone with one, but if we get enough loans or donations, we may be able to bump that up.  If you have your own, tell us.",
        "wargame_ok": "The rules will be simplified and geared towards maximum human interaction.",
        "typecast": """If you're an old hand at Guild games, we likely have an image in our heads of the type of
    characters you play, and there's a good chance we'll gravitate towards roles
     like that for you.  Here's your opportunity to tell us whether you want that, and what your view of your
     own typecast is.<br/>
                    If you don't know what a typecast is, don't worry about it.""",
        "punts": "",
        "how_cast": "If you must be cast in a certain way, if some of your answers are more important than others, or if you have the perfect role in mind, tell us.",
        "mechanics": "Examples include ",
        "spy_plots": "This will help us match you with a good set of plots. If you've never played a spy plot before (or think you haven't), tell us that, and perhaps what spy plots you might enjoy.<br />What's a spy plot? Broadly speaking, it's an opposed plot conducted under conditions of secrecy and uncertainty. What that means is up to you.",
        "public_secret": """'Public authority' might be the UN Secretary General,
the chief of police, or the Pope* in a game full of Catholics.  'Secret
authority' might be the head of the secret police, the commander of a black-ops
infiltration team, or an evil wizard with a group of brainwashed thralls.*
'Working under others' might be an enforcer, assassin, researcher, agent, trusted
lieutenant, or Judas.<br />
As a very general rule of thumb, high-ranking people rely on those loyal to them to get stuff done.
For example, a professor might have lots of research plots but a zero research stat, relying on her
grad students (all of whom have high research stats and plots of their own) to get research done.<br />
* Neither the Pope nor evil wizards appear in this game.
""",
        "motivations": "Some characters might be unswervingly devoted to particular causes, groups, countries, religions,"
                       " ethical viewpoints, and so on. Others might be more ideologically flexible. What suits you?",
        "die_for": "How strong do you wish your motivations to be? Not every character is willing to put it all on the "
                   "line for King and country. Maybe only certain situations would make you risk your life -- which ones?",
        "teammate": "You may encounter plots with no obvious mechanical support, some of which may be opposed by hidden"
                    " hostile forces. You'll have to apply cunning, guile, and a healthy dose of paranoia. How do you thread the needle?",
        "campus": "There are a number of reasons you might bring someone with you. Maybe you need them. Maybe they need you. "
                  "Maybe you have other motivations. Use your imagination.",
        "changing_minds": "Many plots will require you to convince people of something, whether it be to"
                          " trust you, to give you something, or to take or refrain from an action. There are"
                          " many ways of accomplishing this. What are your preferred ways?",
        "what_else": "Here's your opportunity to tell us things we should know but didn't ask above.",

    }