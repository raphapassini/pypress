from treemenus.models import Menu, MenuItem
from rest_framework import serializers
from .models import MenuItemExtension


class SubMenuItemSerialize(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')

    class Meta:
        model = MenuItem


class MenuExtensionSerializer(serializers.ModelSerializer):
    menu_type_display = serializers.CharField(
        source='get_menu_type_display', read_only=True)
    related_display = serializers.CharField(
        source='get_related_display', read_only=True)
    menu_item = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MenuItemExtension


class MenuItemSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)
    subitems = SubMenuItemSerialize(many=True, read_only=True,
                                    source='children',)
    extension = MenuExtensionSerializer()
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = MenuItem

    def create(self, validated_data):
        extension = validated_data.pop('extension')

        if not validated_data.get('parent'):
            validated_data['parent'] = MenuItem.objects.get(
                menu=validated_data['menu'], caption='root')

        instance = MenuItem.objects.create(**validated_data)
        extension['menu_item'] = instance
        MenuItemExtension.objects.create(**extension)
        return instance


class MenuSerializer(serializers.ModelSerializer):
    contained_items = serializers.SerializerMethodField()

    def get_contained_items(self, obj):
        items = MenuItem.objects.filter(menu=obj, level=1)
        serializer = MenuItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = Menu
