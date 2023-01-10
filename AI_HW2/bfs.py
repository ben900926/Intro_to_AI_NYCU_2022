import csv
edgeFile = 'edges.csv'
# the start of csv is sorted!

def bfs(start, end):
    # Begin your code (Part 1)
    """
    explanation : 
    construct the graph of the map from csv file using a dictionary that use start id as key, end ids and distances as values 
    create queues (using a list that append in end and pop in top : FIFO) for distance and path, 
    push the start into that of paths.
    create a list to store visited id.
    while the queue is not empty, pop the front from queue and push it into visited list, 
    if the front is a key of graph, visit the adjacent nodes of it
    for each non-visited adjacency, push it and new distance into queue.
    if one of these is the goal, return the path and distance and num_visited then end loop
    """
    # read the csv file 
    with open(edgeFile,newline='') as csvFile:
        rows = csv.reader(csvFile)
        # build a graph
        graph = dict()
        for row in rows:
            # store number only
            if row[0].isnumeric():
                k = int(row[0])
                # key not in dict
                if k not in graph:
                    graph[k] = list()
                graph[k].append(row)
        # start BFS
        queue = [[start]] # store path
        dist = [0.0] # list of distances
        visited = [start] # visited edges
        num_visited = 0
        # while the queue is not empty
        while len(queue) > 0:
            path = queue.pop(0) # front element
            path_dis = dist.pop(0) # current distance
            this_start = path[-1]
            # try if this start is a key of graph
            try:
                # for each adjacent 
                for row in graph[this_start]:
                    adj = int(row[1])
                    if adj not in visited:
                        num_visited +=1
                        # mark as visited
                        visited.append(adj)
                        # construct new path appending adjacent
                        new_path = list(path)
                        new_path.append(adj)
                        queue.append(new_path)
                        # new distance
                        new_dis = path_dis + float(row[2])
                        dist.append(new_dis)
                        # if found destination
                        if adj == end:
                            return new_path,new_dis,num_visited
            except KeyError: 
                continue
        # if not found
        return [],-1,-1
    # End your code (Part 1)
if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
