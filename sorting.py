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
		
		def iterator_shell(n):
			'''	Complexity O(n**2);
				k = [N/2, N/4, N/8, ... , 1]'''
			from math import log
			for x in range(1, int(log(n, 2) + 1)):
				yield n >> x
	
		def iterator_ciura(n):
			''' Proper for len<4000: '''
			for x in [1750,701,301,132,57,23,10,4,1]:
				if x < n//2 + 1:
					yield x
				
		def iterator_sedgwick(n):
			''' Complexity O(n**4/3) '''			
			kk,i = [1],1
			while 3*kk[-1] < n:			# for i in range(2 * int(log(1 + (1 + 4/9*(N/3-1))**0.5, 2))):
				if i & 1 == 0:	kk.append(9*2**i - 9*2**(i//2) + 1)
				else:			kk.append(8*2**i - 6*2**((i+1)//2) + 1)
				i += 1
			return kk
				
	#	for k in iterator_shell(len(self)):
		for k in iterator_ciura(len(self)):
	#	for k in iterator_sedgwick(len(self)):
			for i in range(k, len(self)):
				temp = self[i]
				for j in range(i, k-2, -k):
					if (self[j-k] >= temp) == reverse:
						break
					self[j] = self[j-k]
				self[j] = temp

	def Heapsort(self, reverse = False):
		'''Complexity O(nlogn)'''
		size = len(self)
		
		# Build a balanced (depth is k or k-1) B-tree, where root a[0] = max(a), a[i]>=a[2i+1] and a[i]>=a[2i+2].
		def heapify(k, n):
			new_lmnt = self[k]							
			while 2*k+1 < n:							# While there are sons, do:
				child = 2*k+1							# (a[2k+1] is a left son, a[2k+2] is a right son)
				if child+1 < n and (self[child] >= self[child+1]) == reverse:
					child += 1							# Choose largest of two sons.
				if (new_lmnt < self[child]) == reverse:
					break
				self[k] = self[child]					# If a[k] < the largest son,
				k = child								# take this son up to the root on the k-place.
			self[k] = new_lmnt
			
		for i in range(size//2-1, -1, -1):				# a[n/2]...a[n] are already leaves of a pyramid.
			heapify(i, size-1)							# Build a binary heap.
		for i in range(size-1, 0, -1):
			self[0],self[i] = self[i],self[0]			# Swap the first (max) and the last elements, putting max at the end,
			heapify(0,i)								# and remake a pyramid except the last element (put a new max at the root)
				
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

	def Quick(self, reverse = False):
	
		def lt(a,b,reverse): return a < b if not reverse else a > b
		def gt(a,b,reverse): return a > b if not reverse else a < b
		
		def _quick(left, right):
			if right - left <= 1:
				if gt(self[left], self[right], reverse):
					self[left],self[right] = self[right],self[left]
				return
		
			i, j, middle = left, right, left + (right - left) // 2
			pivot = self[middle]							# Different variables are possible. E.g., a median of a[left], a[middle] and a[right]
			
			while i <= j:
				while lt(self[i], pivot, reverse):			# Pass all a[i] < pivot
					i += 1
				while gt(self[j], pivot, reverse):			# Pass all a[j] > pivot
					j -= 1
				if i <= j:									# If a[i] >= pivot >= a[j], swap a[i] and a[j]
					self[i],self[j] = self[j],self[i]
					i += 1
					j -= 1
		
			if j >= left:									# Sort elements to the left of the pivot
				_quick(left, j)
			if i <= right:									# Sort elements to the right of the pivot
				_quick(i, right)
				
		_quick(0, len(self)-1)
	
	def QuickI(self, reverse = False):
	
		def lt(a,b,reverse): return a < b if not reverse else a > b
		def gt(a,b,reverse): return a > b if not reverse else a < b
	
		indices = [0, len(self)-1]							# A stack, where indices[2i] == lefts, indices[2i+1] == rights.
		
		while len(indices) > 0:
			left,right = indices[-2],indices[-1]
			del indices[-2:]								# Pop current indices from the stack.
			
			if right - left <= 1:
				if gt(self[left], self[right], reverse):
					self[left],self[right] = self[right],self[left]
				continue
			
			i, j, middle = left, right, left + (right - left) // 2
			pivot = self[middle]							# Different variables are possible. E.g., a median of a[left], a[middle] and a[right]
		
			while i <= j:
				while lt(self[i], pivot, reverse):			# Pass all a[i] < pivot
					i += 1
				while gt(self[j], pivot, reverse):			# Pass all a[j] > pivot
					j -= 1
				if i <= j:									# If a[i] >= pivot >= a[j], swap a[i] and a[j]
					self[i],self[j] = self[j],self[i]
					i += 1
					j -= 1
		
			if j >= left:									# Sort elements to the left of the pivot
				indices += left,j
			if i <= right:									# Sort elements to the right of the pivot
				indices += i, right

	
def main():
	import time
	import random
	
#	a = Sorting([9,8,10,1,5,7,2,3,6,4,3,11,14,12,15,18,19,20,17,13,11])
#	a = Sorting([5,7,2,6,8,1,3,4])

	n = 1000
	a = Sorting(random.randint(0,n) for _ in range(n))
	n = len(a)

	direction = True

	# def qsort(L):
		# if L:
			# return qsort([x for x in L[1:] if x<L[0]]) + L[0:1] + qsort([x for x in L[1:] if x>=L[0]])
		# return []
	
	# print(qsort(a))
		
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
	a.Heapsort(reverse = direction)
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

	random.shuffle(a)
	t1 = time.perf_counter()
	a.Quick(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)

	random.shuffle(a)
	t1 = time.perf_counter()
	a.QuickI(reverse = direction)
	print(time.perf_counter() - t1)
#	print(*a)
	
if __name__ == '__main__':
    main()
