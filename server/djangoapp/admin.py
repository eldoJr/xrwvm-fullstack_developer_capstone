from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import CarMake, CarModel

# Register your models here.

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    actions = ['view_cars']
    
    def view_cars(self, request, queryset):
        return HttpResponseRedirect('/djangoapp/get_cars')
    
    view_cars.short_description = "View all cars"

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ('car_make', 'type')
    actions = ['view_cars']
    
    def view_cars(self, request, queryset):
        return HttpResponseRedirect('/djangoapp/get_cars')
    
    view_cars.short_description = "View all cars"

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
