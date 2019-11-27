import numpy as np

# http://cs231n.github.io/python-numpy-tutorial/#numpy

a = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(a.shape)

# select element
# print(a[1, 2])  # row 1, column 2, same as a[(1, 2)]

# select range
# print(a[:2, 1:])  # rows 0,1, columns 1, 2
# print(a[:, 1])  # column 1
# print(a[1, :])  # row 1

# select specific index pairs
print(a[[0, 1, 0], [1, 2, 0]])

# set element
a[1, 2] = 30
# print(a)

# set range
a[:2, 1:] = np.array([[10, 11], [12, 13]])
# print(a)

# set specific indices
a[np.arange(a.shape[0]), [0, 1, 0]] += 3
print(a)

a = np.array([
    [1, 2],
    [3, 4],
    [5, 6]]
)

ind = a >= 4
print(ind)
print(a[ind])

x = np.array([1, 2], dtype=np.int64)
y = np.array([1, 2], dtype=np.float)
print(x)
print(y)

c = x + y
print(c)

a = np.array([
    [1, 2],
    [3, 4]
])
print(np.sum(a))  # sum everything
print(np.sum(a, axis=0))  # sum columns
print(np.sum(a, axis=1))  # sum rows

# broadcasting
a = np.array([
    [1, 2],
    [3, 4]
])
a += 1
print(a)

import matplotlib.pyplot as plt
x = np.arange(0, 3 * np.pi, 0.1)
y = np.sin(x)

plt.plot(x, y)
plt.show()
