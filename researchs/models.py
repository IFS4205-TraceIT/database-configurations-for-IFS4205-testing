from django.db import models

class Researchers(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = 'researchers'

class Researchdata(models.Model):
    dob = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    postal_code = models.TextField(blank=True)
    list_of_vaccines = models.TextField(blank=True)
    last_close_contact = models.TextField(blank=True)
    last_infected_date = models.TextField(blank=True)
    total_infection = models.BigIntegerField(blank=True, null=True)
    total_close_contact_as_infected = models.BigIntegerField(blank=True, null=True)
    total_close_contact_with_infected = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'researchdata'