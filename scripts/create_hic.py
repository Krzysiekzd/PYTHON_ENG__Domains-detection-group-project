import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# This script creates 300x300 toy matrix with values from 0 to 100, that can be used for testing purposes.

def create_square(matrix, size, left_up_corner, min_value, max_value):
    for i in range(size):
        for j in range(size):
            matrix[left_up_corner+i][left_up_corner+j] = random.randint(min_value, max_value)
    print('Positions from: {} to: {}, values from: {} to {}'.format(left_up_corner, left_up_corner+size,
    min_value, max_value))
# New matrix
a = np.random.randint(low=10, high=30 ,size=(300,300),dtype=np.int8)
a[299][0] = 100
a[299][1] = 0

create_square(a, size=60, left_up_corner=165, min_value=23, max_value=40)
create_square(a, size=70, left_up_corner=20, min_value=26, max_value=36)
create_square(a, size=100, left_up_corner=70, min_value=21, max_value=31)
create_square(a, size=45, left_up_corner=255, min_value=21, max_value=31)

create_square(a, size=40, left_up_corner=0, min_value=55, max_value=60)
create_square(a, size=25, left_up_corner=0, min_value=57, max_value=68)

create_square(a, size=20, left_up_corner=40, min_value=25, max_value=53)
create_square(a, size=10, left_up_corner=40, min_value=62, max_value=72)
create_square(a, size=10, left_up_corner=50, min_value=59, max_value=70)

create_square(a, size=40, left_up_corner=60, min_value=50, max_value=68)
create_square(a, size=25, left_up_corner=75, min_value=58, max_value=72)
create_square(a, size=10, left_up_corner=75, min_value=65, max_value=75)

create_square(a, size=35, left_up_corner=100, min_value=53, max_value=67)
create_square(a, size=15, left_up_corner=100, min_value=60, max_value=73)
create_square(a, size=20, left_up_corner=115, min_value=61, max_value=67)

create_square(a, size=60, left_up_corner=135, min_value=40, max_value=59)
create_square(a, size=30, left_up_corner=135, min_value=62, max_value=66)
create_square(a, size=30, left_up_corner=165, min_value=62, max_value=66)
create_square(a, size=20, left_up_corner=155, min_value=64, max_value=68)
create_square(a, size=20, left_up_corner=135, min_value=75, max_value=83)
create_square(a, size=10, left_up_corner=155, min_value=80, max_value=87)
create_square(a, size=17, left_up_corner=165, min_value=65, max_value=73)
create_square(a, size=13, left_up_corner=182, min_value=67, max_value=74)

create_square(a, size=60, left_up_corner=195, min_value=30, max_value=55)
create_square(a, size=45, left_up_corner=210, min_value=53, max_value=65)
create_square(a, size=25, left_up_corner=230, min_value=60, max_value=67)
create_square(a, size=15, left_up_corner=195, min_value=67, max_value=71)
create_square(a, size=20, left_up_corner=210, min_value=65, max_value=72)
create_square(a, size=15, left_up_corner=230, min_value=60, max_value=75)
create_square(a, size=10, left_up_corner=245, min_value=66, max_value=78)

create_square(a, size=15, left_up_corner=255, min_value=66, max_value=78)
create_square(a, size=30, left_up_corner=270, min_value=66, max_value=78)

# Making the matrix symmetric
for i in range(300):
    for j in range(300-i):
        a[i][j]=a[j][i]


plot = sns.heatmap(a, cmap='YlOrRd')
figure = plot.get_figure()
# Save png
#figure.savefig('hic.png', dpi=600)
plt.show()
# Save to .csv file. Can be easily loaded with np.loadtxt function.
#np.savetxt('hic_matrix.csv', a, delimiter=',')
