from grafo_pronto import grafo
import random
import queue
from copy import deepcopy
from math import sqrt
import time
import matplotlib.pyplot as plt
import numpy as np
import os
from queue import Queue
from visual import visual
G = grafo('pdh.txt')
fluxo_aresta = [373.0, 0.0, 364.0, 237.0, 40.0, 0.0, 0.0, 266.0, 99.0, 0.0, 0.0, 278.0, 138.0, 0.0, 144.0, 237.0, 160.0, 22.0, 124.0, 0.0, 105.0, 0.0, 95.0, 0.0, 0.0, 108.0, 115.0, 212.0, 378.0, 160.0, 384.0, 0.0, 247.0, 100.0]
visual(G,fluxo_aresta)
