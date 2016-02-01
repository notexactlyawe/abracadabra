import numpy as np

def graph_ascii(some_list, graph_max=None, graph_min=None, resolution=10):
    if graph_max is None:
        graph_max = np.max(some_list)
#        print "max in array: {0}".format(graph_max)
    if graph_min is None:
        graph_min = np.min(some_list)
#        print "min in array: {0}".format(graph_min)
    if graph_max == graph_min:
        range_graph = 1 
    else:
        range_graph = graph_max - graph_min
    # create array to print
    to_graph = [[" " for _ in range(len(some_list))] for _ in range(resolution + 1)]

    x_val = 0
    for item in some_list:
        temp_height = (float(item - graph_min) / (range_graph))
        height = int(temp_height * resolution) + 1
#        print "{0} has gone to {1}".format(item, height)
        for y_val in range(height):
#            print "X Y: {0}, {1}".format(x_val, y_val)
            to_graph[y_val][x_val] = "*"
        x_val += 1
    
    for line_no in range(len(to_graph) - 1, -1, -1):
        print "".join(to_graph[line_no])

if __name__ == "__main__":
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    test_2 = [5, 5, 5, 5, 5]
    test_3 = [1, 3, 3, 3, 3, 5]
    
    print "test_data"
    graph_ascii(test_data)
    raw_input("Press enter to continue")
    print "test_2"
    graph_ascii(test_2)
    raw_input("Press enter to continue")
    print "test_3"
    graph_ascii(test_3)
