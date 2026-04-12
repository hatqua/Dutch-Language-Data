# This is the script that builds the corpus. This script has many dependencies that are CSV files.
# This script is not the most perfect piece of code ever written, because it contains lots of code duplication. This is more of a coarse piece of code, one that needs some refinment. Nevertheless, this script is a one-time-use kind of script. (Due to some tight deadlines that I came up with, I could not refine it.)

from random import choice

word_associations = set([]) # This set will contain all word associations as unordered pairs. A pair denotes that two lemma forms are semantically related.
nouns = [] # Table of nouns.
verbs = [] # Table of verbs.

# A temporary placeholder for stuff.
parts = None

# Open word associations file for reading.
with open("data/word_associations.csv") as file:
	# Skip CSV header.
	file.readline()
	# Process word associations file line by line.
	for line in file:
		# Each line in the file is an unordered pair of word associates. (Well, they are ordered in the file, but the order is irrelevant.)
		# Split the line, upon removing the CSV line terminator, make a set out of the split line, and store.
		# A set because the order is irrelevant. And a frozenset because this is how Python works: Python sets only store objects that are hashable, which frozenset is, but a Python set is not.
		word_associations.add(frozenset(line[:-1].split(",")))

# Open nouns file for reading.
with open("data/nouns.csv") as file:
	# Skip CSV header.
	file.readline()
	# Process file line by line.
	for line in file:
		# Split the line extracting field values: lemma, article, and category. The last field is a colon-separated list of categories to which the noun belongs.
		parts = line[:-1].split(",")
		# Abstract noun no good! This is still unexplainable at the moment. Exclude all nouns that belong to no other cateogry but abstract.
		if parts[2] != "abstract":
			# The following condition excludes only het/de koper (het koper = the copper, de koper = the buyer). This is the only case in the file where changing the article has the effect of changing the status of membership to category persoonsnaam (het koper ∉ persoonsnaam, but de koper ∈ persoonsnaam). (Otherwise, create two records manually, but I just try to avoid manual labor!)
			if ";" not in parts[1] or "persoonsnaam" not in parts[2]:
				# Create a record per article. That is, for a noun that accepts one article, create one recrod only (de or het), but for a noun that accepts two articles, two records (de and het). For example: two records for de/het wezen, but one for het meisje.
				for article in parts[1].split(";"):
					# A record is a tuple comprising the following fields: lemma, article, and list of semantic categories to which the noun (lemma) belongs.
					# Never mind abstract. Just exclude abstract and all its associates.
					nouns.append(tuple([parts[0], article, frozenset(parts[2].split(";")) - set(["abstract"])]))

# Open verbs file for reading.
with open("data/verbs.csv") as file:
	# Skip CSV header.
	file.readline()
	# Process file line by line.
	for line in file:
		# Split the line extracting field values: verb, past, suffix, direct object category, frequency, and reference. The direct object category field is a colon-separated list of categories to which the noun belongs. This will turn messy at the flast ield, which we don't need, however.
		parts = line[:-1].split(",")
		# Exclude all verbs that accept direct objects belonging to the cateogry abstract only, and no other category.
		if parts[3] != "abstract":
			# Create a record for each verb. A record is a tuple comprising the following fields: verb in infinite form (lemma), past tense of verb, preposition, a list of semantic categories of which nouns the verb accepts in direct object position, excluding abstract.
			verbs.append(tuple([parts[0], parts[1], parts[2], frozenset(parts[3].split(";")) - set(["abstract"])]))

# Subset the table of nouns by filtering out any noun not belonging to the catagory persoonsnaam. These will serve the purpose of subjects and indirect objects.
persoonsnaam = [noun for noun in nouns if "persoonsnaam" in noun[2]]

# Stuff!
prime_verb = None
target_verb = None

prime_subject = None
target_subject = None

prime_indirect_object = None
target_indirect_object = None

prime_direct_object = None
target_direct_object = None

sentence_pair = None

# Start constructing subcorpora, condition after another.

# Frist condition: definitely no overlap of any kind whatsoever, absolutely (not).

# Stores subcorpora.
subcorpus = set([])

# 15000 sentence pair/condition (P/C).
while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			target_subject[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_subject[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_indirect_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_indirect_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
		):
		target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or
			# belongs to a cateogry the target sentence verb does not accept;
			target_direct_object[2].isdisjoint(target_verb[3]) or
			# lexically overlaps with the target sentence indirect object;
			target_direct_object[0] == target_indirect_object[0] or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object;
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object;
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
			# lexically overlaps with the prime sentence direct object; or
			target_direct_object[0] == prime_direct_object[0] or
			# semantically overlaps with the prime sentence direct object.
			set([target_direct_object[0], prime_direct_object[0]]) in word_associations
		):
		target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

# Open subcorpus file for writing.
with open("corpus/no_overlap.csv", "w") as file:
	# Write CSV header.
	file.write("ppo,pdo,tpo,tdo\n")
	# Iterate over sentence pairs in the subcorpus and write pairs.
	for sentence_pair in subcorpus:
		# Write prime sentence in prepositional object form (transitive).
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		# Write prime sentence in dative object form (ditransitive).
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		# Write target sentence in prepositional object form (transitive).
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		# Write target sentence in dative object form (ditransitive).
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Second condition: verbs are semantically related.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb, but
			target_verb[0] == prime_verb[0] or
			# semantically does not overlap with the prime sentence verb.
			set([prime_verb[0], target_verb[0]]) not in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			target_subject[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_subject[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_indirect_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_indirect_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
		):
		target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or
			# belongs to a cateogry the target sentence verb does not accept;
			target_direct_object[2].isdisjoint(target_verb[3]) or
			# lexically overlaps with the target sentence indirect object;
			target_direct_object[0] == target_indirect_object[0] or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object;
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object;
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
			# lexically overlaps with the prime sentence direct object; or
			target_direct_object[0] == prime_direct_object[0] or
			# semantically overlaps with the prime sentence direct object.
			set([target_direct_object[0], prime_direct_object[0]]) in word_associations
		):
		target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

# I won't repeat the same comments unless necessary. See comments above for the similar chunck of code.
with open("corpus/semantic_similarity_verb.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Third condition: corresponding nouns across prime and target are semanticaly related.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# This subcorpus while-loop gets stuck always. Therefore, a maximum number of attempts per sub-while-loop as an ad-hoc solution.
	count = 0
	
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Make at most 100 attemps to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically does not overlap with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) not in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnaam)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	# However, it could be the case that the 100th attempt was successful, and it remains ambiguous whether the 100th attempt was successful without (additional) check(s) in the previous while-loop and/or in the following if-clause. Nevertheless, this design is more simple. Besides, efficiency is not the a strict requirement in this script, since this is a one-time-use script.
	if count >= 100:
		continue
	
	count = 0

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Make at most 100 attemps to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or

				# lexically overlaps with the prime sentence subject;
				target_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_indirect_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object; or
				target_indirect_object[0] == prime_indirect_object[0] or
				# semantically does not overlap with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) not in word_associations
			)
		):
		target_indirect_object = choice(persoonsnaam)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue
	
	count = 0
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Make at most 100 attemps to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or
				# belongs to a cateogry the target sentence verb does not accept;
				target_direct_object[2].isdisjoint(target_verb[3]) or
				# lexically overlaps with the target sentence indirect object;
				target_direct_object[0] == target_indirect_object[0] or

				# lexically overlaps with the prime sentence subject;
				target_direct_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_direct_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_direct_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object;
				target_direct_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object;
				set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
				# lexically overlaps with the prime sentence direct object; or
				target_direct_object[0] == prime_direct_object[0] or
				# semantically does not overlap with the prime sentence direct object.
				set([target_direct_object[0], prime_direct_object[0]]) not in word_associations
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/semantic_similarity_nouns.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Fourth condition: the verbs and corresponding nouns across prime and target are semanticaly related.

subcorpus = set([])

while len(subcorpus) < 15_000:
	count = 0
	
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb, but
			target_verb[0] == prime_verb[0] or
			# semantically does not overlap with the prime sentence verb.
			set([prime_verb[0], target_verb[0]]) not in word_associations
		):
		target_verb = choice(verbs)

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Make at most 100 attemps to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically does not overlap with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) not in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnaam)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	# However, it could be the case that the 100th attempt was successful, and it remains ambiguous whether the 100th attempt was successful without (additional) check(s) in the previous while-loop and/or in the following if-clause. Nevertheless, this design is more simple. Besides, efficiency is not the a strict requirement in this script, since this is a one-time-use script.
	if count >= 100:
		continue
	
	count = 0

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Make at most 100 attemps to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or

				# lexically overlaps with the prime sentence subject;
				target_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_indirect_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object; or
				target_indirect_object[0] == prime_indirect_object[0] or
				# semantically does not overlap with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) not in word_associations
			)
		):
		target_indirect_object = choice(persoonsnaam)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue
	
	count = 0
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Make at most 100 attemps to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or
				# belongs to a cateogry the target sentence verb does not accept;
				target_direct_object[2].isdisjoint(target_verb[3]) or
				# lexically overlaps with the target sentence indirect object;
				target_direct_object[0] == target_indirect_object[0] or

				# lexically overlaps with the prime sentence subject;
				target_direct_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_direct_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_direct_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object;
				target_direct_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object;
				set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
				# lexically overlaps with the prime sentence direct object; or
				target_direct_object[0] == prime_direct_object[0] or
				# semantically does not overlap with the prime sentence direct object.
				set([target_direct_object[0], prime_direct_object[0]]) not in word_associations
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/semantic_similarity_all.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Fifth condition: random noun overlap.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Make your (random) choice, Python script: 1 = subject overlap, 2 = indirect object overlap, 3 = direct object overlap.
	noun_choice = choice([1, 2, 3])

	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Check if this script choose subject overlap for this iteration.
	if noun_choice == 1:
		# Keep assigning a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
		while (
				# semantically overlaps with the target sentence verb; or
				set([prime_subject[0], target_verb[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			):
			prime_subject = target_subject = choice(persoonsnaam)
	else:
		# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
		while set([prime_subject[0], target_verb[0]]) in word_associations:
			prime_subject = choice(persoonsnaam)
		# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
		while (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			):
			target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Check if this script choose indirect object overlap for this iteration.
	if noun_choice == 2:
		# Keep assigning a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
		while (
				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb;
				set([prime_indirect_object[0], target_verb[0]]) in word_associations or

				# lexically overlaps with the prime sentence subject;
				target_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_indirect_object[0], prime_verb[0]]) in word_associations
			):
			prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	else:
		# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
		while (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			):
			prime_indirect_object = choice(persoonsnaam)
		# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
		while (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or

				# lexically overlaps with the prime sentence subject;
				target_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_indirect_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object; or
				target_indirect_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			):
			target_indirect_object = choice(persoonsnaam)

	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Check if this script choose direct object overlap for this iteration.
	if noun_choice == 3:
		# Keep assigning a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
		while (
				# belongs to a category neither verb in prime and target sentences accept; or
				prime_direct_object[2].isdisjoint(prime_verb[3]) or
				target_direct_object[2].isdisjoint(target_verb[3]) or

				# lexicaly overlaps with the target sentence subject;
				prime_direct_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([prime_direct_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb;
				set([prime_direct_object[0], target_verb[0]]) in word_associations or
				# lexically overlaps with the target sentence indirect object;
				prime_direct_object[0] == target_indirect_object[0] or
				# semantically overlaps with the target sentence indirect object;
				set([prime_direct_object[0], target_indirect_object[0]]) in word_associations or

				# lexically overlaps with the prime sentence subject;
				target_direct_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_direct_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_direct_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object; or
				target_direct_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object.
				set([target_direct_object[0], prime_indirect_object[0]]) in word_associations
			):
			prime_direct_object = target_direct_object = choice(nouns)
	else:
		# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
		while (
				# lexically overlaps with the prime sentence subject;
				prime_direct_object[0] == prime_subject[0] or
				# belongs to a category the prime sentence verb does not accept;
				prime_direct_object[2].isdisjoint(prime_verb[3]) or
				# lexically overlaps with the prime sentence indirect object;
				prime_direct_object[0] == prime_indirect_object[0] or

				# lexicaly overlaps with the target sentence subject;
				prime_direct_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([prime_direct_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb;
				set([prime_direct_object[0], target_verb[0]]) in word_associations or
				# lexically overlaps with the target sentence indirect object; or
				prime_direct_object[0] == target_indirect_object[0] or
				# semantically overlaps with the target sentence indirect object.
				set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
			):
			prime_direct_object = choice(nouns)
		# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
		while (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or
				# belongs to a cateogry the target sentence verb does not accept;
				target_direct_object[2].isdisjoint(target_verb[3]) or
				# lexically overlaps with the target sentence indirect object;
				target_direct_object[0] == target_indirect_object[0] or

				# lexically overlaps with the prime sentence subject;
				target_direct_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_direct_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_direct_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object;
				target_direct_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object;
				set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
				# lexically overlaps with the prime sentence direct object; or
				target_direct_object[0] == prime_direct_object[0] or
				# semantically overlaps with the prime sentence direct object.
				set([target_direct_object[0], prime_direct_object[0]]) in word_associations
			):
			target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/overlap_random_noun.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Sixth condition: all nouns overlap.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
	while (
			# semantically overlaps with the target sentence verb; or
			set([prime_subject[0], target_verb[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		prime_subject = target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_indirect_object[0], target_verb[0]]) in word_associations or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_indirect_object[0], prime_verb[0]]) in word_associations
		):
		prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
	while (
			# belongs to a category neither verb in prime and target sentences accept; or
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			target_direct_object[2].isdisjoint(target_verb[3]) or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object;
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object;
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations
		):
		prime_direct_object = target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/overlap_all_nouns.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Seventh condition: same verb in prime and target sentences.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences.
	prime_verb = target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			target_subject[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_subject[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_indirect_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_indirect_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
		):
		target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or
			# belongs to a cateogry the target sentence verb does not accept;
			target_direct_object[2].isdisjoint(target_verb[3]) or
			# lexically overlaps with the target sentence indirect object;
			target_direct_object[0] == target_indirect_object[0] or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object;
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object;
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
			# lexically overlaps with the prime sentence direct object; or
			target_direct_object[0] == prime_direct_object[0] or
			# semantically overlaps with the prime sentence direct object.
			set([target_direct_object[0], prime_direct_object[0]]) in word_associations
		):
		target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/overlap_verb.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Eighth condition: determiner overlap.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			# does not share the same article with the prime sentence subject;
			target_subject[1] != prime_subject[1] or
			# lexically overlaps with the prime sentence subject;
			target_subject[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_subject[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_indirect_object[0], prime_verb[0]]) in word_associations or
			# does not share the same article with the prime sentence indirect object;
			target_indirect_object[1] != prime_indirect_object[1] or
			# lexically overlaps with the prime sentence indirect object; or
			target_indirect_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
		):
		target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or
			# belongs to a cateogry the target sentence verb does not accept;
			target_direct_object[2].isdisjoint(target_verb[3]) or
			# lexically overlaps with the target sentence indirect object;
			target_direct_object[0] == target_indirect_object[0] or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object;
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object;
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
			# does not share the same article with the prime sentence direct object;
			target_direct_object[1] != prime_direct_object[1] or
			# lexically overlaps with the prime sentence direct object; or
			target_direct_object[0] == prime_direct_object[0] or
			# semantically overlaps with the prime sentence direct object.
			set([target_direct_object[0], prime_direct_object[0]]) in word_associations
		):
		target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/overlap_determiner.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write(sentence_pair[0][0] + " " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " " + sentence_pair[0][4] + " " + sentence_pair[0][5] + " " + sentence_pair[0][6] + " " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[0][0] + " " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][4] + " " + sentence_pair[0][5] + " " + sentence_pair[0][6] + " " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Ninth condition: prime sentence and target sentence are the same sentence.

subcorpus = set([])

while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences.
	prime_verb = target_verb = choice(verbs)

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
	while (
			# semantically overlaps with the target sentence verb; or
			set([prime_subject[0], target_verb[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		prime_subject = target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_indirect_object[0], target_verb[0]]) in word_associations or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_indirect_object[0], prime_verb[0]]) in word_associations
		):
		prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
	while (
			# belongs to a category neither verb in prime and target sentences accept; or
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			target_direct_object[2].isdisjoint(target_verb[3]) or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object;
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object;
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations
		):
		prime_direct_object = target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

with open("corpus/overlap_all.csv", "w") as file:
	file.write("ppo,pdo,tpo,tdo\n")
	for sentence_pair in subcorpus:
		file.write(sentence_pair[0][0] + " " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " " + sentence_pair[0][4] + " " + sentence_pair[0][5] + " " + sentence_pair[0][6] + " " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[0][0] + " " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][4] + " " + sentence_pair[0][5] + " " + sentence_pair[0][6] + " " + sentence_pair[0][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .\n")

# Tenth condition: different word order.

subcorpus = set([])

# 15000 sentence pair/condition (P/C).
while len(subcorpus) < 15_000:
	# Pick a random verb and assign it to prime and target sentences. Assignment to the target sentence renders the condition in the while-loop redundant, but the combination of assingment and condition helps maintain a compact code. (No do-while in Python, like in the C-family of programming langauges.)
	prime_verb = target_verb = choice(verbs)
	# Keep assigning a random verb to the target sentence, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence verb; or
			target_verb[0] == prime_verb[0] or
			# semantically overlaps with the prime sentence verb.
			set([target_verb[0], prime_verb[0]]) in word_associations
		):
		target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnaam)
	# Keep assinging a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			target_subject[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject; or
			set([target_subject[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb.
			set([target_subject[0], prime_verb[0]]) in word_associations
		):
		target_subject = choice(persoonsnaam)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_indirect_object[0] == prime_subject[0] or

			# lexically overlaps with the target sentence subject;
			prime_indirect_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject; or
			set([prime_indirect_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb.
			set([prime_indirect_object[0], target_verb[0]]) in word_associations
		):
		prime_indirect_object = choice(persoonsnaam)
	# Keep assigning a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or

			# lexically overlaps with the prime sentence subject;
			target_indirect_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_indirect_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_indirect_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object; or
			target_indirect_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object.
			set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
		):
		target_indirect_object = choice(persoonsnaam)
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)
	# Keep assigning a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the prime sentence subject;
			prime_direct_object[0] == prime_subject[0] or
			# belongs to a category the prime sentence verb does not accept;
			prime_direct_object[2].isdisjoint(prime_verb[3]) or
			# lexically overlaps with the prime sentence indirect object;
			prime_direct_object[0] == prime_indirect_object[0] or

			# lexicaly overlaps with the target sentence subject;
			prime_direct_object[0] == target_subject[0] or
			# semantically overlaps with the target sentence subject;
			set([prime_direct_object[0], target_subject[0]]) in word_associations or
			# semantically overlaps with the target sentence verb;
			set([prime_direct_object[0], target_verb[0]]) in word_associations or
			# lexically overlaps with the target sentence indirect object; or
			prime_direct_object[0] == target_indirect_object[0] or
			# semantically overlaps with the target sentence indirect object.
			set([prime_direct_object[0], target_indirect_object[0]]) in word_associations
		):
		prime_direct_object = choice(nouns)
	# Keep assigning a random noun to the target sentence direct object, as long as the previous pick:
	while (
			# lexically overlaps with the target sentence subject;
			target_indirect_object[0] == target_subject[0] or
			# belongs to a cateogry the target sentence verb does not accept;
			target_direct_object[2].isdisjoint(target_verb[3]) or
			# lexically overlaps with the target sentence indirect object;
			target_direct_object[0] == target_indirect_object[0] or

			# lexically overlaps with the prime sentence subject;
			target_direct_object[0] == prime_subject[0] or
			# semantically overlaps with the prime sentence subject;
			set([target_direct_object[0], prime_subject[0]]) in word_associations or
			# semantically overlaps with the prime sentence verb;
			set([target_direct_object[0], prime_verb[0]]) in word_associations or
			# lexically overlaps with the prime sentence indirect object;
			target_direct_object[0] == prime_indirect_object[0] or
			# semantically overlaps with the prime sentence indirect object;
			set([target_direct_object[0], prime_indirect_object[0]]) in word_associations or
			# lexically overlaps with the prime sentence direct object; or
			target_direct_object[0] == prime_direct_object[0] or
			# semantically overlaps with the prime sentence direct object.
			set([target_direct_object[0], prime_direct_object[0]]) in word_associations
		):
		target_direct_object = choice(nouns)

	# Construct abstract prime and target pair.
	sentence_pair = tuple([
		# subject noun article, subject noun, verb, verb preposition, indirect object noun article, indirect object noun, direct object noun article, direct object noun
		tuple([prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]]),
		tuple([target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0]])])

	# If the subcorpus does not contain the recently constructed prime and target pair, then store.
	if sentence_pair not in subcorpus:
		subcorpus.add(sentence_pair)

# Open subcorpus file for writing.
with open("corpus/no_overlap_different_word_order.csv", "w") as file:
	# Write CSV header.
	file.write("ppo,pdo,tpo,tdo\n")
	# Iterate over sentence pairs in the subcorpus and write pairs.
	for sentence_pair in subcorpus:
		# Write prime sentence in prepositional object form (transitive).
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " een " + sentence_pair[0][7] + " .,")
		# Write prime sentence in dative object form (ditransitive).
		file.write("een " + sentence_pair[0][1] + " " + sentence_pair[0][2] + " een " + sentence_pair[0][7] + " " + sentence_pair[0][3] + " een " + sentence_pair[0][5] + " .,")
		# Write target sentence in prepositional object form (transitive).
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " .,")
		# Write target sentence in dative object form (ditransitive).
		file.write(sentence_pair[1][0] + " " + sentence_pair[1][1] + " " + sentence_pair[1][2] + " " + sentence_pair[1][6] + " " + sentence_pair[1][7] + " " + sentence_pair[1][3] + " " + sentence_pair[1][4] + " " + sentence_pair[1][5] + " .\n")