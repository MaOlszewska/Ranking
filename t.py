import numpy as np

l = [1, 10]
l = np.array(l)
l = l - 1
l = np.multiply(l, 16/9)
l = l + 1
print(l)


a = [

        [0,10],
        [1,10],
        [1.1,10],
        [1,10]

]
a = np.ndarray.tolist(np.multiply((np.array(a)), 16/10) + 1)
print(a)
# l = l * 1,7
# print(l)
# l = l + 1
# print(l)