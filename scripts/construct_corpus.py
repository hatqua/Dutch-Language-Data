# This is the script that builds the corpus. This script has many dependencies that are CSV files.
# This script is not the most perfect piece of code ever written, because it contains lots of code duplication. This is more of a coarse piece of code, one that needs some refinment. Nevertheless, this script is a one-time-use kind of script. (Due to some tight deadlines that I came up with, I could not refine it.)

from random import choice, sample
from pathlib import Path

class Sentence:
	"""
	A sentence consists of a subject + article (de/het), a verb + preposition, an indirect object + article, and a direct object + article.
	"""
	def __init__(self, subject_article: str, subject_noun: str, verb_form: str, verb_preposition: str, indirect_object_article: str, indirect_object_noun: str, direct_object_article: str, direct_object_noun: str):
		"""
		Construct a sentence given the elements.
		"""
		self.subject_article = subject_article
		self.subject_noun = subject_noun
		self.verb_form = verb_form
		self.verb_preposition = verb_preposition
		self.indirect_object_article = indirect_object_article
		self.indirect_object_noun = indirect_object_noun
		self.direct_object_article = direct_object_article
		self.direct_object_noun = direct_object_noun
		self.hash = self.serialize_dopo().__hash__()
	
	def __eq__(self, value) -> bool:
		"""
		Check two sentences for equality.
		"""
		return	type(value) == Sentence and self.hash == value.hash
	
	def __hash__(self):
		return self.hash

	def serialize_iodo(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize setnence in ditransitive form (subject, verb, indirect object, direct object).
		"""
		return	(self.subject_article if definite_subject else "een") + " " + \
				self.subject_noun + " " + \
				self.verb_form + " " + \
				(self.indirect_object_article if definite_indirect_object else "een") + " " + \
				self.indirect_object_noun + " " + \
				(self.direct_object_article if definite_direct_object else "een") + " " + \
				self.direct_object_noun
	
	def serialize_podo(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in transitive form, where the prepositional (indirect) object precedes the direct object (subject, verb, preposition, indirect object, direct object).
		"""
		return	(self.subject_article if definite_subject else "een") + " " + \
				self.subject_noun + " " + \
				self.verb_form + " " + \
				self.verb_preposition + " " + \
				(self.indirect_object_article if definite_indirect_object else "een") + " " + \
				self.indirect_object_noun + " " + \
				(self.direct_object_article if definite_direct_object else "een") + " " + \
				self.direct_object_noun
	
	def serialize_dopo(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in transitive form, where the prepositional (indirect) object succeeds the direct object (subject, verb, direct object, preposition, indirect object).
		"""
		return	(self.subject_article if definite_subject else "een") + " " + \
				self.subject_noun + " " + \
				self.verb_form + " " + \
				(self.direct_object_article if definite_direct_object else "een") + " " + \
				self.direct_object_noun + " " + \
				self.verb_preposition + " " + \
				(self.indirect_object_article if definite_indirect_object else "een") + " " + \
				self.indirect_object_noun
	
	def serialize_io_random_token(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in ditransitive form, with a random order of the tokens.
		"""
		return " ".join(sample([
			(self.subject_article if definite_subject else "een"),
			self.subject_noun,
			self.verb_form,
			(self.indirect_object_article if definite_indirect_object else "een"),
			self.indirect_object_noun,
			(self.direct_object_article if definite_direct_object else "een"),
			self.direct_object_noun
		], k=7))
	
	def serialize_io_random_constituent(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in ditransitive form, with a random order of the constituents.
		"""
		return " ".join(sample([
			(self.subject_article if definite_subject else "een") + " " + self.subject_noun,
			self.verb_form,
			(self.indirect_object_article if definite_indirect_object else "een") + " " + self.indirect_object_noun,
			(self.direct_object_article if definite_direct_object else "een") + " " + self.direct_object_noun
		], k=4))

	def serialize_po_random_token(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in transitive form, with a random order of the tokens.
		"""
		return " ".join(sample([
			(self.subject_article if definite_subject else "een"),
			self.subject_noun,
			self.verb_form,
			self.verb_preposition,
			(self.indirect_object_article if definite_indirect_object else "een"),
			self.indirect_object_noun,
			(self.direct_object_article if definite_direct_object else "een"),
			self.direct_object_noun
		], k=8))

	def serialize_po_random_constituent(self, definite_subject: bool=True, definite_indirect_object: bool=True, definite_direct_object: bool=True) -> str:
		"""
		Serialize sentence in transitive form, with a random order of the constituents.
		"""
		return " ".join(sample([
			(self.subject_article if definite_subject else "een") + " " + self.subject_noun,
			self.verb_form,
			self.verb_preposition + " " + (self.indirect_object_article if definite_indirect_object else "een") + " " + self.indirect_object_noun,
			(self.direct_object_article if definite_direct_object else "een") + " " + self.direct_object_noun
		], k=4))

class SentencePair:
	"""
	A pair comprising a prime sentence and a target sentence.
	"""
	def __init__(self, prime: Sentence, target: Sentence):
		self.prime = prime
		self.target = target
		self.hash = self.serialize_prime_dopo_target_podo().__hash__()
	
	def __eq__(self, value) -> bool:
		return type(value) == SentencePair and self.hash == value.hash
	
	def __hash__(self):
		return self.hash

	def serialize_prime_io_random_token_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_io_random_token_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_io_random_token_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_io_random_constituent_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_io_random_constituent_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_io_random_constituent_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_io_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_po_random_token_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_po_random_token_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_po_random_token_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_token(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_po_random_constituent_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_po_random_constituent_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_po_random_constituent_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_po_random_constituent(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_iodo_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_iodo_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_iodo_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_podo_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_podo_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_podo_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	

	def serialize_prime_dopo_target_iodo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_iodo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_dopo_target_podo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_podo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)
	
	def serialize_prime_dopo_target_dopo(self, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> str:
		return self.prime.serialize_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object) + ", " + self.target.serialize_dopo(definite_target_subject, definite_target_indirect_object, definite_target_direct_object)

class SentencePairCorpus(set[SentencePair]):
	"""
	A simple extension of set[SentencePair], with a serialization functionality.
	"""
	def __init__(self):
		super().__init__()
	
	def serialize(self, directory: Path, name: str, definite_prime_subject: bool=True, definite_prime_indirect_object: bool=True, definite_prime_direct_object: bool=True, definite_target_subject: bool=True, definite_target_indirect_object: bool=True, definite_target_direct_object: bool=True) -> None:
		if not directory.exists():
			directory.mkdir()
		else:
			if directory.is_file():
				raise Exception("directory is a file")
	
		prime_io_random_token_target_iodo = open(directory.joinpath(name + "_prime_io_random_token_target_iodo"), "w")
		prime_io_random_token_target_podo = open(directory.joinpath(name + "_prime_io_random_token_target_podo"), "w")
		prime_io_random_token_target_dopo = open(directory.joinpath(name + "_prime_io_random_token_target_dopo"), "w")
		prime_io_random_constituent_target_iodo = open(directory.joinpath(name + "_prime_io_random_constituent_target_iodo"), "w")
		prime_io_random_constituent_target_podo = open(directory.joinpath(name + "_prime_io_random_constituent_target_podo"), "w")
		prime_io_random_constituent_target_dopo = open(directory.joinpath(name + "_prime_io_random_constituent_target_dopo"), "w")
		prime_po_random_token_target_iodo = open(directory.joinpath(name + "_prime_po_random_token_target_iodo"), "w")
		prime_po_random_token_target_podo = open(directory.joinpath(name + "_prime_po_random_token_target_podo"), "w")
		prime_po_random_token_target_dopo = open(directory.joinpath(name + "_prime_po_random_token_target_dopo"), "w")
		prime_po_random_constituent_target_iodo = open(directory.joinpath(name + "_prime_po_random_constituent_target_iodo"), "w")
		prime_po_random_constituent_target_podo = open(directory.joinpath(name + "_prime_po_random_constituent_target_podo"), "w")
		prime_po_random_constituent_target_dopo = open(directory.joinpath(name + "_prime_po_random_constituent_target_dopo"), "w")
		prime_iodo_target_iodo = open(directory.joinpath(name + "_prime_iodo_target_iodo"), "w")
		prime_iodo_target_podo = open(directory.joinpath(name + "_prime_iodo_target_podo"), "w")
		prime_iodo_target_dopo = open(directory.joinpath(name + "_prime_iodo_target_dopo"), "w")
		prime_podo_target_iodo = open(directory.joinpath(name + "_prime_podo_target_iodo"), "w")
		prime_podo_target_podo = open(directory.joinpath(name + "_prime_podo_target_podo"), "w")
		prime_podo_target_dopo = open(directory.joinpath(name + "_prime_podo_target_dopo"), "w")
		prime_dopo_target_iodo = open(directory.joinpath(name + "_prime_dopo_target_iodo"), "w")
		prime_dopo_target_podo = open(directory.joinpath(name + "_prime_dopo_target_podo"), "w")
		prime_dopo_target_dopo = open(directory.joinpath(name + "_prime_dopo_target_dopo"), "w")

		for sentence_pair in self:
			prime_io_random_token_target_iodo.write(sentence_pair.serialize_prime_io_random_token_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_token_target_iodo.write("\n")
			prime_io_random_token_target_podo.write(sentence_pair.serialize_prime_io_random_token_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_token_target_podo.write("\n")
			prime_io_random_token_target_dopo.write(sentence_pair.serialize_prime_io_random_token_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_token_target_dopo.write("\n")
			prime_io_random_constituent_target_iodo.write(sentence_pair.serialize_prime_io_random_constituent_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_constituent_target_iodo.write("\n")
			prime_io_random_constituent_target_podo.write(sentence_pair.serialize_prime_io_random_constituent_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_constituent_target_podo.write("\n")
			prime_io_random_constituent_target_dopo.write(sentence_pair.serialize_prime_io_random_constituent_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_io_random_constituent_target_dopo.write("\n")
			prime_po_random_token_target_iodo.write(sentence_pair.serialize_prime_po_random_token_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_token_target_iodo.write("\n")
			prime_po_random_token_target_podo.write(sentence_pair.serialize_prime_po_random_token_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_token_target_podo.write("\n")
			prime_po_random_token_target_dopo.write(sentence_pair.serialize_prime_po_random_token_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_token_target_dopo.write("\n")
			prime_po_random_constituent_target_iodo.write(sentence_pair.serialize_prime_po_random_constituent_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_constituent_target_iodo.write("\n")
			prime_po_random_constituent_target_podo.write(sentence_pair.serialize_prime_po_random_constituent_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_constituent_target_podo.write("\n")
			prime_po_random_constituent_target_dopo.write(sentence_pair.serialize_prime_po_random_constituent_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_po_random_constituent_target_dopo.write("\n")
			prime_iodo_target_iodo.write(sentence_pair.serialize_prime_iodo_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_iodo_target_iodo.write("\n")
			prime_iodo_target_podo.write(sentence_pair.serialize_prime_iodo_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_iodo_target_podo.write("\n")
			prime_iodo_target_dopo.write(sentence_pair.serialize_prime_iodo_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_iodo_target_dopo.write("\n")
			prime_podo_target_iodo.write(sentence_pair.serialize_prime_podo_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_podo_target_iodo.write("\n")
			prime_podo_target_podo.write(sentence_pair.serialize_prime_podo_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_podo_target_podo.write("\n")
			prime_podo_target_dopo.write(sentence_pair.serialize_prime_podo_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_podo_target_dopo.write("\n")
			prime_dopo_target_iodo.write(sentence_pair.serialize_prime_dopo_target_iodo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_dopo_target_iodo.write("\n")
			prime_dopo_target_podo.write(sentence_pair.serialize_prime_dopo_target_podo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_dopo_target_podo.write("\n")
			prime_dopo_target_dopo.write(sentence_pair.serialize_prime_dopo_target_dopo(definite_prime_subject, definite_prime_indirect_object, definite_prime_direct_object, definite_target_subject, definite_target_indirect_object, definite_target_direct_object))
			prime_dopo_target_dopo.write("\n")
		
		prime_io_random_token_target_iodo.close()
		prime_io_random_token_target_podo.close()
		prime_io_random_token_target_dopo.close()
		prime_io_random_constituent_target_iodo.close()
		prime_io_random_constituent_target_podo.close()
		prime_io_random_constituent_target_dopo.close()
		prime_po_random_token_target_iodo.close()
		prime_po_random_token_target_podo.close()
		prime_po_random_token_target_dopo.close()
		prime_po_random_constituent_target_iodo.close()
		prime_po_random_constituent_target_podo.close()
		prime_po_random_constituent_target_dopo.close()
		prime_iodo_target_iodo.close()
		prime_iodo_target_podo.close()
		prime_iodo_target_dopo.close()
		prime_podo_target_iodo.close()
		prime_podo_target_podo.close()
		prime_podo_target_dopo.close()
		prime_dopo_target_iodo.close()
		prime_dopo_target_podo.close()
		prime_dopo_target_dopo.close()

word_associations = set([]) # This set will contain all word associations as unordered pairs. A pair denotes that two lemma forms are semantically related.
# Common nouns that are not persoonsnaam.
nouns = []
# Common nouns that are persoonsnaam.
persoonsnamen = []
# Verbs.
verbs = []

# Stuff!
abstract = set(["abstract"])

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
		# Split the line extracting field values: lemma, article, and categories. The last field is a colon-separated list of categories to which the noun belongs.
		parts = line[:-1].split(",")
		# Calculate categories.
		categories = set(parts[2].split(";")) - abstract
		# If noun belongs to persoonsnaam, among others, add noun to the list of persoonsnamen only.
		if "persoonsnaam" in categories:
			# Add a record comprising the following fields: lemma, article, and list of semantic categories to which the persoonsnaam (lemma) belongs.
			persoonsnamen.append(tuple([parts[0], parts[1], categories]))
		# Otherwise, add noun to the list of nouns.
		else:
			# Add a record comprising the following fields: lemma, article, and list of semantic categories to which the noun (lemma) belongs.
			nouns.append(tuple([parts[0], parts[1], categories]))

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

corpus_path = Path("corpus")

# Start constructing subcorpora, condition after another.

# First condition: definitely no overlap of any kind whatsoever, absolutely (not).

# Stores subcorpora.
subcorpus = SentencePairCorpus()

# 1000 sentence pair/condition (P/C).
while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	# However, it could be the case that the 100th attempt was successful, and it remains ambiguous whether the 100th attempt was successful without (additional) check(s) in the previous while-loop and/or in the following if-clause. Nevertheless, this design is more simple. Besides, efficiency is not the a strict requirement in this script, since this is a one-time-use script.
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnamen)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			)
		):
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable persoonsnaam. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable noun. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue

	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	# If the previous while-loop made 100 attemps, then the while-loop potentially failed to pick randomly a suitable noun. In this case, skip this subcorpus iteration (try again by resetting the counter and randomly picking new verbs).
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "no_overlap", False, False, False, True, True, True)

# Second condition: verbs are semantically related.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			)
		):
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue

	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
		continue

	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "semantic_similarity_verb", False, False, False, True, True, True)

# Third condition: corresponding nouns across prime and target are semanticaly related.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
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
		target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "semantic_similarity_nouns", False, False, False, True, True, True)

# Fourth condition: the verbs and corresponding nouns across prime and target are semanticaly related.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
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
		target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
		continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
		continue
	
	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
	if count >= 100:
		continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "semantic_similarity_all", False, False, False, True, True, True)

# Fifth condition: random noun overlap.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	# Check if this script choose subject overlap for this iteration.
	if noun_choice == 1:
		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
		while (
				count < 100 and (
					# semantically overlaps with the target sentence verb; or
					set([prime_subject[0], target_verb[0]]) in word_associations or
					# semantically overlaps with the prime sentence verb.
					set([target_subject[0], prime_verb[0]]) in word_associations
				)
			):
			prime_subject = target_subject = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue
	else:
		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
		while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
			prime_subject = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue
	
		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
		while (
				count < 100 and (
					# lexically overlaps with the prime sentence subject;
					target_subject[0] == prime_subject[0] or
					# semantically overlaps with the prime sentence subject; or
					set([target_subject[0], prime_subject[0]]) in word_associations or
					# semantically overlaps with the prime sentence verb.
					set([target_subject[0], prime_verb[0]]) in word_associations
				)
			):
			target_subject = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	# Check if this script choose indirect object overlap for this iteration.
	if noun_choice == 2:
		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
		while (
				count < 100 and (
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
				)
			):
			prime_indirect_object = target_indirect_object = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue
	else:
		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
		while (
				count < 100 and (
					# lexically overlaps with the prime sentence subject;
					prime_indirect_object[0] == prime_subject[0] or

					# lexically overlaps with the target sentence subject;
					prime_indirect_object[0] == target_subject[0] or
					# semantically overlaps with the target sentence subject; or
					set([prime_indirect_object[0], target_subject[0]]) in word_associations or
					# semantically overlaps with the target sentence verb.
					set([prime_indirect_object[0], target_verb[0]]) in word_associations
				)
			):
			prime_indirect_object = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue

		count = 0
		# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
					# semantically overlaps with the prime sentence indirect object.
					set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
				)
			):
			target_indirect_object = choice(persoonsnamen)
			count = count + 1
		if count >= 100:
			continue

	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	# Check if this script choose direct object overlap for this iteration.
	if noun_choice == 3:
		count = 0
		# Attempt at most 100 times to assign a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
		while (
				count < 100 and (
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
				)
			):
			prime_direct_object = target_direct_object = choice(nouns)
			count = count + 1
		if count >= 100:
			continue
	else:
		count = 0
		# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
		while (
				count < 100 and (
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
				)
			):
			prime_direct_object = choice(nouns)
			count = count + 1
		if count >= 100:
			continue

		count = 0
		# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
		while (
				count < 100 and (
					# lexically overlaps with the target sentence subject;
					target_direct_object[0] == target_subject[0] or
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
				)
			):
			target_direct_object = choice(nouns)
			count = count + 1
		if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "lexical_overlap_random_noun", False, False, False, True, True, True)

# Sixth condition: all nouns overlap.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
	while (
			count < 100 and (
				# semantically overlaps with the target sentence verb; or
				set([prime_subject[0], target_verb[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		prime_subject = target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_indirect_object = target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = target_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "lexical_overlap_all_nouns", False, False, False, True, True, True)

# Seventh condition: same verb in prime and target sentences.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
	# Pick a random verb and assign it to prime and target sentences.
	prime_verb = target_verb = choice(verbs)
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and  set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			)
		):
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "lexical_overlap_verb", False, False, False, True, True, True)

# Eighth condition: determiner overlap.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence subject, as long as the previous pick semantically overlaps with the target sentence verb.
	while count < 100 and set([prime_subject[0], target_verb[0]]) in word_associations:
		prime_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# does not share the same article with the prime sentence subject;
				target_subject[1] != prime_subject[1] or
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject; or
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject; or
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb.
				set([prime_indirect_object[0], target_verb[0]]) in word_associations
			)
		):
		prime_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence indirect object, as long as the previous pick:
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
				# does not share the same article with the prime sentence indirect object;
				target_indirect_object[1] != prime_indirect_object[1] or
				# lexically overlaps with the prime sentence indirect object; or
				target_indirect_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			)
		):
		target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
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
			)
		):
		target_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "lexical_overlap_determiner", True, True, True, True, True, True)

# Ninth condition: prime sentence and target sentence are the same sentence.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
	# Pick a random verb and assign it to prime and target sentences.
	prime_verb = target_verb = choice(verbs)

	# Pick a random persoonsnaam and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence subjects, as long as the previous pick:
	while (
			count < 100 and (
				# semantically overlaps with the target sentence verb; or
				set([prime_subject[0], target_verb[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb.
				set([target_subject[0], prime_verb[0]]) in word_associations
			)
		):
		prime_subject = target_subject = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to prime sentence and target sentence indirect objects, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_indirect_object = target_indirect_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random noun and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to prime sentence and target sentence direct objects, as long as the previous pick:
	while (
			count < 100 and (
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
			)
		):
		prime_direct_object = target_direct_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "lexical_overlap_all", True, True, True, True, True, True)

# Tenth condition: semantic dissonance.

subcorpus = SentencePairCorpus()

while len(subcorpus) < 1000:
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
	
	# Pick a random noun and assign it to prime sentence and target sentence subjects.
	prime_subject = target_subject = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# semantically overlaps with the prime sentence verb;
				set([prime_subject[0], prime_verb[0]]) in word_associations or
				# belongs to a cateogry the prime sentence verb accepts;
				prime_subject[2] & prime_verb[3] or
				# semantically overlaps with the target sentence verb; or
				set([prime_subject[0], target_verb[0]]) in word_associations or
				# belongs to a cateogry the target sentence verb accepts;
				prime_subject[2] & target_verb[3]
			)
		):
		prime_subject = choice(nouns)
		count = count + 1
	if count >= 100:
			continue
	
	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence subject, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				target_subject[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_subject[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_subject[0], prime_verb[0]]) in word_associations or
				# belongs to a cateogry the prime sentence verb accepts;
				target_subject[2] & prime_verb[3] or

				# semantically overlaps with the target sentence verb; or
				set([target_subject[0], target_verb[0]]) in word_associations or
				# belongs to a cateogry the target sentence verb accepts.
				target_subject[2] & target_verb[3]
			)
		):
		target_subject = choice(nouns)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random noun and assign it to prime sentence and target sentence indirect objects.
	prime_indirect_object = target_indirect_object = choice(nouns)

	count = 0
	# Attempt at most 100 times to assign a random noun to the prime sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([prime_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([prime_indirect_object[0], prime_verb[0]]) in word_associations or
				# belongs to a cateogry the prime sentence verb accepts;
				prime_indirect_object[2] & prime_verb[3] or

				# lexically overlaps with the target sentence subject;
				prime_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([prime_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb; or
				set([prime_indirect_object[0], target_verb[0]]) in word_associations or
				# belongs to a cateogry the target sentence verb accepts.
				prime_indirect_object[2] & target_verb[3]
			)
		):
		prime_indirect_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random noun to the target sentence indirect object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_indirect_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([target_indirect_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb;
				set([target_indirect_object[0], target_verb[0]]) in word_associations or
				# belongs to a cateogry the target sentence verb accepts;
				target_indirect_object[2] & target_verb[3] or

				# lexically overlaps with the prime sentence subject;
				target_indirect_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([target_indirect_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([target_indirect_object[0], prime_verb[0]]) in word_associations or
				# belongs to a cateogry the prime sentence verb accepts;
				target_indirect_object[2] & prime_verb[3] or
				# lexically overlaps with the prime sentence indirect object; or
				target_indirect_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object.
				set([target_indirect_object[0], prime_indirect_object[0]]) in word_associations
			)
		):
		target_indirect_object = choice(nouns)
		count = count + 1
	if count >= 100:
			continue
	
	# Pick a random persoonsnaam and assign it to prime sentence and target sentence direct objects.
	prime_direct_object = target_direct_object = choice(persoonsnamen)

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the prime sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the prime sentence subject;
				prime_direct_object[0] == prime_subject[0] or
				# semantically overlaps with the prime sentence subject;
				set([prime_direct_object[0], prime_subject[0]]) in word_associations or
				# semantically overlaps with the prime sentence verb;
				set([prime_direct_object[0], prime_verb[0]]) in word_associations or
				# lexically overlaps with the prime sentence indirect object;
				prime_direct_object[0] == prime_indirect_object[0] or
				# semantically overlaps with the prime sentence indirect object;
				set([prime_direct_object[0], prime_indirect_object[0]]) in word_associations or

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
			)
		):
		prime_direct_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	count = 0
	# Attempt at most 100 times to assign a random persoonsnaam to the target sentence direct object, as long as the previous pick:
	while (
			count < 100 and (
				# lexically overlaps with the target sentence subject;
				target_direct_object[0] == target_subject[0] or
				# semantically overlaps with the target sentence subject;
				set([target_direct_object[0], target_subject[0]]) in word_associations or
				# semantically overlaps with the target sentence verb;
				set([target_direct_object[0], target_verb[0]]) in word_associations or
				# lexically overlaps with the target sentence indirect object;
				target_direct_object[0] == target_indirect_object[0] or
				# semantically overlaps with the target sentence indirect object;
				set([target_direct_object[0], target_indirect_object[0]]) in word_associations or

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
			)
		):
		target_direct_object = choice(persoonsnamen)
		count = count + 1
	if count >= 100:
			continue

	# Construct abstract prime and target pair.
	subcorpus.add(SentencePair(
		Sentence(prime_subject[1], prime_subject[0], prime_verb[1], prime_verb[2], prime_indirect_object[1], prime_indirect_object[0], prime_direct_object[1], prime_direct_object[0]),
		Sentence(target_subject[1], target_subject[0], target_verb[1], target_verb[2], target_indirect_object[1], target_indirect_object[0], target_direct_object[1], target_direct_object[0])
	))

subcorpus.serialize(corpus_path, "semantic_dissonance", False, False, False, True, True, True)