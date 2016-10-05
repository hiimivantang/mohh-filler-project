import click
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize



@click.command()
@click.option("--word", default="smoke", help="word to look for in clinical notes")
@click.option("--mongo-host", default="192.168.0.2", help="ip or url of mongodb")
def main(word, mongo_host):
    client = MongoClient(mongo_host, 27017)
    db = client.mimic
    total_count = db.noteevents.count()
    documents = db.noteevents.find({"$text": { "$search": "smoke" } })
    print "%d of %d notes found." %(documents.count(), total_count)
    raw_input()
    for doc in documents:
        process_doc(doc)

#this function can be improved. Currently manually looking for sentence of interest.
def is_smoke_in_sent(sent):
    if "smoke" in sent.lower():
        return True
    if "smok" in sent.lower():
        return True
    if "smoking" in sent.lower():
        return True
    


def is_smoker(doc):
    #get clinical notes
    text = doc["TEXT"]
    sent_tokenize_list = sent_tokenize(text)
    for sent in sent_tokenize_list:
        if is_smoke_in_sent(sent):
            print sent


def process_doc(doc):
    print ">>>>> SUBJECT_ID: %d" %doc["SUBJECT_ID"]
    print ">>>>> CHARTDATE: %s" %doc["CHARTDATE"]
    print ">>>>> CATEGORY: %s" %doc["CATEGORY"]
    print ">>>>> CLINICAL NOTE:"
    is_smoker(doc)
    raw_input()

if __name__ == '__main__':
	main()
