from django.shortcuts import render_to_response
from get_query_example.demo.get_query import GetQuery


def index(request):
    return render_to_response('demo/index.html',
                              {})

def tester(request):
	gq = GetQuery(request)
	foo = [11,22,33,44,55]
	return render_to_response('demo/tester.html',
                              {'gq': gq,
							   'foo': foo})
