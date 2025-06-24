from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import Category

class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = "Categories"
    menu_icon = "list-ul"  # иконка в админке
    add_to_settings_menu = False
    list_display = ("name",)
    search_fields = ("name",)

modeladmin_register(CategoryAdmin)