import os, json, nltk, string 

import utils as tech

from pprint import pprint 
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import framenet as fn

lmtz = WordNetLemmatizer()
PATH = "../phikal/forums"
stopwords = open('../phikal/data/stopwords').read().splitlines() 

substance_effects = {drug:[] for drug in  json.load(open(os.path.join(os.getcwd(),'..','phikal','data','drug_misnaming.json'),'rb')).keys()}
named_entities = set(json.load(open('./drug-taxonomy.json','rb')).keys()) & set(tech.flatten(json.load(open('./drug_misnaming.json','rb')).values()))

allowed_topics = {'Excreting','Excreter','Medical_conditions','Health_response'}

def is_medical(frame_list):
	if len(frame_list) == 0:
		return -1
	else:
		return any([len(set(frame.FE.keys()) & allowed_topics)>0  for frame in frame_list])

parsed_yes = []
parsed_no = []
unparsed = []

def process(item):
	line = ' '.join(item)
	ans =[lmtz.lemmatize(word,pos=tech.get_wordnet_pos(pos)) for word, pos in nltk.pos_tag(nltk.word_tokenize(line))]
	return [(lemma,is_medical(fn.frames_by_lemma(lemma))) for lemma in ans]

denom = 9286.
for i,filename in enumerate(os.listdir(PATH)):
	print i/denom
	fragment = {}
	text = open(os.path.join(PATH,filename)).read().decode("utf-8").lower()

	corpus = (tech.standardize_drug_names([word for word in nltk.word_tokenize(sentence)
				if not any([word in lst for lst in [stopwords,string.punctuation+'`']])]) 
				for sentence in nltk.sent_tokenize(text))

	counter = 0 
	for sentence in corpus:
		if counter < 3:
			if sentence:
				entities = named_entities & set(sentence)
				if len(entities) > 0:
					combined_key = '-'.join(entities)
					if combined_key not in fragment:
						fragment[combined_key] = []
					
					current_payload = fragment[combined_key]
					updated_payload = current_payload + process(item for item in list(set(sentence) - entities) if item.isalpha() and item.isalnum())
					fragment[combined_key] = updated_payload
		
					for key,value in fragment.iteritems():
						if key not in substance_effects:
							substance_effects[key] = []
						
						current_payload = substance_effects[key]
						updated_payload = current_payload + value
						substance_effects[key] = updated_payload
			counter += 1

for key,value in substance_effects:
	for word,isRelated in value:
		if isRelated == -1:
			unparsed += [word]
		elif isRelated:
			parsed_yes += [word]
		else:
			parsed_no += [word]

json.dump({'parsed_no':parsed_no,'parsed_yes':parsed_yes,'unparsed':unparsed}, open('./frame-parsed-effects.json','wb'))
pprint({'parsed_no':parsed_no,'parsed_yes':parsed_yes,'unparsed':unparsed})
