import strategy_A_Star
import strategy_Dij
import strategy
import random

def go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall):

  our_head = (data["you"]["head"]["x"],data["you"]["head"]["y"])
  open_space_star = strategy_Dij.AStar()
  open_space_star.grid_height = data["board"]["height"]
  open_space_star.grid_width = data["board"]["width"]
  
  the_closest_open_value = findopenspace(board)
  #print("closet open value" + str(the_closest_open_value))
  open_space_star.init_grid(open_space_star.grid_width, open_space_star.grid_height, walls = snake_walls, others_walls = other_snakes_wall, start = our_head)
  open_space_star.solve()

  curr_path, weight = open_space_star.get_path(the_closest_open_value[0],the_closest_open_value[1])
  if curr_path is not None:
    #all_paths.sort(key=len)
    #print("paths sorted: ",all_paths)
    if (curr_path[1][0] < our_head[0]):
      move = "left"
    elif (curr_path[1][0] > our_head[0]):
      move = "right"
    elif (curr_path[1][1] < our_head[1]):
      move = "down"
    else:
      move = "up"
    #print(path)
  else:
    move = None
  
  return move

def findopenspace(M):
    R = len(M) # no. of rows in M[][]
    C = len(M[0]) # no. of columns in M[][]
  
    S = [[0 for k in range(C)] for l in range(R)]
    # here we have set the first row and column of S[][]
  
    # Construct other entries
    for i in range(1, R):
        for j in range(1, C):
            if (M[i][j] == 1):
                S[i][j] = min(S[i][j-1], S[i-1][j],
                            S[i-1][j-1]) + 1
            else:
                S[i][j] = 0
      
    # Find the maximum entry and
    # indices of maximum entry in S[][]
    max_of_s = S[0][0]
    #max_i = 0
    #max_j = 0
    for i in range(R):
        for j in range(C):
            if (max_of_s < S[i][j]):
                max_of_s = S[i][j]
                #max_i = i
                #max_j = j
    
    largest_value = 0
    the_closest_value_location = (0,0)
    for i in range(len(S)):
      for j in range(len(S[i])):
        if S[i][j] > largest_value:
          largest_value = S[i][j]
          the_closest_value_location = (i,j)
    
    # print("LARGEST VALUE" + str(largest_value))
    # print("Original Game Board")
    # for i in range(R):
    #     for j in range(C):
    #         print (M[i][j], end = " ")
    #     print("")

    # print("Matrix With Empty Space Weight")
    # for i in range(R):
    #     for j in range(C):
    #         print (S[i][j], end = " ")
    #     print("")
    return the_closest_value_location
  
# Driver Program
#Here, 1s are the empty spaces and 0s have food or snake
# M = [[0, 1, 1, 0, 1],
#     [1, 1, 0, 1, 0],
#     [0, 1, 1, 1, 0],
#     [1, 1, 1, 1, 0],
#     [1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0]]
  
#printMaxSubSquare(M)

def go_to_open_old(data, board, food_and_snakes, all_snake_body_parts):

  our_head = (data["you"]["head"]["x"],data["you"]["head"]["y"])
  open_space_star = strategy_A_Star.AStar()
  open_space_star.grid_height = data["board"]["height"]
  open_space_star.grid_width = data["board"]["width"]
  
  the_closest_open_value = findopenspace(board)
  #print("closet open value" + str(the_closest_open_value))
  open_space_star.init_grid(open_space_star.grid_width, open_space_star.grid_height, walls = food_and_snakes, start = our_head, end = the_closest_open_value)
  curr_path = open_space_star.solve()
  #print(curr_path)
  if curr_path is not None: 
    #print("paths sorted: ",all_paths)
    if (curr_path[1][0] < our_head[0]):
      move = "left"
    elif (curr_path[1][0] > our_head[0]):
      move = "right"
    elif (curr_path[1][1] < our_head[1]):
      move = "down"
    else:
      move = "up"
  else:
    possible_moves = strategy.determine_possible_moves(data, all_snake_body_parts)
    #and head towards open areas 
    move = random.choice(possible_moves)
  
  return move
