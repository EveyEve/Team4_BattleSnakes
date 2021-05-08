
import global_variables as gv
#have a library with our strategy
import strategy_A_Star
import strategy_Dij
def determine_possible_moves(data, all_snakes_body_parts):
  
  #current head of snake 
  current_head = data["you"]["head"]

  #all_snakes_body_parts = other_snakes(data)

  #what is adjacent to our head 
  aboveHead = {'x': current_head['x'], 'y': current_head['y']+1}
  belowHead = {'x': current_head['x'], 'y': current_head['y']-1}
  leftHead = {'x': current_head['x']-1, 'y': current_head['y']}
  rightHead = {'x': current_head['x']+1, 'y': current_head['y']}

  #potential moves we could make 
  possible_moves = []

  if (aboveHead not in all_snakes_body_parts) and (aboveHead['y'] < data["board"]["height"]):
    possible_moves.append("up")

  if (belowHead not in all_snakes_body_parts) and (belowHead['y'] >= 0):
    possible_moves.append("down")

  if (leftHead not in all_snakes_body_parts) and (leftHead['x'] >= 0):
    possible_moves.append("left")

  if (rightHead not in all_snakes_body_parts) and (rightHead['x'] < data["board"]["width"]):
    possible_moves.append("right")

  return possible_moves

#generate an array with all of the snakes body parts
def other_snakes(data):
  all_snakes_body_parts = []
  
  snakes = data["board"]["snakes"]

  for snake in snakes:
    for body_part in snake["body"]:
      all_snakes_body_parts.append(body_part)
      #print(body_part)

  return all_snakes_body_parts

def go_for_food_Dij(data,snake_walls, other_snakes_wall, all_food):
  our_head = (data["you"]["head"]["x"],data["you"]["head"]["y"])

  a_star = strategy_Dij.AStar()
  #store the grid height and width
  a_star.grid_height = data["board"]["height"]
  a_star.grid_width = data["board"]["width"]
  a_star.init_grid(a_star.grid_width, a_star.grid_height, walls = snake_walls, others_walls = other_snakes_wall, start = our_head)
  a_star.solve()
  all_paths = []
  costs = []
  
  for food in all_food:
    #initialize the grid walls, starting point (head) and end
    curr_path, weight = a_star.get_path(food[0], food[1])
    if curr_path is not None:
      all_paths.append(curr_path)
      costs.append(weight)
      
    
  #print("paths unsorted: ",all_paths)
  
  if len(all_paths) != 0:
    lowestCost = 100000
    lowestCostIndex = 0;
    for i in range (len(costs)):
      if costs[i] < lowestCost:
        lowestCost = costs[i]
        lowestCostIndex = i;
    #all_paths.sort(key=len)
    #print("paths sorted: ",all_paths)
    path = all_paths[lowestCostIndex] #shortest one since we sorted
    if (path[1][0] < our_head[0]):
      move = "left"
    elif (path[1][0] > our_head[0]):
      move = "right"
    elif (path[1][1] < our_head[1]):
      move = "down"
    else:
      move = "up"
    #print(path)
  else:
    move = None
  return move 

def go_for_food_A_Star(data,all_snake_body_parts):
  #create the object that contains the astar implementation
  #have list of our other snakes body parts that will act as our walls
  #all_snake_body_parts = other_snakes(data)

  a_star = strategy_A_Star.AStar()
  #store the grid height and width
  a_star.grid_height = data["board"]["height"]
  a_star.grid_width = data["board"]["width"]

  snake_walls = []
  for part in all_snake_body_parts:
      snake_walls.append((part["x"], part["y"]))
  #print(snake_walls)

  #need starting position our head
  our_head = (data["you"]["head"]["x"], data["you"]["head"]["y"])

  all_food_data = data["board"]["food"]
  all_food = []
  for food in all_food_data:
      all_food.append((food["x"], food["y"]))
  #print(all_food)

  all_paths = []

  for food in all_food:
      #initialize the grid walls, starting point (head) and end
      a_star.init_grid(a_star.grid_width,
                      a_star.grid_height,
                      walls=snake_walls,
                      start=our_head,
                      end=food)
      curr_path = a_star.solve()
      if curr_path is not None:
          all_paths.append(curr_path)

  #print("paths unsorted: ",all_paths)

  if len(all_paths) != 0:
      all_paths.sort(key=len)
      #print("paths sorted: ",all_paths)
      path = all_paths[0]  #shortest one since we sorted
      if (path[1][0] < our_head[0]):
          move = "left"
      elif (path[1][0] > our_head[0]):
          move = "right"
      elif (path[1][1] < our_head[1]):
          move = "down"
      else:
          move = "up"
      #print(path)
  else:
      #flood fill should be activated here
      #and head towards open areas
      move = None
  return move