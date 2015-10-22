from rest_framework import fields


class FilterField(object):
    _creation_counter = 0

    def __init__(self, name=None, required=False, lookup_type='exact'):
        self.name = name
        self.required = required
        self.lookup_type = lookup_type

        self._creation_counter = FilterField._creation_counter
        FilterField._creation_counter += 1


class BooleanFilter(FilterField):
    field_class = fields.BooleanField
