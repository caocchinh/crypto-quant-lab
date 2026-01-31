# import random
# import string
# from matplotlib import pyplot as plt
#
# plt.style.use("fivethirtyeight")
#
# length = range(10)
# slices = [random.randint(100, 1000) for i in length]
# labels = [''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in length) for i in length]
# color = ["#" + ''.join(random.SystemRandom().choice("abcdef" + string.digits) for _ in range(6)) for i in length]
# plt.pie(slices, labels=labels, colors=color, wedgeprops={"edgecolor": "black"})
# plt.title("My pie chart")
# plt.tight_layout()
# plt.show()

import random
import string
from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")
plt.xkcd()

length = range(10)
labels = ['Java', 'Python', 'SQL', 'HTML/CSS', 'JavaScript']
slices = [35917, 36443, 47544, 55466, 59219]
explode = [0,0,0,0.231,0]

color = ["#" + ''.join(random.SystemRandom().choice("abcdef" + string.digits) for _ in range(6)) for i in length]
plt.pie(slices, labels=labels, wedgeprops={"edgecolor": "black"},explode=explode,shadow=True,startangle=130
        ,autopct="%1.1f%%")
plt.title("My pie chart")
plt.tight_layout()
plt.show()

