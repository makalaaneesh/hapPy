from django.shortcuts import render
from .models import WordCount

# Create your views here.
import urllib

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello. You're here to view Tweet Analytics!")


def wordcloud(request):
    img_string = WordCount.get_word_cloud_image()
    context = {
        'wordcloud_image_str' : urllib.parse.quote(img_string)
    }
    return render(request, 'tweet_analytics/wordcloud.html', context)
    # uri = 'data:image/png;base64,' + urllib.parse.quote(img_string)
    # html = '<img src = "%s"/>' % uri

    # return HttpResponse(html)
