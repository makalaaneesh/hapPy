from django.db import models

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import urllib, base64
import base64
from io import BytesIO

# Create your models here.


class WordCount(models.Model):
    word = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    @classmethod
    def get_word_cloud_image(cls):
        all_objs = cls.objects.all()
        word_count_dict = {obj.word: obj.count for obj in all_objs}

        wc_class = WordCloud(background_color='white',
                             stopwords=STOPWORDS,
                             width=1200,
                             height=600,
                             colormap="Set2")
        wc = wc_class.generate_from_frequencies(word_count_dict)

        wc_image = wc.to_image()

        # Saving to string and encoding
        output = BytesIO()
        wc_image.save(output, format='PNG')
        output.seek(0)
        output_s = output.read()
        b64 = base64.b64encode(output_s)
        return b64

        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        #
        # # https://stackoverflow.com/questions/5314707/matplotlib-store-image-in-variable/45099838#45099838
        # fig = plt.gcf()
        #
        # buf = io.BytesIO()
        # fig.savefig(buf, format='png')
        # buf.seek(0)
        # string = base64.b64encode(buf.read())

        return string


