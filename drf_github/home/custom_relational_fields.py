from rest_framework import serializers


class EmailAndUsernameFields(serializers.RelatedField):
    def to_representation(self, value):
        # value is a object
        return f"{value.email} - {value.username}"
