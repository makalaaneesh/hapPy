from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier


# applicable for NaiveBayes, SGDClassifier
alpha_ranges = [ 0.0001,0.001,0.01,0.1,1,2,3,4,5,6,7,8,9,10,50,100]

def linearSVM():
    model_params = dict(eta0=0.0001,
                        loss='hinge',
                        random_state=15,
                        penalty='l2',
                        tol=1e-3,
                        verbose=0)
    return SGDClassifier(model_params)

def multinomialNB():
    return MultinomialNB()


