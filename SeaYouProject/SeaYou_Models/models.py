# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Route(models.Model):
    routeid = models.AutoField(db_column='RouteId', primary_key=True)  # Field name made lowercase.
    visit = models.CharField(db_column='Visit', max_length=7, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    journey = models.IntegerField(db_column='Journey')  # Field name made lowercase.
    shipid = models.ForeignKey('Ship', models.DO_NOTHING, db_column='ShipId')  # Field name made lowercase.
    routecategoryid = models.ForeignKey('Routecategory', models.DO_NOTHING, db_column='RouteCategoryId')  # Field name made lowercase.
    routestarteddt = models.DateTimeField(db_column='RouteStartedDT')  # Field name made lowercase.
    waypointid = models.ForeignKey('Waypoint', models.DO_NOTHING, db_column='WaypointId')  # Field name made lowercase.
    waypointdt = models.DateTimeField(db_column='WaypointDT')  # Field name made lowercase.
    dockeddt = models.DateTimeField(db_column='DockedDT', blank=True, null=True)  # Field name made lowercase.
    zonetoid = models.ForeignKey('Zoneto', models.DO_NOTHING, db_column='ZoneToId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Route'


class Routecategory(models.Model):
    routecategoryid = models.AutoField(db_column='RouteCategoryId', primary_key=True)  # Field name made lowercase.
    routecategoryname = models.CharField(db_column='RouteCategoryName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RouteCategory'


class Ship(models.Model):
    shipid = models.AutoField(db_column='ShipId', primary_key=True)  # Field name made lowercase.
    shipname = models.CharField(db_column='ShipName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    imo = models.IntegerField(db_column='IMO')  # Field name made lowercase.
    max_length = models.DecimalField(db_column='Max_Length', max_digits=8, decimal_places=2)  # Field name made lowercase.
    max_width = models.DecimalField(db_column='Max_Width', max_digits=8, decimal_places=2)  # Field name made lowercase.
    max_draft = models.DecimalField(db_column='Max_Draft', max_digits=8, decimal_places=2)  # Field name made lowercase.
    operationaldraft = models.DecimalField(db_column='OperationalDraft', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ship'
        unique_together = (('shipname', 'imo'),)


class Waypoint(models.Model):
    waypointid = models.AutoField(db_column='WaypointId', primary_key=True)  # Field name made lowercase.
    waypointname = models.CharField(db_column='WaypointName', unique=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    waypointdescription = models.TextField(db_column='WaypointDescription', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    waypointlongitude = models.FloatField(db_column='WaypointLongitude', blank=True, null=True)  # Field name made lowercase.
    waypointlatitude = models.FloatField(db_column='WaypointLatitude', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Waypoint'


class Zoneto(models.Model):
    zonetoid = models.AutoField(db_column='ZoneToId', primary_key=True)  # Field name made lowercase.
    zonetoname = models.CharField(db_column='ZoneToName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZoneTo'

class AccessToken(models.Model):
    token = models.CharField(max_length=2000)
    exp_date = models.DateTimeField()


class WeatherCache(models.Model):
    cashed_weather_data = models.TextField(db_column='CashedWeatherData', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    updated_at = models.DateTimeField()


class ETACache(models.Model):
    name = models.CharField(db_column='Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', default='port')
    cashed_eta_data = models.TextField(db_column='CashedETAData', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    updated_at = models.DateTimeField()

# class WeatherStation(models.Model):
#     id = models.AutoField(db_column='id', primary_key=True)
#     code_name = models.CharField(db_column='CodeName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     full_name = models.CharField(db_column='FullName',max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     longitude