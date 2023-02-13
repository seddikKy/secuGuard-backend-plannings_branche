import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import calendar

# Calendar settings
calendar.setfirstweekday(calendar.SUNDAY)
HOLIDAY_DAY_INDEX = 8
WEEK_DAYS_MAPPING = (
    (calendar.MONDAY, 'Lundi'),
    (calendar.TUESDAY, 'Mardi'),
    (calendar.WEDNESDAY, 'Mercredi'),
    (calendar.THURSDAY, 'Jeudi'),
    (calendar.FRIDAY, 'Vendredi'),
    (calendar.SATURDAY, 'Samedi'),
    (calendar.SUNDAY, 'Dimanche'),
    (HOLIDAY_DAY_INDEX, 'Jours fériés'))


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Créé')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modifié')

    class Meta:
        abstract = True


class Enterprise(TimestampModel):
    designation = models.CharField(max_length=255, verbose_name='Nom de l\'entreprise')

    class Meta:
        verbose_name = 'Entreprise'

    def __str__(self):
        return self.designation


class Site(TimestampModel):
    designation = models.CharField(max_length=255, verbose_name='Nom du site')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation + f" ({self.enterprise.designation})"


class Zone(TimestampModel):
    PLAN_STATES = (
        (1, 'Brouillon'),
        (2, 'Validé'),
    )
    designation = models.CharField(max_length=255, verbose_name='Nom de la zone')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site')
    plan_state = models.IntegerField(choices=PLAN_STATES, default=PLAN_STATES[0][0], editable=False)

    def __str__(self):
        return self.designation + f" ({self.site.designation} - {self.site.enterprise.designation})"

    def validate_plan(self):
        self.plan_state = self.PLAN_STATES[1][0]
        self.save()

    def invalidate_plan(self):
        self.plan_state = self.PLAN_STATES[0][0]
        self.save()

    def create_planned_checkpoints(self):
        current_datetime = timezone.now()
        today = current_datetime.date()
        today_weekday_index = calendar.weekday(today.year, today.month, today.day)

        # Update check plan
        future_plans = PatrolLog.objects.filter(
            check_datetime__gte=current_datetime,
            tag__zone=self
        )
        future_plans.delete()

        related_tags = Tag.objects.filter(zone=self)  # Tags assigned to the current Zone
        zone_planning = Planning.objects.filter(zone=self)

        for plan in zone_planning:
            if plan.selected_day_index != HOLIDAY_DAY_INDEX:  # holidays index
                for tag in related_tags:
                    if today_weekday_index <= plan.selected_day_index:
                        check_date = today + datetime.timedelta(plan.selected_day_index - today_weekday_index)
                    else:
                        check_date = today + datetime.timedelta(plan.selected_day_index)
                    check_time = plan.patrol_check_time
                    check_datetime = datetime.datetime.combine(check_date, check_time)
                    PatrolLog.objects.create(
                        tag=tag,
                        check_tolerance=plan.tolerated_time,
                        check_datetime=check_datetime,
                        planning=plan
                    )
                    # todo if holidays ?

    def do_action(self, action, user):
        if action == 'confirm':
            self.create_planned_checkpoints()
            self.validate_plan()
        elif action == 'reopen':
            self.invalidate_plan()


class Employee(TimestampModel):
    designation = models.CharField(max_length=255, verbose_name='Nom de l\'employée')
    code_pin = models.CharField(max_length=6, verbose_name='Code PIN')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    code_pin = models.CharField(max_length=255, verbose_name='Code PIN', null=True)

    class Meta:
        verbose_name = 'Employée'

    def __str__(self):
        return self.designation


class Tag(TimestampModel):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='Zone')
    code_nfc = models.CharField(max_length=255, verbose_name='code NFC')
    designation = models.CharField(max_length=255, verbose_name='Nom du TAG')
    order = models.PositiveIntegerField(verbose_name='Ordre', blank=True, null=True)
    observation = models.CharField(max_length=255, verbose_name='Observation')

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return self.designation
    



class Holiday(TimestampModel):
    designation = models.CharField(max_length=100, verbose_name='Désignation')
    date = models.DateField(verbose_name='Date')



class Planning(TimestampModel):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='Zone', editable=False)
    selected_day_index = models.IntegerField(choices=WEEK_DAYS_MAPPING, editable=False)
    patrol_check_time = models.TimeField(auto_now=False, auto_now_add=False,
                                         verbose_name='Heure de début de la tournée')
    tolerated_time = models.DurationField(verbose_name='Temps toléré')
    observation = models.TextField(verbose_name='Observation', blank=True, null=True)

    def __str__(self):
        return f"Check time : {self.patrol_check_time} (+{self.tolerated_time})"

    def save(self, *args, **kwargs):
        if self.zone.plan_state != 1:
            raise ValidationError('Vous ne pouvez pas modifier un planning valider !')
        else:
            super().save(args, kwargs)

class PatrolLog(TimestampModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Tag')
    audio_path = models.CharField(max_length=255, verbose_name='Lien de la memo-vocale', blank=True, null=True)
    image_path = models.ImageField(null=True, blank=True, upload_to="images/")
    description_anomaly = models.TextField(verbose_name='Anomalie', blank=True, null=True)
    is_checked = models.BooleanField(verbose_name='tag visité', default=False)
    check_datetime = models.DateTimeField('Date / Heure prévue ')
    check_tolerance = models.DurationField('Tolérance')
    checked_datetime = models.DateTimeField(verbose_name='Date / Heure de passage', blank=True, null=True,
                                            editable=False)
    checked_by = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                   verbose_name=('Controlé par'),
                                   null=True, blank=True, editable=False)
    planning = models.ForeignKey(Planning, on_delete=models.SET_NULL,null=True, verbose_name='Planning')

    class Meta:
        verbose_name = 'Journal des tournées'

    def __str__(self):
        return self.tag.designation
