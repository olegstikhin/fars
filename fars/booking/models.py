from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _('Only alphanumeric characters are allowed.'))


class Bookable(models.Model):
    # unique ID string used in the URL
    id_str = models.CharField(max_length=32, unique=True, validators=[alphanumeric])
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    icon = models.CharField(max_length=32, default='tf.svg')
    public = models.BooleanField(default=False)
    # How far in the future bookings are allowed (zero means no limit)
    forward_limit_days = models.PositiveIntegerField(default = 0)
    # How long bookings are allowed to be (zero means no limit)
    length_limit_hours = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Bookable)
def create_bookable_group(sender, instance, **kwargs):
    g = Group(name="{}_admin".format(instance.id_str))
    g.save()


# class TimeSlot(models.Model):
#     start = models.CharField(null=False)
#     end = models.CharField(max_length=8, null=False)
#     bookable = models.ForeignKey(max_length=8, Bookable, on_delete=models.CASCADE)


class Booking(models.Model):
    bookable = models.ForeignKey(Bookable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"))
    comment = models.CharField(_("comment"), max_length=128)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        return "{}, {}".format(self.comment, self.start.strftime("%Y-%m-%d %H:%M"))
