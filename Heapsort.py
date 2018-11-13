import time
import random

class Sortable(list):
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


def main():
    n = 1000
    a = Sortable(random.randint(0, n) for _ in range(n))
    n = len(a)

    reverse = True

    random.shuffle(a)
    start = time.perf_counter()
    a.Heapsort(reverse=reverse)
    print("Dimension = {}, time = {:.3f} sec"
          .format(n, time.perf_counter() - start))


if __name__ == '__main__':
    main()
