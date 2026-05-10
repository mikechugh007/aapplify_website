from django.contrib import admin
from .models import Service, BlogPost, Ticket, Message, ServiceBooking, Plugin

# Register your models here.

@admin.register(Service)
class UserServiceAdmin(admin.ModelAdmin):
    list = ('pk', 'title', 'price', 'created')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_by', 'is_accepted', 'published_at']
    search_fields = ["title", "created_at__username"]
    list_editable = ["is_accepted",]
    list_filter = ["created_by", "is_accepted"]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'staff', 'created_at', 'updated_at']

@admin.register(Message)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at', 'updated_at']

    
@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'user', 'booking_date', 'status']


admin.site.site_header = 'Aaplify dashboard'



class PluginAdmin(admin.ModelAdmin):
    list_display = ["pk", "file"]

admin.site.register(Plugin, PluginAdmin)
