# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid


class Buildingaccess(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    building = models.ForeignKey('Buildings', on_delete=models.CASCADE)
    access_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'buildingaccess'
        unique_together = (('user', 'building', 'access_timestamp'),)


class Buildings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    location = models.IntegerField()

    class Meta:
        db_table = 'buildings'


class Closecontacts(models.Model):
    infected_user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name="infected_user")
    contacted_user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name="contacted_user")
    contact_timestamp = models.DateTimeField()
    rssi = models.DecimalField(max_digits=10, decimal_places=2)
    infectionhistory = models.ForeignKey('Infectionhistory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'closecontacts'


class Contacttracers(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = 'contacttracers'


class Infectionhistory(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    recorded_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'infectionhistory'
        unique_together = (('user', 'recorded_timestamp'),)


class Notifications(models.Model):
    due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    tracer = models.ForeignKey(Contacttracers, on_delete=models.SET_NULL, blank=True, null=True)
    infection = models.OneToOneField(Infectionhistory, on_delete=models.CASCADE, primary_key = True)
    uploaded_status = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nric = models.TextField(unique=True)
    name = models.TextField()
    dob = models.DateField()
    email = models.TextField(blank=True)
    phone = models.TextField()
    gender = models.TextField()
    address = models.TextField()
    postal_code = models.TextField()

    class Meta:
        db_table = 'users'


class Vaccinationhistory(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    vaccination = models.ForeignKey('Vaccinationtypes', on_delete=models.CASCADE)
    date_taken = models.DateField()

    class Meta:
        db_table = 'vaccinationhistory'
        unique_together = (('user', 'vaccination', 'date_taken'),)


class Vaccinationtypes(models.Model):
    name = models.TextField()
    start_date = models.DateField()

    class Meta:
        db_table = 'vaccinationtypes'
