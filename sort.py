class Sorting(list):
	def Bubble(self, reverse = False):
		'''Complexity O(n2)'''
		
		for i in range(len(self)):							# Compare every element with every element.
			flag,min = False,i
			for j in range(i,len(self)-i-1):				# Inner cycle till the last changed element (others are sorted already)
				if (self[j] < self[j+1]) == reverse:
					self[j],self[j+1] = self[j+1],self[j]
					flag = True								# Elements changes appeared.
				if (self[j] > self[min]) == reverse:
					min = j
			if flag == False:								# Return if there were no changes after inner cycle.
				return
			if min != i:
				self[i],self[min] = self[min],self[i]

	def Shell(self, reverse = False):
		from math import log
		kk,i = [1],1
		while 3*kk[-1] < len(self):			# for i in range(2 * int(log(1 + (1 + 4/9*(N/3-1))**0.5, 2))):
			if i & 1 == 0:	kk.append(9*2**i - 9*2**(i//2) + 1)
			else:			kk.append(8*2**i - 6*2**((i+1)//2) + 1)
			i += 1
		for k in kk:																	# Sedgwick, O(n**4/3)
	#	for k in [len(self) >> x for x in range(1, int(log(len(self), 2) + 1))]:		# Shell, O(n**2): k = [N/2, N/4, N/8, ... , 1]
	#	for k in [x for x in [1750,701,301,132,57,23,10,4,1] if x < len(self)//2 + 1]:	# Ciura for len<4000: k = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
			for i in range(k, len(self)):
				temp = self[i]
				for j in range(i, k-2, -k):
					if (self[j-k] >= temp) == reverse:
						break
					self[j] = self[j-k]
				self[j] = temp

	def Merge(self, reverse = False):
		'''Complexity O(nlogn), extra memory O(n)'''
		
		def _merge(left, right):
			if left == right:							# Return if array contains only one element
				return
			
			middle = left + (right - left) // 2			# Divide array to two equal parts.			
			_merge(left, middle)						# Recursively working with every part.
			_merge(middle + 1, right)
			
			a, i, j, k = [], left, middle+1, 0
			
			while i <= middle and j <= right:			# While both halfs are not exhausted,
				if (self[i] > self[j]) == reverse:		# compare sequential elements
					a.append(self[i])					# and gather them into resulting array.
					i += 1
				else:
					a.append(self[j])
					j += 1
			
			a += self[i:middle+1] + self[j:right+1]		# If any half is off of elements, append another to result
			self[left:left+len(a)] = a					# Rewrite elements to the origin array.
		
		_merge(0, len(self)-1)

	def Tree(self, reverse = False):
		'''Complexity O(nlogn), extra memory O(n) - n for keys and 2n for pointers'''
		class Node:
			def __init__(self, data=None, left=None, right=None):
				self.data = data
				self.left = left
				self.right = right
		class Tree:
			def __init__(self):
				self.root = None
				self.index = 0
			def add(self, data):
				if self.root == None:
					self.root = Node(data, None, None)
				else:
					self._add(data, self.root)
			def _add(self, data, node):
				if data < node.data:
					if node.left == None:
						node.left = Node(data, None, None)
					else:
						self._add(data, node.left)
				else:
					if node.right == None:
						node.right = Node(data, None, None)
					else:
						self._add(data, node.right)
			def sorting(self, arr, reverse):
				self.index = 0
				self._going(self.root, arr, reverse)
			def _going(self, node, arr, reverse):
				if node == None:
					return
				self._going(node.left if reverse == False else node.right, arr, reverse)
				arr[self.index] = node.data
				self.index += 1
				self._going(node.right if reverse == False else node.left, arr, reverse)
				
		_tree = Tree()
		for item in self:
			_tree.add(item)
		_tree.sorting(self, reverse)

	
	
	
def main():
	import time
	import random
	
#	a = Sorting([9,8,10,1,5,7,2,3,6,4,3,11,14,12,15,18,19,20,17,13,11])
#	a = Sorting([5,7,2,6,8,1,3,4])

	n = 1000
	a = Sorting(random.randint(0,n) for _ in range(n))
	n = len(a)

	direction = True
	
	random.shuffle(a)
	t1 = time.perf_counter()
	a.Bubble(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)
	
	random.shuffle(a)
	t1 = time.perf_counter()
	a.Shell(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)

	random.shuffle(a)
	t1 = time.perf_counter()
	a.Merge(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)
	
	random.shuffle(a)
	t1 = time.perf_counter()
	a.Tree(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)

	
main()