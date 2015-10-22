from core_filters.filters import FilterField


class TestFilterField:
    def test_init(self):
        filter = FilterField(name='foo', required=True, lookup_type='iexact')
        assert filter.name == 'foo'
        assert filter.required == True
        assert filter.lookup_type == 'iexact'
