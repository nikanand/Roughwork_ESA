# Calculate the loss between era0 and last era
def gt(x,y): return x > y
def lt(x,y): return x < y

def better(i):  return lt

def loss1(i,x,y):
    return (x - y) if better(i) == lt else (y - x)

def expLoss(i,x,y,n):
    return math.exp( loss1(i,x,y) / n)

def loss(x, y):
    x,y    = x.getObjectives(), y.getObjectives()
    n      = min(len(x), len(y))    #lengths should be equal 
    losses = [ expLoss(i,xi,yi,n)
                 for i, (xi, yi) 
                   in enumerate(zip(x,y)) ]
    return sum(losses) / n

