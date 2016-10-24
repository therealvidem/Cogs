import urllib.request
import xmltodict

class color:

def homepage(request):
    file = urllib2.urlopen('https://www.goodreads.com/review/list/20990068.xml?key=nGvCqaQ6tn9w4HNpW8kquw&v=2&shelf=toread')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return render_to_response('my_template.html', {'data': data})
