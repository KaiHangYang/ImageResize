#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,17---------------
import math
import time
def test(W,H,w,h, flag):
    for i in xrange(W):
        for j in xrange(H):
            if flag:
                x = (i+0.0)/w
                y = (i+0.0)/h

                p = x - int(x)
                q = y - int(y)

            else:
                x = int(math.floor((i+1)/w-1))
                y = int(math.floor((j+1)/h-1))
                p = (i+0.0)/w - x
                q = (j+0.0)/h - y

if __name__ == "__main__":
    t1 = time.time()
    test(1000, 700, 2, 2, True)
    t2 = time.time()
    print "My:%f"%(t2-t1)

    t1 = time.time()
    test(1000, 700, 2, 2, False)
    t2 = time.time()
    print "They:%f"%(t2-t1)
