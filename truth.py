class Expr:
	order = ['Var', 'Not', 'And', 'Or', 'Eq']

	def __init__(self, op1, op2 = None):
		self.op1 = op1
		self.op2 = op2
		self.tauto = True

	def getStr(self, classname, op):
		i = Expr.order.index(classname)
		s = ""
		# if parents operator binds stronger than childe then add bracket
		if  Expr.order.index(self.op1.__class__.__name__) > i:
			s += "(" + str(self.op1) + ")"
		else : s += str(self.op1)
		s += op
		if  Expr.order.index(self.op2.__class__.__name__) > i:
			s += "(" + str(self.op2) + ")"
		else : s += str(self.op2)
		return s
	
	def getAllTerms(self):
		# get all Vars in current expression
		if isinstance(self, Var):
			return [self.op1]
		r = self.op1.getAllTerms()
		if self.op2 != None: r += self.op2.getAllTerms()
		return list(set(r))

	def make_tt(self):
		result = ''
		terms = self.getAllTerms()
		table = [[True], [False]]
		for i in range(1, len(terms)):
			new_table = []
			for t in table:
				new_table.append([True] + t)
				new_table.append([False] + t)
			table = new_table
		
		# print head of truth table
		for t in terms:
			result += '{0:10}|'.format(t)
		result += str(self) + '\n'

		# iterate all possible combinations and evaluate expression
		for t in table:
			for i in t:
				result += '{0:10}|'.format(str(i))
			x = {}
			for i, v in enumerate(terms):
				x[v] = t[i]
			e = self.eval(x)
			if e == False: self.tauto = False
			result +=  str(e) + "\n"
		return (result)
		
	def isTauto(self):
		self.make_tt()
		return self.tauto


class Not(Expr):
	def __init__(self, var):
		assert(isinstance(var, Expr))
		super().__init__(var)

	def __str__(self):
		if  Expr.order.index(self.op1.__class__.__name__) > 1:
			return "!(" + str(self.op1) + ")"
		return "!" + str(self.op1)

	def eval(self, table):
		return not self.op1.eval(table) 

class And(Expr):
	def __init__(self, op1, op2):
		super().__init__(op1, op2)

	def __str__(self):
		return self.getStr('And', '&')

	def eval(self, table):
		return self.op1.eval(table) and self.op2.eval(table)

class Or(Expr):
	def __init__(self, op1, op2):
		super().__init__(op1, op2)

	def __str__(self):
		return self.getStr("Or",'|')

	def eval(self, table):
		return self.op1.eval(table) or self.op2.eval(table)

class Eq(Expr):
	def __init__(self, op1, op2):
		super().__init__(op1, op2)

	def __str__(self):
		return self.getStr('Eq' , '==')

	def eval(self, table):
		return self.op1.eval(table) == self.op2.eval(table)

class Var(Expr):
	def __init__(self, var):
		assert(isinstance(var, str))
		super().__init__(var)

	def __str__(self):
		return self.op1

	def eval(self, table):
		return table[self.op1]


# test code

e1 = Or(Var("x"),Not(Var("x")))
e2 = Eq(Var("x"),Not(Not(Var("x"))))
e3 = Eq(Not(And(Var("x"),Var("y"))),Or(Not(Var("x")),Not(Var("y"))))
e4 = Eq(Not(And(Var("x"),Var("y"))),And(Not(Var("x")),Not(Var("y"))))
e5 = Eq(Eq(Eq(Var("p"),Var("q")),Var("r")),Eq(Var("p"),Eq(Var("q"),Var("r"))))

e5.make_tt()

print(e1)
print(e2)
print(e3)
print(e4)
print(e5)



print(And(Not(Var("p")),Var("q")))
print(Not(And(Var("p"),Var("q"))))
print(Or(And(Var("p"),Var("q")),Var("r")))
print(And(Var("p"),Or(Var("q"),Var("r"))))
print(Eq(Or(Var("p"),Var("q")),Var("r")))
print(Or(Var("p"),Eq(Var("q"),Var("r"))))

print (e2.eval({"x" : True}))
print (e3.eval({"x" : True, "y" : True}))
print (e4.eval({"x" : False, "y" : True}))

print(e1.make_tt())
print(e2.make_tt())
print(e3.make_tt())
print(e4.make_tt())
print(e5.make_tt())

print (And(Var("x"),And(Var("y"),Var("z"))))
print (And(And(Var("x"),Var("y")),Var("z")))

print (e1.isTauto())
print (e2.isTauto())
print (e3.isTauto())
print (e4.isTauto())
print (e5.isTauto())