import numpy as np
y = np.empty((0,4), int)
cam = np.array([20,20])
row  = np.array([1,2,3,4])
y = np.append(y, [row] , axis = 0)
y = np.append(y, [row], axis = 0)

for line in y:
    line[2:4] -= cam
print(y)
