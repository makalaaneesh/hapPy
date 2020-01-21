import os
import random

PATH = "{basepath}/etc/quotes.txt".format(basepath=os.environ['HAPPY_HOME'])


def get_uplifting_quote(tweet, limit=280):
    with open(PATH, "r") as f:
        quotes = f.readlines()

        found_quote = False
        quote = ""
        while not found_quote:
            random_quote = random.choice(quotes)
            quote = "{0} #happiness #MentalHealth #MentalHealthAwareness".format(random_quote)
            if len(random_quote) > 5 and len(quote) < limit:
                found_quote = True
                break
        return quote
