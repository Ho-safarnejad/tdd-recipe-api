from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        """ create a new user with encrypteed password """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user



class TokenSerilizer(serializers.Serializer):
    """ serializer for user authentication object s"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # when we validate our serializer this will be called
    # checks the inputs are correct
    def validate(self, attrs):
        """ validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
