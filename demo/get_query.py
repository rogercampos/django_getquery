import urllib
import re
from django.http import QueryDict


class GetQuery:
    def __init__(self, request, only=[], exclude=[]):
        self.dict = request.GET.copy()
        for x in request.GET.keys():
            if x in exclude or (only and x not in only):
                try:
                    del self.dict[x]
                except:
                    pass

    def to_query_safe(self, mod=''):
        if not self.dict and not mod:
            return ''

        if mod:
            if isinstance(mod, QueryDict):
                new_dict = self.dict.copy()
                for x in mod.keys():
                    if x[0] == '$':
                        for y in mod.getlist(x):
                            new_dict.appendlist(x[1:], y)
                    else:
                        new_dict[x] = mod[x]
            else:
                new_dict = self.dict.copy()
                mods = mod.split(',')
                for x in mods:
                    values = x.strip().split(':')
                    if values[0][0] == '$':
                        new_dict.appendlist(values[0][1:], values[1])
                    else:
                        new_dict[values[0]] = values[1]
        else:
            new_dict = self.dict

        pairs = []
        for x in new_dict.lists():
            for y in x[1]:
                pairs.append("%s=%s" % (x[0], urllib.quote(str(y))))

        return '?' + '&'.join(pairs)

	def to_query(self, mod=''):
		if mod and not GetQuery.validate_mod(mod):
			return 'ERROR'
		else:
			return self.to_query_safe(mod)

    @staticmethod
    def validate_mod(str):
        regex = r'(\$?\w+:.+)'
        for x in str.split(','):
            if not re.match(regex, x):
                return False
        return True


def get_int_from_get(request, expected):
    if expected in request.GET:
        try:
            res = int(request.GET[expected])
        except:
            res = None
    else:
        res = None
    return res

def get_str_from_get(request, expected):
    if expected in request.GET:
        res = str(request.GET[expected])
    else:
        res = ''
    return res
