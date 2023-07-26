from django.contrib import admin

from basic_app import models

# Register your models here.
admin.site.register(models.Upload_File)
admin.site.register(models.Upload_File2)


class Model1Admin(admin.ModelAdmin):
    search_fields = ['model_name', 'mark__mark_name']
    list_filter = ['model_name']
    sortable_by = ['file_id']


admin.site.register(models.Model1, Model1Admin)


class MarkAdmin(admin.ModelAdmin):
    search_fields = ['mark_name']
    list_filter = ['mark_name']
    sortable_by = ['mark_name']


admin.site.register(models.Mark, MarkAdmin)


class Data21Admin(admin.ModelAdmin):
    search_fields = ['time']
    search_help_text = "Search by time"  # Fix the attribute name
    list_filter = ['file_id']  # Fix the attribute name for sorting


admin.site.register(models.DATA21, Data21Admin)


class Data22Admin(admin.ModelAdmin):
    search_fields = ['time']
    search_help_text = "Search by time"  # Fix the attribute name
    list_filter = ['file_id']  # Fix the attribute name for sorting


admin.site.register(models.DATA22, Data22Admin)
