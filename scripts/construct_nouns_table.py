# This script constructs a CSV file containing noun lemmas associated with the categories and articles. The script only stores noun lemmas that are among the most 5000 frequent lemmas in SoNaR.

from pathlib import Path
from csv import reader, writer
from itertools import groupby

# Read frequency list, and limit the result to the 5000 most frequent lemmas. See notes in data/noun_lemma_frequency_list.txt for more information on the need for grouping.
lemma_frequency_list = None
with open("data/lemma_frequency_list.csv") as file:
	# Skip CSV header.
	file.readline()
	lemma_frequency_list = [(row[0], int(row[1])) for row in reader(file)]
# Sort lemma frequency data by lemma for later grouping.
lemma_frequency_list.sort(key=lambda x: x[0])
# Group by lemma summing frequencies.
lemma_frequency_list = [(group[0], sum([record[1] for record in group[1]])) for group in groupby(lemma_frequency_list, lambda x: x[0])]
# Order lemma data by frequency descending.
lemma_frequency_list.sort(key=lambda x: x[1], reverse=True)
# Limit lemma data to 5000.
lemma_frequency_list = {lemma_frequency[0] for lemma_frequency in lemma_frequency_list[:5000]}

# List of excluded lemmas.
excluded_lemmas = None
# Add pronoun lemmas to excluded lemmas.
with open("data/pronouns.csv") as file:
	# Skip CSV header.
	file.readline()
	excluded_lemmas = {row[1] for row in reader(file)}

# Add conjunction lemmas to excluded lemmas.
with open("data/conjunctions.csv") as file:
	# Skip CSV header.
	file.readline()
	excluded_lemmas = excluded_lemmas | {row[1] for row in reader(file)}

# Add numeral lemmas to excluded lemmas.
with open("data/telwoorden.csv") as file:
	# Skip CSV header.
	file.readline()
	excluded_lemmas = excluded_lemmas | {row[1] for row in reader(file)}

# Collect lemma category data.
lemma_categories = []
# Iterate over the files under the category folder. The name of the file denotes the semantic category.
for file_name in Path("data/nouns/categories").glob("*.csv"):
	# Abstract noun no good! This is still unexplainable at the moment. Exclude all nouns that belong to no other cateogry but abstract.
	# Add verzamelnaam to the list of excluded nouns. These nouns are of an ambiguous nature.
	if file_name.stem != "abstract" and file_name.stem != "verzamelnaam":
		with open(file_name) as file:
			# Skip CSV header.
			file.readline()
			# Append lemmas from file, associated with the category, if the lemma is not excluded.
			lemma_categories = lemma_categories + [(lemma, file_name.stem) for lemma in {row[1] for row in reader(file) if row[1] not in excluded_lemmas}]
# Sort lemma category data by lemma for later grouping.
lemma_categories.sort(key=lambda x: x[0])
# Group by lemma concatenating categories.
lemma_categories = {group[0]: [record[1] for record in group[1]] for group in groupby(lemma_categories, lambda x: x[0])}

# Collect lemma article frequency data.
lemma_articles = None
with open("data/nouns/articles.csv") as file:
	# Skip CSV header.
	file.readline()
	# (article, lemma, frequency)
	lemma_articles = [tuple(row[0].split(" ")) + (row[1], ) for row in reader(file)]
# Sort lemma article data by lemma for later grouping.
lemma_articles.sort(key=lambda x: x[1])
# Group by lemma and choose the most frequent article.
lemma_articles = [(group[0], max(group[1], key=lambda x: int(x[2]))[0]) for group in groupby(lemma_articles, lambda x: x[1])]

with open("data/nouns.csv", "w") as file:
	file.write("lemma,article,category\n")
	for lemma_article in lemma_articles:
		if lemma_article[0] in lemma_frequency_list:
			try:
				categories = lemma_categories[lemma_article[0]]
				file.write(lemma_article[0])
				file.write(",")
				file.write(lemma_article[1])
				file.write(",")
				file.write(";".join(categories))
				file.write("\n")
			except KeyError:
				pass