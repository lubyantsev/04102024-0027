from django.db import models

class Schedule(models.Model):
    password = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='events', on_delete=models.CASCADE)
    when = models.CharField(max_length=255)
    where = models.CharField(max_length=255)
    who = models.CharField(max_length=255)
    position_x = models.FloatField(default=0.0)  # Позиция X на экране
    position_y = models.FloatField(default=0.0)  # Позиция Y на экране

    def get_color(self):
        if self.when and self.where and self.who:
            return 'pink'  # Розовый цвет
        elif self.when and self.where:
            return 'lightseagreen'  # Светло-изумрудный цвет
        elif self.when:
            return 'lightseagreen'  # Светло-изумрудный цвет
        return 'grey'  # Цвет по умолчанию