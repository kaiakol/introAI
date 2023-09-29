from Map import Map_Obj

#inspired by https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/a-star-search-algorithm/

map = Map_Obj(2)
[start_node, stop_node, end_goal_pos, path_to_map] = map.fill_critical_positions(2)
map_array = map.read_map(path_to_map)
print(map_array)

map.set_start_pos_str_marker(start_node,map_array[1])
map.set_goal_pos_str_marker(stop_node, map_array[1])

# heuristic function, using the manhattan function
def h(node):
     posx=node[0]
     posy=node[1]
     goalx=stop_node[0]
     goaly=stop_node[1]
     return abs(goalx - posx) + abs(goaly - posy)

def get_neighbors(node):
     x = node[1]
     y = node[0]
     all_neighbors = []

     #add all neighbors to the list
     if x>0:
          all_neighbors.append([y, x-1])
     if y>0:
          all_neighbors.append([y-1, x])
     if x<38:
          all_neighbors.append([y, x+1])
     if y<46:
          all_neighbors.append([y+1, x])

     walkable_neighbors = []
     for neighbor in all_neighbors:
          if map_array[1][neighbor[0]][neighbor[1]] != ' # ':
               walkable_neighbors.append(neighbor)
     return walkable_neighbors

def a_star(start_node, stop_node):

     # the list of nodes that have been visited, but the neighbors haven't all been inspected
    open_list = [start_node]

    # the list of nodes that have been visited and the neighbors have been inspected
    closed_list = []

    g = {}

    def make_key(node):
          x=str(node[1])
          y=str(node[0])
          if(len(x)==1):
               x="0"+x
          if(len(y)==1):
               y="0"+y
          return y+x

    g[make_key(start_node)] = 0

    parents = {}
    parents[make_key(start_node)] = start_node
    
    while len(open_list) > 0:
          n = None

          # find a node with the lowest value of f
          for v in open_list:
               if n == None or g[make_key(v)] + h(v) < g[make_key(n)] + h(n):
                    n = v
               if v == stop_node:
                    n = stop_node
                    break

          if n == None:
               print("The path does not exist")
               return None
          
          # if the current node is the stop node, we have found a path
          if n == stop_node:
               found_path = []

               while parents[make_key(n)] != n:
                    found_path.append(n)
                    n = parents[make_key(n)]
               
               found_path.append(start_node)

               found_path.reverse()

               print("Path found: {}".format(found_path))
               return found_path
          
          for neighbor in get_neighbors(n):
               if neighbor not in open_list and neighbor not in closed_list:
                    open_list.append(neighbor)
                    parents[make_key(neighbor)] = n
                    g[make_key(neighbor)] = g[make_key(n)] + 1

               else:
                    if g[make_key(neighbor)] > g[make_key(n)] + 1:
                         g[make_key(neighbor)] = g[make_key(n)] + 1
                         parents[make_key(neighbor)] = n

          open_list.remove(n)
          closed_list.append(n)
          
    print("The path does not exist")
    return None

path = a_star(start_node, stop_node)
shortPath = map_array[1]

for n in path:
     if n!=start_node:
          shortPath = map.replace_map_values(n, 4, stop_node)
map_array = map.read_map(path_to_map)
map.show_map(shortPath)