from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

docs = ["我 爱 篮球", "电影 明星", "篮球 比赛", "娱乐 新闻"]
labels = ["体育", "娱乐", "体育", "娱乐"]

vec = CountVectorizer()
x = vec.fit_transform(docs)

model = MultinomialNB()
model.fit(x, labels)

test = vec.transform(["篮球 明星"])
print(model.predict(test))