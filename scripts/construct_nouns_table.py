# This script constructs a CSV file containing noun lemmas associated with the categories and articles. The script only stores noun lemmas that are among the most 5000 frequent lemmas in SoNaR.

import pandas as pd
import numpy as np
from pathlib import Path

# This is the output data file where this script stores the result of processing all noun data files.
output_file = Path("data/nouns.csv")

# If the output data file already exists, delete the file.
if output_file.exists():
	output_file.unlink()

# Read frequency list, and limit the result to the 5000 most frequent lemmas. See notes in data/noun_lemma_frequency_list.txt for more information about the need for grouping.
lemma_frequency_list = pd.read_csv("data/lemma_frequency_list.csv").groupby("lemma", as_index=False)[["count"]].sum().sort_values(by="count", ascending=False)[:5000]

# Read pronoun data.
pronouns = pd.read_csv("data/pronouns.csv", usecols=["lemma"])

# Read conjunction data.
conjunctions = pd.read_csv("data/conjunctions.csv", usecols=["lemma"])

# Initialize empty data frame. The script collects all cateogry data in this data frame.
categories_concatenated = pd.DataFrame()
categories_concatenated.insert(0, "lemma", "")
categories_concatenated.insert(1, "category", "")

# The name of the file denotes the semantic category.
for file_name in Path("data/nouns/categories").glob("*.csv"):
	# Read category data, grouping by lemma to collapse all duplicates into one lemma.
	tmp = pd.read_csv(file_name, usecols=["lemma"]).groupby("lemma", as_index=False).nunique()
	# Exclude pronouns and conjunctions. This will also result in the exclusion of pronouns and conjunctions in the last line in this script, resulting in an output file that contains no pronouns and no conjunctions.
	tmp = tmp[~tmp["lemma"].isin(pronouns["lemma"])]
	tmp = tmp[~tmp["lemma"].isin(conjunctions["lemma"])]
	# Insert the category column with a constant value derived from the name of the file.
	tmp.insert(1, "category", file_name.stem)
	# Accumulate data.
	categories_concatenated = pd.concat([categories_concatenated, tmp])

# Group category data by lemma to collapse duplicates, concatenating categories.
categories_concatenated = categories_concatenated.groupby("lemma", as_index=False).aggregate(lambda x: ";".join(x.tolist()))

# Initialize empty data frame. The script collects all article data in this data frame.
articles_concatenated = pd.DataFrame()
articles_concatenated.insert(0, "lemma", "")
articles_concatenated.insert(1, "article", "")

# The name of the file denotes the article.
for file_name in Path("data/nouns/articles").glob("*.csv"):
	# Read article data, grouping by lemma to collapse all duplicates into one lemma.
	tmp = pd.read_csv(file_name, usecols=["lemma"]).groupby("lemma", as_index=False).nunique()
	# Insert the article column with a constant value derived from the name of the file.
	tmp.insert(1, "article", file_name.stem)
	# Accumulate data.
	articles_concatenated = pd.concat([articles_concatenated, tmp])

# Group article data by lemma to collapse duplicates, concatenating articles.
articles_concatenated = articles_concatenated.groupby("lemma", as_index=False).aggregate(lambda x: ";".join(x.tolist()))

# (Inner) join frequency data with category data and article data, filtering out any lemma not in the 5000 most frequent lemmas and any lemma with missing/no article. Then, sort the data by count. Finally, write the result to the output file.
articles_concatenated.merge(categories_concatenated.merge(lemma_frequency_list, how="inner", left_on="lemma", right_on="lemma"), how="inner", left_on="lemma", right_on="lemma").sort_values(by="count", ascending=False).to_csv(output_file, columns=["lemma","article","category"], index=False)