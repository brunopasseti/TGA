from collections import deque
from enum import IntEnum
from typing import Dict, Tuple, List
from sys import argv
import time


class Queue(deque):

  def __init__(self, iterable=None):
    if (iterable):
      super().__init__(iterable)
    else:
      super().__init__()

  def push(self, item):
    super().append(item)

  def pop(self):
    return super().popleft()


# Enum to represent the colors of an edge
class ColorEnum(IntEnum):
  BLUE = 0
  RED = 1
  YELLOW = 2
  GREEN = 3
  BLACK = -1


# Enum to rgb string
def match_color(t):
  if (t == ColorEnum.BLUE):
    return "0,0,255"
  elif (t == ColorEnum.RED):
    return "255,0,0"
  elif (t == ColorEnum.YELLOW):
    return "255,255,0"
  elif (t == ColorEnum.GREEN):
    return "0,255,0"
  elif (t == ColorEnum.BLACK):
    return "0,0,0"


# Search graph using Depth-first search
def dfs(n, graph, start) -> Dict[Tuple[int, int], ColorEnum]:
  t = 0
  PE = [0] * n
  PS = [0] * n
  pai = [None] * n
  colors: Dict[Tuple[int, int], ColorEnum] = dict()

  def idfs(v, t):
    t = t + 1
    PE[v] = t
    for w in range(n):
      if (v == w or not graph[v][w] or (w, v) in colors.keys()):
        continue
      if (PE[w] == 0):
        # print("Now doing %d going to %d" % (v, w))
        colors[(v, w)] = ColorEnum.BLUE
        pai[w] = v
        idfs(w, t)
      else:
        if (PS[w] == 0 and w != pai[v]):
          # print("return from %d to %d" % (v, w))
          colors[(v, w)] = ColorEnum.RED
    t = t + 1
    PS[v] = t

  idfs(0, t)
  return colors


# Search graph using Breadth-first search, return the color of the edges, the maximum path,
# and the avarage path between start and other node
def bfs(n, graph,
        start) -> Tuple[Dict[Tuple[int, int], ColorEnum], int, float]:
  t = 0
  F = Queue()
  L = [0] * n
  colors: Dict[Tuple[int, int], ColorEnum] = dict()
  pai = [None] * n
  nivel = [0] * n
  is_first_run = True
  while 0 in L:
    v = start if is_first_run else L.index(0)
    is_first_run = False
    nivel[v] = 0
    t = t + 1
    L[v] = t
    F.push(v)
    while len(F) > 0:
      v = F.pop()
      for w in range(n):
        if (v == w or not graph[v][w] or (w, v) in colors.keys()
            or (v, w) in colors.keys()):
          continue
        if (L[w] == 0):
          colors[(v, w)] = ColorEnum.BLUE
          pai[w] = v
          nivel[w] = nivel[v] + 1
          t = t + 1
          L[w] = t
          F.push(w)
        else:
          if (nivel[w] == nivel[v] and w in F):
            if (pai[w] == pai[v]):
              colors[(v, w)] = ColorEnum.RED
            else:
              colors[(v, w)] = ColorEnum.YELLOW
          elif (nivel[w] == nivel[v] + 1):
            colors[(v, w)] = ColorEnum.GREEN
  lw = max(nivel)
  an = sum(nivel) / (n - 1)  # Don't count start
  return colors, lw, an


# Read graph as tuple of (int, int[[]])
def read_datafile(filename):
  with open(filename, 'r') as f:
    n = int(f.readline().strip())
    data = list(
      map(lambda l: list(map(int,
                             l.lstrip("\n").split(" "))), f.readlines()))
  return (n, data)


# Write the result file in Gephi's GDF format
def write_gdf_file(filename, n, data, colors):
  with open(filename, 'w') as f:
    f.write("nodedef>name VARCHAR, label VARCHAR\n")
    for i in range(n):
      f.write("%d,%d\n" % (i + 1, i + 1))
    f.write(
      "edgedef>node1 VARCHAR, node2 VARCHAR, directed BOOLEAN, color VARCHAR\n"
    )
    s = []
    for i in range(n):
      for j in range(n):
        if data[i][j] == 1 and (i, j) in colors.keys():
          s.append("%d, %d, false,'%s'\n" %
                   (i + 1, j + 1, match_color(colors[(i, j)])))
    s.sort()
    for line in s:
      f.write(line)


def main():
  n, data = read_datafile(argv[1] if len(argv) > 1 else "graph_1b.txt")
  colors = dfs(n, data, 0)
  # print(colors)
  time_str = time.strftime("%H_%M_%S", time.localtime())
  write_gdf_file("graph_" + time_str + "_dfs_.gdf", n, data, colors)
  colors, lw, av = bfs(n, data, 0)
  write_gdf_file("graph_" + time_str + "_bfs_.gdf", n, data, colors)
  h = [bfs(n, data, i) for i in range(n)]
  av = list(map(lambda e: e[2], h))
  h = list(map(lambda e: e[1], h))
  print(("radius = %d, " + "diameter = %d " + "avg. path = %lf") %
        (min(h), max(h), sum(av) / n))


if __name__ == "__main__":
  main()
