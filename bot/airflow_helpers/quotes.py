import os
import random

PATH = "{basepath}/etc/quotes.txt".format(basepath=os.environ['HAPPY_HOME'])


def get_uplifting_quote(tweet, limit=280):
    """
    :param tweet: tweet text
    :param limit: limit of characters
    :return: Get a random quote from the list of quotes and return one.

    TODO: Pick a relevant quote(and not just any random quote)
    """
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


def get_follow_up_response(tweet):
    return "https://twitter.com/owhnm/status/1259038214515392512?s=20"
