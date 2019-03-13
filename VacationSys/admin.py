from django.contrib import admin
from .models import typeofvacation
from .models import holiday
from .models import tableofinfo
from .models import noteforleave

# Register your models here.
@admin.register(typeofvacation)
class TypeOfVacationAdmin(admin.ModelAdmin):
    list_display = ('idVacation', 'holiType', 'marryOrNot', 'sepWithCouple', 'sepWithParent', 'serMeet10', 'serMeet20', 'daysOfVacation')


@admin.register(holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('nameOfHoli', 'dateOfHoli')


@admin.register(tableofinfo)
class TableOfInfoAdmin(admin.ModelAdmin):
    list_display = ('person', 'daysOfRoad', 'sepWithCouple', 'sepWithParent', 'holiType', 'daysLeft', 'status')
    list_filter = ('person', 'sepWithCouple', 'sepWithParent', 'status')
    search_fields = ('person',)


@admin.register(noteforleave)
class NoteForLeaveAdmin(admin.ModelAdmin):
    list_display = ('person', 'holiType', 'dateOfStart', 'dateOfEnd', 'dateOfAdd', 'dateOfCancel', 'apprFlag', 'apprUpperFlag')
    list_filter = ('person', 'apprFlag', 'apprUpperFlag')
    search_fields = ('person',)
    date_hierarchy = 'dateOfAdd'
    ordering = ('dateOfStart', 'dateOfAdd')
