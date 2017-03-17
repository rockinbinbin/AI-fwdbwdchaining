# Robin
# robimeht
# AI Homework 4

import sys
import utils
from collections import deque
import itertools
import Queue
import copy

# Iteration limits
# Stop your search when you reach these limits
FORWARD_LIMIT = 10000
BACKWARD_LIMIT = 10000

# A useful function to get all possible n-permutations of a set of objects
# Returns an iterable generator of permutations
# Google online documentation for further reference
def getPermutations(objList, n):
	return itertools.permutations(objList, n)

'''
Tips:
Use the built-in python "set" class for set operations
	(previously in this course we used Set from the sets module,
	 but the built-in "set" works just as well if not better)
You may create your own parser and object classes if you wish,
	 as long as they are *in this file*. Using the given objects
	 in utils.py is recommended, however.
Use the getPermutations function to construct all possible action arguments,
	 so that you can initialize a list with all possible actions
'''

# *** Create whatever helper functions and classes you need in this space

def forward_search(initial, goal, actions, groundObjects):
	stateQueue = Queue.Queue()
	stateQueue.put([initial, ''])
	actionPermutations = list()
	visitedStates = list()
	for action in actions:
		perms = list(getPermutations(groundObjects, action.numargs))
		for perm in perms:
			inst = action.getInstance(perm)
			actionPermutations.append(inst)
	poppedActions = list()

	while not stateQueue.empty():
		top = stateQueue.get()
		state = top
		parent_action = ''
		if len(top) == 2:
			state = top[0]
			parent_action = top[1]

		if isinstance(parent_action, utils.actionInst):
			poppedActions.append(parent_action)

		applicableActions = set()
		for action in actionPermutations:
			preconditions = action.getPrecond()
			if preconditions.issubset(state):
				applicableActions.add(action)

		for action in applicableActions:
			unchanged_state = copy.deepcopy(state)
			addSet = action.getAdd()
			deleteSet = action.getDelete()
			for obj in addSet:
				unchanged_state.add(obj)
			for obj in deleteSet:
				if obj in unchanged_state:
					unchanged_state.remove(obj)

			if goal.issubset(unchanged_state): #goal-test
				end = action
				path = [end]
				for parent in poppedActions:
					path.append(parent)
				path.reverse()
				return True, path
			else:
				if unchanged_state not in visitedStates:
					stateQueue.put([unchanged_state, action])
			visitedStates.append(unchanged_state)
	return False, []

# Returns true if a plan is found, along with a list of actionInst objects that forms the plan
# Returns false otherwise, with an empty list
# initial, goal, and groundObjects are sets, and actions is a list
def backward_search(initial, goal, actions, groundObjects):
	stateQueue = Queue.Queue()
	stateQueue.put([goal, ''])
	actionPermutations = list()
	visitedStates = list()
	for action in actions:
		perms = list(getPermutations(groundObjects, action.numargs))
		for perm in perms:
			inst = action.getInstance(perm)
			actionPermutations.append(inst)
	poppedActions = list()

	while not stateQueue.empty():
		top = stateQueue.get()
		state = top
		parent_action = ''
		if len(top) == 2:
			state = top[0]
			parent_action = top[1]

		if isinstance(parent_action, utils.actionInst):
			poppedActions.append(parent_action)

		applicableActions = set()
		for action in actionPermutations:
			addSet = action.getAdd()
			deleteSet = action.getDelete()
			satisfied = False
			for predicate in addSet: #all addList predicates should be subset of state
				if predicate in state:
					satisfied = True
				else:
					satisfied = False
					break
			if satisfied:
				for predicate in deleteSet: #all deleteList predicates should NOT be subset of state
					if not predicate in state:
						satisfied = True
					else:
						satisfied = False
						break
			if satisfied:
				applicableActions.add(action)

		for action in applicableActions:
			preconditions = action.getPrecond()
			unchanged_state = copy.deepcopy(state)
			for obj in addSet:
				if obj in unchanged_state:
					unchanged_state.remove(obj)
			for precondition in preconditions:
				unchanged_state.add(precondition)

			if initial.issubset(unchanged_state): #goal-test
				end = action
				path = [end]
				for parent in poppedActions:
					path.append(parent)
				path.reverse()
				return True, path
			else:
				if unchanged_state not in visitedStates:
					stateQueue.put([unchanged_state, action])
			visitedStates.append(unchanged_state)
	return False, []

# Do not modify the following
if __name__=='__main__':
	assert(len(sys.argv) == 3)
	stype = sys.argv[1]
	fname = sys.argv[2]
	initial, goal, actions, groundObjects = utils.parse(fname)

	print "Actions"
	for a in actions:
		print str(a)
	print "\nInitial\n"
	for i in initial:
		print str(i)
	print "\nGoal\n"
	for g in goal:
		print str(g)
	print '\n'

	if stype == 'forward':
		foundPlan, plan = forward_search(initial, goal, actions, groundObjects)
		print foundPlan
		for a in plan:
			print str(a)
	elif stype == 'backward':
		foundPlan, plan = backward_search(initial, goal, actions, groundObjects)
		print foundPlan
		for a in plan:
			print str(a)
