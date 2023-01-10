import csv
edgeFile = 'edges.csv'

def dfs(start, end):
    # Begin your code (Part 2)
    """
    explanation : 
    construct the graph of the map from csv file by using a dictionary that use start id as key, end ids and distances as values
    similar to BFS, create a stack (using a list that both append and pop elements in the end) to store paths and distances
    push the start to that of path.
    create a list to store visited elements.
    while the stack is not empty, pop an element from the back of it and push the element to visited list
    if this element is a key of graph, visit its every adjacency.
    for each non-visited adjacency, push it and new distance to stack
    if it is the goal, return the path and distance and num_visited then end loop
    """
    # read the csv file 
    with open(edgeFile,newline='') as csvFile:
        rows = csv.reader(csvFile)
        # build a graph
        graph = dict()
        for row in rows:
            # store number
            if row[0].isnumeric():
                k = int(row[0])
                # key not in dict
                if k not in graph:
                    graph[k] = list()
                graph[k].append(row) 
        # start DFS
        stack = [[start]] # record paths
        dist = [0.0] #distance
        visited = []
        num_visited = 0
        # similar to BFS, using stack instead of queue
        while stack:
            # get this path and its distance
            path = stack.pop(-1)
            path_dis = dist.pop(-1)
            this_start = path[-1] # last node
            # mark as visited
            if this_start not in visited:
                visited.append(this_start)
            # try if this start is a key of graph
            try:
                for row in graph[this_start]:
                    adj = int(row[1])
                    # not visited
                    if adj not in visited:
                        num_visited += 1
                        # add new path to stack
                        new_path = list(path)
                        new_path.append(adj)
                        stack.append(new_path)
                        # add new distance to stack
                        new_dis = path_dis + float(row[2])
                        dist.append(new_dis)
                        # found destination
                        if adj == end:
                            return new_path,new_dis,num_visited
            # not found key
            except KeyError:
                continue
        # if not found
        return [],-1,-1

    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
