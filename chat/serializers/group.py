from rest_framework import serializers



class GroupAddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    group_id = serializers.IntegerField(min_value=1)


