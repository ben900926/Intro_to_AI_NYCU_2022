import csv
edgeFile = 'edges.csv'
# something DFS needed
graph = dict()
reached_path = list() # record paths
visited = list()
num_visited = 0

# recursion version of DFS
def dfs_recur(start,end,path,dist):
    # marked as visited
    visited.append(start)
    path.append(start)
    # for adjacent
    for row in graph[start]:
        # already found
        if reached_path:
            return
        # next start
        adj = int(row[1])
        if adj not in visited:
            dist += float(row[2])
            num_visited += 1
            # reached end
            if adj == end:
                reached_path = path
            else:
                dfs_recur(adj,end,path,dist)

def dfs(start, end):
    # Begin your code (Part 2)
    # read the csv file 
    with open(edgeFile,newline='') as csvFile:
        rows = csv.reader(csvFile)
        # build a graph
        for row in rows:
            # store number
            if row[0].isnumeric():
                k = int(row[0])
                # key not in dict
                if k not in graph:
                    graph[k] = list()
                graph[k].append(row)
        
        # start DFS
        # recursion
        dfs_recur(start,end,[])
        return reached_path
        
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
