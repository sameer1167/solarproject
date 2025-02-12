from django.contrib import admin
from .models import ShippingAddress,order,orderItem

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(order)
admin.site.register(orderItem)

#create order item inline
class OrderItemInline(admin.StackedInline):
    model = orderItem
    extra = 0

# extend order model
class OrderAdmin(admin.ModelAdmin):
    model=order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]

#unregister order model
admin.site.unregister(order)

# re-register order and orderadmin
admin.site.register(order,OrderAdmin)