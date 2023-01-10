import csv
edgeFile = 'edges.csv'

def ucs(start, end):
    # Begin your code (Part 3)
    """
    explanation : 
    construct the graph of the map from csv file by using a dictionary that use start id as key, end ids and distances as values
    implement a priority queue as the frontier of UCS, which uses a list consists of lists of distance values and paths,
    and it's sorted by distance value. push start element to the priority queue
    create a list to store visited elements.
    while the priority queue is not empty, sort it first then pop its front element with min distance value,
    then push it to visited list. If this front is the goal, return the path and distance and num_visited then end loop
    else for each adjacency, if it's not in visited list or priority queue, push it with new path and distance
    if it's in priority queue and it contain a shorter path to the node, update this element with new values 
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
        # start UCS
        num_visited = 0
        # min priority queue
        pq = []
        visited = []
        # push path to start into pq
        pq.append([0.0,[start]])
        while len(pq)>0:
            pq = sorted(pq,key=lambda pq:pq[0]) # sort by distance
            this_list = pq.pop(0) # min distance and path : delete min
            dist = this_list[0]
            path = this_list[1]
            this_start = path[-1] # this start
            visited.append(this_start) # mark as visited
            # found destination
            if this_start == end:
                return path,dist,num_visited
            # try if this start is a key of graph
            try:
                # for each adjacent
                for row in graph[this_start]:
                    adj = int(row[1])
                    # check if adj is in pq and record index
                    adjINpq = False
                    i = 0
                    for l in pq:
                        if l[1][-1]==adj:
                            adjINpq = True
                            break
                        i+=1                       
                    # if adj not in visited or pq, insert it to pq
                    new_path = list(path)
                    new_path.append(adj)
                    new_dist = dist + float(row[2])
                    if (adj not in visited) and (not adjINpq):
                        num_visited += 1
                        pq.append([new_dist,new_path])
                    # if adj in pq, do decrease key
                    elif adjINpq and (pq[i][0] > new_dist):
                        pq[i][0] = new_dist
                        pq[i][1] = new_path
            except KeyError:
                continue
        # not found
        return [],-1,-1
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
