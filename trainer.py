'''
trainer.py
----------

This file contains functions and classes that, given evidence
on transitions between states, will generate a probability
matrix used for the Markov Chain Monte Carlo (MCMC) simulation
'''

from ConfigParser import SafeConfigParser
import seaborn as sb

class Trainer:
	'''
	Models the probability that a single state will transition
	to any other state. Constructs a single list with `num_states`
	entries representing the probs of transitioning to states
	with that index.

	Currently, the probability is modeled as a very straightforward
	Dirichlet distribution approximation: for each observation, we
	add 1 to its category, and then, when generating probabilities,
	we simply normalize across all of our observations. Eg: if we
	had 3 possible transitions, and we saw 1 of type 1, 2 of type 2,
	and 1 of type 3, we would output [0.25, 0.5, 0.25].

	Note: Actually, we don't quite do that, because we add a small
	initial weight to all categories, to assume that any transition
	is possible; this gets ironed out if we have significant amounts
	of data.
	'''

	def __init__(self, num_states=None, initial_weight=0.2):

		# If no num_states is passed, load it from the config
		if num_states == None:
			cfg = SafeConfigParser()
			cfg.read("config.cfg")
			num_states = cfg.getint("modeling", "num_states")

		self.priors = [initial_weight for i in range(num_states)]

	def update(self, evidence):
		'''
		Takes an int index or list of indices representing
		the states that have been observed transitioned to
		and updates the model with that new evidence.
		'''

		if isinstance(evidence, int):
			self.priors[evidence] += 1
		elif isinstance(evidence, list):
			for prior_index in evidence:
				self.priors[prior_index] += 1
		else:
			raise ValueError(
				"Evidence passed to Bayes is neither an int nor list of ints"
			)

	def output(self):
		''' Return the probability distribution. '''
		return normalize(self.priors)

def visualize(data):
	'''
	Plots a list of lists (matrix) as a heatmap.
	'''

	sb.heatmap(data, square=True, xticklabels=2, yticklabels=2,linewidths=.5)
	sb.plt.show()

def normalize(value_list):
	'''
	Normalizes the values in a list so that the sum
	of the returned list is one.
	'''

	total = sum(value_list)
	return [el/total for el in value_list]

# Testing code
if __name__ == "__main__":
	b = Trainer()
	evidence = [0, 0, 1, 2, 5, 7, 16, 16, 17]
	b.update(evidence)
	print b.output()
	visualize([b.output()])
