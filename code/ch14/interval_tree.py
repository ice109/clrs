from collections import deque
import random
from ch13.red_black_tree import RedBlackTree, RBTreeNode, RBSENTINEL
import re
from ast import literal_eval

class INTERSENTINEL(RBSENTINEL):
    def __init__(self, prnt):
        super().__init__(prnt)
        self.max = float("-inf")

class InterNode(RBTreeNode):

    SENTINEL = INTERSENTINEL

    def __init__(self,*pargs):
        # pargs = val, prnt, color, lchild, rchild
        # **kwargs means unpack them as key value args
        super().__init__(*pargs)
        self.max = max(self.lchild.max,self.rchild.max,pargs[0][1] if len(pargs) > 0 else float("-inf"))


    def __str__(self):
        return re.sub(r'\)',r']',re.sub(r'\(',r'[',super().__str__()[:-1])) + str(self.max)

class IntervalTree(RedBlackTree):

    nodetype = InterNode

    def __init__(self,ls=None):
        super()._init__()
        if ls is not None:
            for v in ls:
                self.insert(v)

    def insert(self, inter):
        new = super().insert(inter)
        while new:
            new.max = max(new.lchild.max,new.rchild.max,new.val[1])
            new = new.prnt


    def overlap(self,inter):
        return self.overlaproot(inter,self.root)

    def overlaproot(self,inter,root):

        ovrlp = lambda x,y: (y[0] <= x[1] <= y[1]) or (y[0] <= x[0] <= y[1])
        ptr = root
        while not ovrlp(inter,ptr.val) and ptr:
            # ptr.lchild.max >= inter[0] but no overlapping intervals then definitely
            # none in the right side either.
            if ptr.lchild and ptr.lchild.max >= inter[0]:
                ptr = ptr.lchild
            # if ptr.lchild.max < inter[0] then definitely no overlapping intervals there
            else:
                ptr = ptr.rchild

        return ptr

    # 14.3-3
    def min_overlap(self,inter):
        cand = self.overlap(inter)

        while cand.lchild:
            cand = self.overlaproot(inter,cand.lchild)

        return cand

    #14.3-4
    def all_overlap(self,inter):
        alloverlap = []
        stk = []
        ovrlp = lambda x,y: (y[0] <= x[1] <= y[1]) or (y[0] <= x[0] <= y[1]) or \
                            (x[0] <= y[1] <= x[1]) or (x[0] <= y[0] <= x[1])
        crnt = self.root

        while crnt or (len(stk) > 0):
            if crnt:
                stk.append(crnt)
                if ovrlp(crnt.val,inter):
                    alloverlap.append(crnt.val)
                if crnt.lchild and crnt.lchild.max >= inter[0]:
                    crnt = crnt.lchild
                else: # hack
                    crnt = None
            else:
                if len(stk) >0 :
                    p = stk.pop()
                    if p.rchild and p.rchild.max >= inter[0] and p.val[0] <= inter[1]:
                        crnt = p.rchild
                else:
                    break


        return alloverlap


        #   y             r
        #  / \  ->    / \
        # b   r      y   d
        #    / \    / \
        #   c   d  b   c
    def _left_rotate(self,y):
        yy,r = super()._left_rotate(y)
        r.max = max(r.lchild.max,r.rchild.max,r.val[1])
        yy.max = max(yy.lchild.max,yy.rchild.max,yy.val[1])

        #   l          y
        #  / \  <-    / \
        # b   y      l   d
        #    / \    / \
        #   c   d  b   c
    def _right_rotate(self,y):
        yy,l = super()._right_rotate(y)
        l.max = max(l.lchild.max,l.rchild.max,l.val[1])
        yy.max = max(yy.lchild.max,yy.rchild.max,yy.val[1])




if __name__ == '__main__':
    xs = random.sample(range(20),10)
    ys = random.sample(range(20),10)

    ps = [(x,y) if x<=y else (y,x) for x,y in zip(xs,ys)]
    itree = IntervalTree(ps)
    itree.print()
    print(itree.all_overlap(literal_eval(input("inter: "))))
    itree.print()

#14.3-6
# when you insert into a binary tree you can keep track of predecessor and successor at no extra cost:
# the predecessor the last right->left turn you made and the successor is the last left->right turn you made
# and the narrowest gap between an element any other element is the minimum of the gap between it and its
# predecessor and successor. so you can insert and keep track of all the minimum intervals and insert them
# into an interval tree. the question of how to find the smallest one though? I guess you could augment
# an interval tree node with max width? i also don't know how to do deletion or search

# 14.3-7
# sweep a line in both directions adding and removing intervals as they appear. on adding each interval
# check if there's a collision

# 14-1

# keep track of the sum of negatives and positives on the left side of a node and the right side of a node
# a surplus of negatives mean the endpoint corresponding to the node you're at is inside that many
# intervals (on the left). a surplus of positives on the right means the same thing. keep a point to the current
# maximum overlap by simply check with some value stored somewhere every time a new interval is inserted
# (can't figure out how to compute it from the tree without traversing entire tree).


# 14-2a use a circularly linked list and just delete notes while skipping forward m times. running time
# is O(mn) but m is a constant so O(m). alternatively you can use the recurrence relation
# josephus(n,k) = (josephus(n-1,k) + k-1)%n +1
# josephus(1,k) = 1
# the logic here is that once the first element of n elements is deleted there are n-1 elements
# remaining and we need the last survivor of those n-1 elements. the k-1 is because we need to count
# from where the first element is deleted (k-1)th position. %n is to wrap around and +1 is shifting
# to 1 counting because using mod makes it as if we're counting from 0

# 14-2b use an order statistic tree and delete the kth ranked element, then delete the (k+k)%n ranked element
# etc