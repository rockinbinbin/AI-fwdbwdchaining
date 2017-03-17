# utils.py
# Classes and functions for reading pddl files

'''
All objects have overloaded equality, hashing, and string operators
So you can call
	str(o)
	hash(o)
	o == p
for any objects o, p of the below types, and also insert them into sets

Read this file carefully so you understand what data types and structures
are being used.

You are not required to use this file, but all your own code should go in plan.py
'''

# Represents a constant object in the problem
class groundObject:
	def __init__(self, name):
		self.name = name

	def __eq__(self, other):
		return (self.name == other.name)

	def __hash__(self):
		return hash(self.name)

	def __str__(self):
		return str(self.name)

# Represents a predicate
class predicate:
	def __init__(self, name, args):
		self.name = name #Name of predicate
		self.args = tuple(args) #List of things

	def get_string(self):
		string = self.name + ' '
		for a in self.args:
			string += str(a) + ' '
		return string

	def __eq__(self, other):
		return ((self.name == other.name) and (self.args == other.args))

	def __hash__(self):
		return hash((self.name, self.args))

	def __str__(self):
		return self.get_string()

# Represents an *instance* of an action
class actionInst:
	def __init__(self, parent, args, precond, addset, delset):
		self.parent = parent
		self.args = tuple(args)
		self.precond = precond
		self.addset = addset
		self.delset = delset

	def getPrecond(self):
		return self.precond

	def getAdd(self):
		return self.addset

	def getDelete(self):
		return self.delset

	def getName(self):
		return self.parent.name

	def getFullName(self):
		outstr = ''
		outstr += self.parent.name+' '
		for i in range(len(self.args)):
			outstr += str(self.args[i]) + ' '
		return outstr

	def getPrecondStr(self):
		outstr = ""
		for p in self.precond:
		 	outstr += str(p)+' '
		return outstr

	def __eq__(self, other):
		return ((self.parent == other.parent) and (self.args == other.args))

	def __hash__(self):
		return hash((self.parent, self.args))
	
	def __str__(self):
		outstr = ''
		outstr += self.parent.name+' '
		for i in range(len(self.args)):
			outstr += str(self.args[i]) + ' '
		outstr += '\n   precond: '
		for p in self.precond:
		 	outstr += str(p)+', '
		outstr += '\n   add: '
		for a in self.addset:
		 	outstr += str(a)+', '
		outstr += '\n   delete: '
		for a in self.delset:
		 	outstr += str(a)+', '
		outstr += '\n'
		return outstr

# Represents a general action template
class action:
	def __init__(self, name, args, precond, addset, delset):
		self.name = name
		self.numargs = len(args)
		self.precond = set([predicate(p.name, \
				[args.index(var) for var in p.args]) \
				for p in precond])
		self.addset = set([predicate(p.name, \
				[args.index(var) for var in p.args]) \
				for p in addset])
		self.delset = set([predicate(p.name, \
				[args.index(var) for var in p.args]) \
				for p in delset])

	# Create an instance of this action with the given arguments
	def getInstance(self, args):
		assert(len(args) == self.numargs)
		instPrecond = set([predicate(p.name, [args[i] for i in p.args]) for p in self.precond])
		instAddset = set([predicate(p.name, [args[i] for i in p.args]) for p in self.addset])
		instDelset = set([predicate(p.name, [args[i] for i in p.args]) for p in self.delset])
		return actionInst(self, args, instPrecond, instAddset, instDelset)

	def printAction(self):
		print self.get_string()

	def __str__(self):
		return self.get_string()

	def get_string(self):
		outstr = ''
		outstr += self.name+' '
		for i in range(self.numargs):
			outstr += str(i) + ' '
		outstr += '\n   precond: '
		for p in self.precond:
		 	outstr += str(p)+', '
		outstr += '\n   add: '
		for a in self.addset:
		 	outstr += str(a)+', '
		outstr += '\n   delete: '
		for a in self.delset:
		 	outstr += str(a)+', '
		outstr += '\n'
		return outstr
	 	
	def getNumArgs(self):
		return self.numargs

	def __hash__(self):
		return hash((self.name, self.numargs))

	def __eq__(self, other):
		return ((self.name == other.name) and (self.numargs == other.numargs))


# Return an initial state, a goal, a list of general actions, and set of ground objects
def parse(filename):
	initial = set()
	goal = set()
	groundObjs = set()
	actions = []
	with open(filename, 'r') as fobj:
		lines = fobj.read().splitlines()
		initial_state = lines[0].split(';')
		for l in initial_state:
			pred = l.split(',')
			predname = pred[0].split()[0]
			predargs = pred[1].split()
			predargsObj = [groundObject(n) for n in predargs]
			initial.add(predicate(predname, predargsObj))
			groundObjs = groundObjs.union(set(predargsObj))

		goal_state = lines[1].split(';')
		for l in goal_state:
			pred = l.split(',')
			predname = pred[0].split()[0]
			predargs = pred[1].split()
			predargsObj = [groundObject(n) for n in predargs]
			goal.add(predicate(predname, predargsObj))
			groundObjs = groundObjs.union(set(predargsObj))

		for i in range(2,len(lines)):
			preconds = set()
			adds = set()
			deletes = set()

			parts = lines[i].split('|') # Should be 4 parts
			actDef = parts[0].split(',')
			actname = actDef[0].split()[0]
			actargs = [groundObject(n) for n in actDef[1].split()]
			
			precondList = parts[1].split(';')
			for p in precondList:
				pred = p.split(',')
				predname = pred[0].split()[0]
				predargs = pred[1].split()
				preconds.add(predicate(predname, [groundObject(n) for n in predargs]))

			addList = parts[2].split(';')
			for a in addList:
				pred = a.split(',')
				predname = pred[0].split()[0]
				predargs = pred[1].split()
				adds.add(predicate(predname, [groundObject(n) for n in predargs]))

			deleteList = parts[3].split(';')
			for d in deleteList:
				pred = d.split(',')
				predname = pred[0].split()[0]
				predargs = pred[1].split()
				deletes.add(predicate(predname, [groundObject(n) for n in predargs]))
				
			actions.append(action(actname, actargs, preconds, adds, deletes))
			
	return initial, goal, actions, groundObjs
				
if __name__=='__main__':
	import sys
	assert(len(sys.argv)>1)
	i, g, a, ground = parse(sys.argv[1])
	for act in a:
		act.printAction()

	print "Initial\n"
	for pred in i:
		print pred.get_string()

	print "\nGoals\n"

	for pred in g:
		print pred.get_string()

	print "\nground\n"
	for g in ground:
		print str(g)
