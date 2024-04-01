from cgitb import small
import heapq
from multiprocessing import heap

from numpy import array, insert, true_divide

class PriorityQueue:
    
    #I	ntialize priority queue
	def __init__(pq):
		pq.count = 0
		pq.pq = []
  
	#	Insert an element with specific priority in queue. Returns False if element already exists in queue
	def push(pq,item,priority):
		flag = True
		if (priority,item) in pq.pq:
			return
		typle = (priority,item)
		heapq.heappush(pq.pq,typle)
		if flag == True:
			pq.count+=1
    #	Return and delete from queue the element with the minimum priority
	def pop(pq):
		if pq.count == 0:
			print("Queue is empty")
			return
		pq.count-=1
		return (heapq.heappop(pq.pq))[1]

	#	Returns true if queue is empty
	def isempty(pq):
		if pq.count == 0:
			return True
		return False

	def update(pq,item,priority):
		
		#	If queue is empty do nothing
		if(pq.isempty()):
			return

		#	We transer all elements from our heap to temp_heap deleting dublicates and keeping smallest priority items
		temp_heap = []
		flag = False
		while(len(pq.pq) != 0):
			smallest = heapq.heappop(pq.pq)
			if smallest[1] == item and flag == False:
				if smallest[0] <= priority:
					heapq.heappush(temp_heap,smallest)
					flag = True
				else:
					heapq.heappush(temp_heap,(priority,item))
					flag = True
			elif smallest[1] == item:
				continue
			else:
				heapq.heappush(temp_heap,smallest)
		pq.pq = temp_heap
		pq.count = len(temp_heap)

#	We sort an integer list using Priority Queue, and we return it. Deleting Dublicates
def PQSort(list):
    n = len(list)
    q = PriorityQueue()
    return_list = []
    
    # We move all elements to a Priority Queue and deleting dublicates in push function
    for i in range(n):
    	PriorityQueue.push(q,list[i],list[i])
     
    # We move all elements with Priority to ordering list
    while not q.isempty():
        return_list.append(q.pop())
    return return_list