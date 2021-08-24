from rest_framework import serializers
from .models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=50, min_length=10, write_only=True)
    default_error_messages = {
        'username': 'USERNAME should only contain alphanumeric characters'}
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def validate(self, attrs):

        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():

            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
    class EmailVerificationSerializer(serializers.ModelSerializer):
        token = serializers.CharField(max_length=1000)

        class Meta:
            model = User
            fields = ['token']