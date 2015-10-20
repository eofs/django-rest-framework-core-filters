from collections import OrderedDict
import copy
from django.utils import six
from core_filters.filters import FilterField


class FilterSetMetaClass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.
    Any instances of `FilterField` included as attributes on either the class
    or on any of its superclasses will be include in the
    `_declared_fields` dictionary.
    """

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, FilterField)]
        fields.sort(key=lambda x: x[1]._creation_counter)

        # If this class is subclassing another FilterSet, add that FilterSet's
        # fields. Note that we loop over the bases in *reverse*. This is necessary
        # in order to maintain the correct order of fields.
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = list(base._declared_fields.items()) + fields

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super(FilterSetMetaClass, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(FilterSetMetaClass)
class FilterSet(object):
    def __init__(self, data, queryset=None):
        self.data = data
        self.queryset = queryset

    def get_fields(self):
        return copy.deepcopy(self._declared_fields)

    def is_valid(self, raise_exception=False):
        if not hasattr(self, '_validated_data'):
            self._validated_data = {}
            self._errors = {}
        return not bool(self._errors)

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors

    @property
    def validated_data(self):
        if not hasattr(self, '_validated_data'):
            msg = 'You must call `.is_valid()` before accessing `.validated_data`.'
            raise AssertionError(msg)
        return self._validated_data

    @property
    def qs(self):
        return self.queryset


class ModelFilterSet(FilterSet):
    def get_fields(self):
        assert hasattr(self, 'Meta'), (
            'Class {viewset_class} missing "Meta" attribute'.format(
                viewset_class=self.__class__.__name__
            )
        )
        # TODO Get fields from Meta class
        return super(ModelFilterSet, self).get_fields()