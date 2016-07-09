import pickle
from time import time

try:
    d = pickle.load(open('teste.dat','rb'))
except:
    d = {'a':[]}

a = d['a']

a.append(time())

print a

d['a'] = a

pickle.dump(d,open('teste.dat','wb'))

