import json, csv

data = json.load(open('./drug-taxonomy.json','rb'))
synonyms = json.load(open('./drug_misnaming.json','rb'))
f = csv.writer(open('./to-import-to-protege.csv','wb+'))

#Write Header
f.writerow(["substance","class one","class two","class three","effect one","effect two","effect three",
		"synonym_one","synonym_two","synonym_three","ingredient_one","ingredient_two","ingredient_three"])

for drug in data.iterkeys():
	#hacky, but it works
	row = []
	row += [drug]

	print drug
	if "class" in data[drug]:
		drug_class = data[drug]["class"]
		row += (drug_class + [""]*(3-len(drug_class)))
	else:
		row += ["","",""]
	
	drug_effect = data[drug]["effects"]
	row += (drug_effect + [""]*(3-len(drug_effect)))

	if drug in synonyms:
		drug_synonyms = synonyms[drug]
		#Only some entries are lists
		if type(drug_synonyms) != type([]):
			drug_synonyms = [drug_synonyms]

		row += (drug_synonyms + [""]*(3-len(drug_synonyms)))
	else:
		row += ["","",""]

	if "ingredients" in data[drug]:
		drug_ingredients = data[drug]["ingredients"]
		if type(drug_ingredients) == type([]):
			row += (drug_ingredients + [""]*(3-len(drug_ingredients)))
		elif type(drug_ingredients) == type({}):
			row += (drug_ingredients.keys() + [""]*(3-len(drug_ingredients)))
		else:
			row +=  ["","",""]
	else:
		row += ["","",""]

	f.writerow(row)