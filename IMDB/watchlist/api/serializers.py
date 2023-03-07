from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatorm

class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        #fields = "__all__"
        # fields = ['id', 'name', 'description']
        exclude = ["active"]
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatorm
        fields = "__all__"
    
    # def get_len_name(self, obj):
    #     return len(obj.name)
    
    # # Field level validation
    # def validate_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name must be at least 3 characters long")
    #     else:
    #         return value

    # # Object level validation
    # def validate(self, data):
    #     if data["name"] == data["description"]:
    #         raise serializers.ValidationError("Title and description should be different")
    #     else:
    #         return data

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         """Create a new movie"""
#         return Movie.objects.create(**validated_data)
        
#     def update(self, instance, validated_data):
#         # instance carries the old values
#         # validated_data carries the new values
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     # Field level validation
#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError("Name must be at least 3 characters long")
#         else:
#             return value

#     # Object level validation
#     def validate(self, data):
#         if data["name"] == data["description"]:
#             raise serializers.ValidationError("Title and description should be different")
#         else:
#             return data