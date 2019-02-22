from tinydb import TinyDB, Query
db=TinyDB('testworld.json')
db2=TinyDB('testworld2.json')

width=10
height=10
grid =  {x:{y:False for y in range(height)} for x in range(width)}

grid2 =  grid
for x in range(height):
    for y in range(width):
        grid2[x][y] = grid[x][y] 

db.insert(grid)
db2.insert(grid2)
print(db2.all())
