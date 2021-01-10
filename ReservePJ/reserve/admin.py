from django.contrib import admin
from reserve.models    import office_category,Floor,Room,Seats,Reserve

# Register your models here.
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Seats)
admin.site.register(Reserve)
admin.site.register(office_category)
# Register your models here.
