from django.db import models
from datetime import datetime


# Create your models here.
class Devices(models.Model):
    device_id = models.AutoField(primary_key=True, null=False, blank=False)
    device_address = models.TextField(db_column='device_address', blank=False, null=False)
    device_name = models.TextField(db_column='device_name', blank=True)
    device_description = models.TextField(db_column='device_description', default='')
    registration_time = models.DateTimeField(db_column='registration_time', default=datetime.now())
    class Meta:
        managed = True
        db_table = 'devices'

class Data(models.Model):
    record_id = models.AutoField(primary_key=True, null=False)
    device_id = models.ForeignKey(Devices, on_delete=models.CASCADE)
    rssi = models.IntegerField(db_column='rssi',null=False,default=0)
    timestamp = models.DateTimeField(db_column='timestamp', default=datetime.now())
    class Meta:
        managed = True
        db_table = 'data'
        ordering = ['-timestamp']


class DevicesGateway(models.Model):
    device_id = models.AutoField(primary_key=True, null=False, blank=False)
    device_name = models.TextField(db_column='device_name', blank=True)
    device_description = models.TextField(db_column='device_description', default='')
    registration_time = models.DateTimeField(db_column='registration_time', default=datetime.now())

    class Meta:
        managed = True
        db_table = 'devicesgateway'

class DataGateway(models.Model):
    record_id = models.AutoField(primary_key=True, null=False)
    device_id = models.ForeignKey(DevicesGateway, on_delete=models.CASCADE)
    rssi = models.FloatField(db_column='rssi', null=False, default=0)
    rssitb = models.FloatField(db_column='rssitb', null=False, default=0)
    deltaA = models.FloatField(db_column='deltaA',null=False,default=0)
    timestamp = models.DateTimeField(db_column='timestamp', default=datetime.now())

    class Meta:
        managed = True
        db_table = 'datagateway'
        ordering = ['-timestamp']