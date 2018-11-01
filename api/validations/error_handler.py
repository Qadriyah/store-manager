from flask import jsonify


class CustomeErrorHandler():
    def __init__(self, data, schema):
        self.schema = schema
        self.data = data
        self.errors = {}
        self.data_keys = [*self.data]
        self.schema_keys = [*schema]

    def validate_field_names(self):
        if len(self.data_keys) == 1 and not self.data_keys[0]:
            for field in self.schema_keys:
                self.errors.update({
                    field: "{} is a required field".format(field)
                })
            return self.errors

        if len(self.data_keys) > 1:
            for field in self.schema_keys:
                if field not in self.data_keys:
                    self.errors.update({
                        field: "{} is a required field".format(field)
                    })
            return self.errors
        return True

    def validate_strings(self):
        for key, value in self.data.items():
            if not value:
                self.errors.update({
                    key: "Cannot be empty"
                })
        if len(self.errors) > 0:
            return self.errors
        return True

    def validate_integers(self):
        for key, value in self.data.items():
            try:
                int(value)
            except ValueError:
                self.errors.update({
                    key: "Only numbers are allowed for {}".format(key)
                })
        if len(self.errors) > 0:
            return self.errors
        return True
