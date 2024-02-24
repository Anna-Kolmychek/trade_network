from rest_framework import serializers

from traders.models import Trader


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = '__all__'
        extra_kwargs = {
            'debt': {'read_only': True}
        }

