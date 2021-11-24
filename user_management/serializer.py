from rest_framework import serializers


class SignUpAndLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50)


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    otp = serializers.CharField(max_length=50)
