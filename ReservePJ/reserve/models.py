from register.models import User
from django.db import models

from django.utils import timezone
import datetime

def reserve_validate(value):
    print('A')

# Create your models here.
class office_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=150,verbose_name='カテゴリ名')

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_id']
        verbose_name = 'オフィスカテゴリー'
        verbose_name_plural = 'オフィスカテゴリー'

class Floor(models.Model):
    floor_id = models.AutoField( primary_key=True)
    floor_name = models.CharField(max_length=150,verbose_name='フロア名')

    def __str__(self):
        return self.floor_name

    class Meta:
        ordering = ['floor_id']
        verbose_name = 'フロア'
        verbose_name_plural = 'フロア'
        
class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    room_id = models.AutoField( primary_key=True)
    room_name = models.CharField(max_length=150,verbose_name='ルーム名')

    def __str__(self):
        return str(self.floor) + '-' + self.room_name

    def only_name(self):
        return self.room_name

    class Meta:
        ordering = ['floor_id','room_id']
        verbose_name = 'ルーム'
        verbose_name_plural = 'ルーム'

class Seats(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    seats_id = models.AutoField(primary_key=True)
    seats_name = models.CharField(max_length=150,verbose_name='座席名')

    def __str__(self):
        return str(self.room) + '-' + self.seats_name

    def only_name(self):
        return self.seats_name

    class Meta:
        ordering = ['room_id','seats_id']
        verbose_name = '座席'
        verbose_name_plural = '座席'

class Reserve(models.Model):
    seats = models.ForeignKey(Seats, on_delete=models.CASCADE)
    reserve_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserve_id = models.AutoField(primary_key=True)
    reserve_flg = models.BooleanField()
    reserve_day = models.DateField()
    #予約している日時
    reserve_start_time = models.TimeField()
    reserve_end_time = models.TimeField()
    #予約開始時間
    reserve_hour_zone = models.IntegerField()
    ##予約した時間帯
    #reserve_start_time = models.TimeField()
    #予約した時間
    reserve_time = models.DateTimeField(auto_now_add=True)
    #予約作業をした日時（CREATED_TIMEと同機能）
    change_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return str(self.reserve_user) + '_' + str(self.seats) + '_' + self.reserve_day.strftime("%Y/%m/%d")

    #def __str__(self):
    #   return str(self.reserve_start_time + datetime.timedelta(hours=self.reserve_hour_zone))

    class Meta:
        ordering = ['seats_id','reserve_start_time','reserve_id']
        verbose_name = '予約'
        verbose_name_plural = '予約'
