# coding=utf-8
import hashlib

from django.db import models
from django.forms import ModelForm, Textarea

ML=256

class ConsortiumApp(models.Model):
    name = models.CharField(max_length=ML)
    email = models.EmailField(max_length=ML)
    phone = models.CharField(max_length=ML, blank=True)
    do_not_call = models.TextField(blank=True, verbose_name="Times not to call (or other considerations)")
    time_constraints = models.TextField(blank=True, verbose_name="Do you have significant constraints on your time during game?")
    new_player = models.TextField(blank=True, verbose_name="If you are a new(ish) player, where might we know you from?")
    genders = models.TextField(blank=True, verbose_name="What genders are you willing to play?  Prefer to play?")
    sms_ok = models.TextField(blank=True, verbose_name="Are you OK with receiving (infrequent) SMS alerts?")
    wargame_ok = models.TextField(blank=True, verbose_name="Do you want to participate in a wargame based on Diplomacy?")
    typecast = models.TextField(blank=True, verbose_name="If you have one, what is your typecast?  Do you want it?")
    punts = models.TextField(blank=True, verbose_name="Is there anything that would make you punt game?")
    how_cast = models.TextField(blank=True, verbose_name="Tell us how to cast you.")
    spy_plots = models.TextField(blank=True, verbose_name="Briefly describe any 'spy plots' you've played before, and how you liked them.")
    public_secret = models.TextField(blank=True, verbose_name="Do you prefer public authority, secret authority, or working under others?")
    motivations = models.TextField(blank=True, verbose_name="Do you want motivations like idealism, altruism, fanaticism, extreme views, etc.?")
    die_for = models.TextField(blank=True, verbose_name="What percentage of your goals and motivations do you want to be willing to die for?")
    teammate = models.TextField(blank=True, verbose_name="You have a teammate.  You don't know who they are, and have no mechanic for finding them.  You expect others want to find and kill you both.  You need your teammate's help.  How might you proceed?")
    campus = models.TextField(blank=True, verbose_name="You need to search a portion of campus for something.  Who do you take with you, and why?")
    changing_minds = models.TextField(blank=True, verbose_name="What is your preferred method of changing people's minds?")
    what_else = models.TextField(blank=True, verbose_name="What else should we know?")

    saved_on = models.DateTimeField(blank=True)
    apped_on = models.DateTimeField(blank=True)

    submitted = models.BooleanField(default=False)
    app_id = models.CharField(blank=True, max_length=ML, editable=False)

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.app_id = hashlib.sha1("app_"+self.email).hexdigest()[:6]
        return super(ConsortiumApp, self).save(*args, **kwargs)

class AppForm(ModelForm):
    class Meta:
        model = ConsortiumApp
        attrs = {'cols':40, 'rows':4}
        small = {'cols':40, 'rows':2}

        widgets = {

                "do_not_call": Textarea(attrs=small),
                "time_constraints": Textarea(attrs=attrs),
                "new_player": Textarea(attrs=attrs),
                "genders": Textarea(attrs=small),
                "sms_ok": Textarea(attrs=small),
                "wargame_ok": Textarea(attrs=small),
                "typecast": Textarea(attrs=attrs),
                "punts": Textarea(attrs=attrs),
                "how_cast": Textarea(attrs=attrs),
                "spy_plots": Textarea(attrs=attrs),
                "public_secret": Textarea(attrs=attrs),
                "motivations": Textarea(attrs=attrs),
                "die_for": Textarea(attrs=attrs),
                "teammate": Textarea(attrs=attrs),
                "campus": Textarea(attrs=attrs),
                "changing_minds": Textarea(attrs=attrs),
                "what_else": Textarea(attrs=attrs),

        }