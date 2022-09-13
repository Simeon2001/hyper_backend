import time
from datetime import datetime
import hashlib
import math
import random

dd = str(time.time()) + str(datetime.now())
m = hashlib.sha256(dd.encode("UTF-8")).hexdigest()
value = m[0:5]
rand = math.floor(random.random() * 100000 + 1)
hashes = "{0}{1}".format(value, rand)
