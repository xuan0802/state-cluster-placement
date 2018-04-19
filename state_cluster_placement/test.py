import copy

import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ('Python', 'C++', 'Java')
y_pos = np.arange(len(objects))
performance = [100, 101, 102]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylim(99, 103)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()