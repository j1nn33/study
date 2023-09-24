# простого способа представить структурные данные:
tweet = {
    "user" : "joelgrus",
    "text" : "Наука данных - потрясающая тема",
    "retweet_count" : 100,
     "hashtags" : ["#data", "#science", "#datascience", "#awesome", "#yolo"]
} 

# Помимо поиска отдельных ключей можно обратиться ко всем сразу

tweet_keys = tweet.keys()       # список ключей
tweet_values = tweet.values()   # список значении
tweet_items = tweet.items()     # список кортежей (ключ, значение)


print (tweet_keys)
print (tweet_values)
print (tweet_items)