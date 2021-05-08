import os
import cherrypy
import global_variables as gv
#have a library with our strategy
import strategy
import strategy_open
import copy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
"""
other snakes to challenge:
daliusd - Bender
altersaddle - hotsoup
JFMarten  - Queueueue
 derektcw98 - RiikuSnek
"""

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "👑 William Snakespeare 👑",  # TODO: Your Battlesnake Username
            "color": "#cc0000",  # TODO: Personalize
            "head": "tiger-king",  # TODO: Personalize
            "tail": "bolt",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json
        
        gv.BOARD_MAX_X = data["board"]["width"]
        gv.BOARD_MAX_Y = data["board"]["height"]

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        snake_walls = []
        other_snakes_wall = []
        food_and_snakes = []
        all_food = []
        board = []
        length_of_each_snake = []
        #populating an empty board 
        for row in range(gv.BOARD_MAX_X):
          board.append([])
          for column in range(gv.BOARD_MAX_Y):
            board[row].append(1)

        #populating snake parts
        #have list of our other snakes body parts that will act as our walls
        all_snake_body_parts = strategy.other_snakes(data)
        for part in all_snake_body_parts:
          snake_walls.append((part["x"], part["y"]))
          board[part["x"]][part["y"]] = 0
          if part not in data["you"]["body"]:
            other_snakes_wall.append((part["x"], part["y"]))


        #populating all the food
        all_food_data = data["board"]["food"]
        for food in all_food_data:
          all_food.append((food["x"], food["y"]))
          board[food["x"]][food["y"]] = 0

        food_and_snakes = copy.deepcopy(snake_walls)
        for food in all_food_data:
          food_and_snakes.append((food["x"], food["y"]))

        curr_number_of_snakes = len(data["board"]["snakes"])
        snakes = data["board"]["snakes"]
        our_length = data["you"]["length"]
        curr_total_length = 0
        #get length of each snake
        for snake in snakes:
          if snake["name"] != data["you"]["name"]:
            length_of_each_snake.append(snake["length"])

        curr_total_length = len(other_snakes_wall)
        avg_length = (curr_total_length)/curr_number_of_snakes
        ##########3 or less Snakes###############
        if curr_number_of_snakes <= 2:
          if data["you"]["health"] > 90 and our_length < avg_length:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
            if move is not None:
              print(f"MOVE: {move}")
              return {"move": move}
          else: #go for food
            move = strategy.go_for_food_Dij(data,snake_walls, other_snakes_wall, all_food)
            if move is None:
              move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
              if move is not None:
                print(f"MOVE: {move}")
                return {"move": move}
        else:#multiple snakes 
          if data["you"]["health"] > 95 and our_length < 5:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
            if move is not None:
              print(f"MOVE: {move}")
              return {"move": move}
          else: #go for food
            move = strategy.go_for_food_Dij(data,snake_walls, other_snakes_wall, all_food)
            if move is None:
              move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
              if move is not None:
                print(f"MOVE: {move}")
                return {"move": move}
        #######################################


        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
