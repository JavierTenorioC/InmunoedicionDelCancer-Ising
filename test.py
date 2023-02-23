import mesa

from cancerInmunoediting.agents import *
from cancerInmunoediting.model import CancerInmunoediting

model = CancerInmunoediting(0.6,0.05,0.6,0.05)

for i in range(10):
    model.step()