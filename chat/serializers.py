from rest_framework import serializers

class PostSerialiser(serializers.Serializer): 
    session = serializers.IntegerField(max_value=10000, min_value=1)
    content = serializers.CharField(max_length=255, min_length=3) 


class GetSerialiser(serializers.Serializer): 
    sid = serializers.IntegerField(max_value=10000, min_value=1)
    pag = serializers.IntegerField(max_value=4, min_value=1, required=False)