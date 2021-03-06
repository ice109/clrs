class Deque:
    def __init__(self,len):
        self.len = len
        self.arr = len*[None]
        # the next place to insert in the front
        self.front_ind = 0
        # the next place to insert in the back
        self.back_ind = len-1

    def _safe(self):
        if (self.back_ind == self.front_ind-1) or (self.back_ind+1 == self.front_ind):
            raise Exception("stack full or empty")

    def push_front(self,x):
        self._safe()
        self.arr[self.front_ind] = x
        self.front_ind = (self.front_ind+1)%self.len

    def pop_front(self):
        self._safe()
        ind = (self.front_ind-1)%self.len
        r = self.arr[ind]
        self.arr[ind] = None
        self.front_ind = ind
        return r

    def push_back(self,x):
        self._safe()
        self.arr[self.back_ind] = x
        self.back_ind = (self.back_ind-1)%self.len

    def pop_back(self):
        self._safe()
        ind = (self.back_ind+1)%self.len
        r = self.arr[ind]
        self.arr[ind] = None
        self.back_ind = ind
        return r


if __name__ == '__main__':
    d = Deque(10)
    # d.push_front(1)
    d.push_back(-1)
    # d.push_front(2)
    d.push_back(-2)
    # d.push_front(3)
    d.push_back(-3)
    # d.push_front(4)
    d.push_back(-4)
    # d.push_front(5)
    d.push_back(-5)
    d.pop_front()
    d.push_front(9)
    d.push_front(10)
    d.push_back(11)
    d.pop_back()
    d.pop_back()
    d.pop_back()
    print(d.arr,d.front_ind,d.back_ind)


# 10.1-2 have one stack grow from the left and have the second stack grow from the right (towards
# the end of the other one, e.g. |1|2|3|-|-|-|3|2|1| and when they collide then the two stacks is full

# 10.1-5 essentially circular list with head and tail being linked together. another
# way to implement this is having a counter increment around the array mod the length
# of the array

# 10.1-6 push to one stack. pop from the other. if the "outbox" stack is empty then pop everything from the inbox stack
# and push to outbox stack. they'll be pushed in reverse order. amortized time is O(n)

# 10.1-7 same thing as above: inbox queue and outbox queue. push to inbox. when outbox is empty pop everything from inbox
# and push to outbox. they get pushed in reverse order, i.e. last first and so popping from outbox will give stack behavior.