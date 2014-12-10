from treemenus.models import Menu, MenuItem
from rest_framework import serializers
from .models import MenuItemExtension


class SubMenuItemSerialize(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')
    
    class Meta:
        model = MenuItem


class MenuExtensionSerializer(serializers.ModelSerializer):
    menu_type_display = serializers.CharField(source='get_menu_type_display')
    related_display = serializers.CharField(source='get_related_display')

    class Meta:
        model = MenuItemExtension


class MenuItemSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')
    subitems = SubMenuItemSerialize(many=True, read_only=True,
                                    source='children',)
    extension = MenuExtensionSerializer(read_only=True)

    class Meta:
        model = MenuItem


class MenuSerializer(serializers.ModelSerializer):
    contained_items = serializers.SerializerMethodField()

    def get_contained_items(self, obj):
        items = MenuItem.objects.filter(menu=obj, level=1)
        serializer = MenuItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = Menu
