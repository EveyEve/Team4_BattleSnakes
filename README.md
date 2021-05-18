# Route Strategy

William Snakespeare has little desire to miggle with fools lesser than itself. Using the A* implementation with a mix of Dijkstra's algorithm, it searches for food, but will also avoid food when nearly because a king does not want to seem gluttonous to his subjects. He simply minds his own business and heads towards open areas when he doesn't require food. The Dijkstra's algorithm is also altered as  the weight (value) of each cell in the grid is influenced by how near or far it is to other snakes or the edge of the gameboard. The background on the algorithms and the code can be found here : https://www.redblobgames.com/pathfinding/a-star/implementation.html#troubleshooting-ugly-path

# Many Possible Improvments
* The king neither runs or attacks. Would be nice if does one (probably the later since he can grow fast) 
* At the start of the game, the king should head towards open areas to avoid immediate collision when searching for food
* Possibly implement strategies like minimax to improve its survival rate instead of A* implementation alone 
* Clean up the code. Had a short time frame. Our Dij Algorithm was built on the A* implementation code. 
* Whatever you see fit! We coded this in one week essentially 

![WilliamSnakespeare](https://user-images.githubusercontent.com/78228835/118735578-ba533400-b80e-11eb-9a68-86698ab09ca4.png)
