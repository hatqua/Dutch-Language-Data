# This script processes the raw word associations data. Each line in the word associations file contains a cue and three associates of the cue. In total, the combination of four words, one cue and three associates, yields six permutations of unordered word pairs. This script calculates those permutations and stores the result in a new file.

# (!) The final result of calculating the permutations. A set because a Python set handles duplicates automagically ({apple, orange} = {orange, apple}). That is, this script writes only one instance of an unordered pair to the output file.
result = set([])

# Open raw word associations file for reading.
with open("data/raw_word_associations.csv", "r") as file:
	# Skip CSV header.
	file.readline()
	# Process file line by line.
	for line in file:
		# Extract all field values.
		parts = line.split("\",\"")
		# Clean last associate.
		parts[5] = parts[5][:-2]
		# The following conditional exception raising served the purpose of testing whether the file is a valid CSV file containing one cue and three associates per line.
		# if len(parts) > 6:
		#	raise Exception("line length greater than 6: " + line)
		# Calcuate and store the six permutations. See comment line tagged with (!). frozenset because Python compalins about set not being hashable.
		result.add(frozenset([parts[2], parts[3]]))
		result.add(frozenset([parts[2], parts[4]]))
		result.add(frozenset([parts[2], parts[5]]))
		result.add(frozenset([parts[3], parts[4]]))
		result.add(frozenset([parts[3], parts[5]]))
		result.add(frozenset([parts[4], parts[5]]))

# A temporary placeholder for serialized pairs.
tmp = ""

# Open the output file for writing, truncating the file if it exists, but creating the file if it doesn't exist.
with open("data/word_associations.csv", "w") as file:
	# Write the CSV header. Two arbitrary column names. These are unordered pairs after all.
	file.write("x,y\n")
	# Iterate over the pairs in the final result.
	for pair in result:
		# Serialize the pair by joining both elements of the pair by a comma.
		tmp = ",".join(pair)
		# Check if the pair contains more than one comma. That is, if at least one member of the pair is a comma-containing-word/phrase/sentence.
		if tmp.count(",") == 1:
			# If not, then write the serialized pair to the output file and terminate the CSV line.
			file.write(tmp)
			file.write("\n")