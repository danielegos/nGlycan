from collections import defaultdict

from prettytable import PrettyTable
from python.Lib.symbol import and_expr


# TODO: Fix this algorithm so it properly calculates the PCI as per the example

def compute_derived_values_from_dicts(circles, edges):

    # Step 1: Sort nodes by x-coordinate to determine layers
    sorted_nodes = sorted(circles.items(), key=lambda x: x[1][0])  # Sort by x-coordinate
    layers = {}
    current_layer = 1
    last_x = None

    # print("Printing circles and edges")
    # print("Circles:", circles)
    # print("Edges:", edges)
    # input("Press Enter to continue...\n")

    for node_id, (x, y, color) in sorted_nodes:
        if x != last_x:
            layers[current_layer] = [node_id]
            current_layer += 1
            last_x = x
        else:
            layers[current_layer - 1].append(node_id)

    # Step 2: Initialize storage for derived values
    results = defaultdict(dict)

    # print("Printing Results dict: ", results)

    # Step 3: Compute derived values for each layer
    for layer_num, node_ids in layers.items():
        # NMT: Count unique colors
        node_colors = {circles[node_id][2] for node_id in node_ids}
        NMT = len(node_colors)
        results[layer_num]['NMT'] = NMT
        # print("Printing Node_colors dict: ", node_colors)
        # print("Printing node_ids dict: ", node_ids, "Printing node_ids type: ", type(node_ids))


        # input("\nPress Enter to continue to TNU...")

        # TNU: Total number of nodes in the layer
        TNU = len(node_ids)
        results[layer_num]['TNU'] = TNU

        # NEL: Count inter-layer linkages
        NEL = 0
        edge_types = set()

        # NLT: Count distinct edge types
        for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
            # print("Edge ID: ", edge_id)
            # print("Nodes in Edge: ", (x1, y1), (x2, y2), edge_type)

            # If any edge in the edges_dict touches the node based on its node_id, increment NEL
            # if (x1, y1) == circles[node_id]

            for node_id in node_ids:
                # print("Printing circles[node_id]: ", circles[node_id])
                # print("Printing circles[node_id][0]: ", circles[node_id][0], "Printing circles[node_id][1]: ", circles[node_id][1])

                if (x1 == circles[node_id][0] and y1 == circles[node_id][1]) or (x2 == circles[node_id][0] and y2 == circles[node_id][1]):
                    NEL += 1
                    edge_types.add(edge_type)

            #
            # nodes_in_edge = {x1, x2}
            # nodes_in_layer = set(node_ids)
            # # print("\nPrinting edge types dict: ", edge_type)
            # # print("Printing nodes dict: ", nodes_in_edge)
            # # print("Printing nodes in layer: ", nodes_in_layer)
            #
            # # If the edge connects nodes from the current layer to another layer
            # if nodes_in_edge & nodes_in_layer:
            #     # Count inter-layer linkages
            #     if (nodes_in_edge & nodes_in_layer) != nodes_in_layer:
            #         NEL += 1
            #
            #     # Track edge types for NLT
            #     edge_types.add(edge_type)

        results[layer_num]['NEL'] = NEL

        NLT = len(edge_types)

        results[layer_num]['NLT'] = NLT

        # print("Printing Edge_colors dict: ", edge_types)

        # print("Layer ", layer_num)
        # input("Press Enter to begin NCDSPL calculation\n")
        # NCDSPL: Count nodes connecting to different colored nodes in the previous layer
        NCDSPL = 0
        if layer_num > 1:
            previous_layer_nodes = layers[layer_num - 1]
            print("previous_layer_nodes:", previous_layer_nodes)
            for node_id in node_ids:
                # print("Printing node color of node in this layer:", circles[node_id][2])
                # Get colors of all nodes in layers
                node_color = circles[node_id][2]
                for edge_id, ((x1, y1), (x2, y2), edge_type) in edges.items():
                    # Loop over previous layer nodes
                    for previous_node_id in previous_layer_nodes:
                        # If the previous node and the current node are connected by an edge (check x and y values),
                        # then if their colors are different, increment NCDSPL
                        # print("Previous Node ID: ", previous_node_id)
                        # print("circles[previous_node_id]:", circles[previous_node_id])
                        #
                        if ((circles[previous_node_id][0] == x1 and circles[previous_node_id][1] == y1) and (circles[node_id][0] == x2 and circles[node_id][1] == y2)) or \
                                ((circles[previous_node_id][0] == x2 and circles[previous_node_id][1] == y2) and (circles[node_id][0] == x1 and circles[node_id][1] == y1)):
                            if circles[previous_node_id][2] != circles[node_id][2]:
                                NCDSPL += 1

        results[layer_num]['NCDSPL'] = NCDSPL

        # Add layer score
        results[layer_num]['Layer Score'] = NMT + TNU + NEL + NLT + NCDSPL



    return results


# circles_dict = {91: (160, 200, '#24A5A2'), 92: (320, 200, '#24A5A2'), 93: (480, 200, '#24A5A2'), 94: (640, 200, '#24A5A2'), 95: (480, 360, '#24A5A2'), 104: (800, 200, '#92548A'), 107: (640, 360, '#7BB23C')}
# edges_dict =  {96: ((480, 360), (320, 200), 'a1to4'), 98: ((320, 200), (480, 200), 'a1to4'), 100: ((640, 200), (480, 200), 'a1to6'), 102: ((160, 200), (320, 200), 'a1to2'), 105: ((640, 200), (800, 200), 'a1to6'), 108: ((480, 360), (640, 360), 'a1to2')}

circles_dict = {91: (120, 160, '#24A5A2'), 92: (280, 160, '#24A5A2'), 93: (280, 320, '#AA4926'), 94: (440, 160, '#7BB23C'), 95: (600, 160, '#7BB23C'), 96: (760, 160, '#7BB23C'), 97: (920, 160, '#7BB23C'), 98: (1080, 160, '#24A5A2'), 99: (1240, 160, '#24A5A2'), 100: (1400, 160, '#24A5A2'), 101: (440, 320, '#7BB23C'), 102: (600, 320, '#7BB23C'), 103: (760, 320, '#7BB23C'), 104: (920, 320, '#7BB23C'), 105: (760, 480, '#7BB23C'), 106: (920, 480, '#7BB23C')}
edges_dict = {107: ((120, 160), (280, 320), 'a1to6'), 109: ((120, 160), (280, 160), 'b1to4'), 111: ((280, 160), (440, 160), 'b1to4'), 113: ((440, 160), (600, 160), 'a1to3'), 115: ((600, 160), (760, 160), 'a1to2'), 117: ((760, 160), (920, 160), 'a1to2'), 119: ((920, 160), (1080, 160), 'a1to3'), 121: ((1080, 160), (1240, 160), 'a1to3'), 123: ((1240, 160), (1400, 160), 'a1to2'), 125: ((440, 160), (600, 320), 'a1to6'), 127: ((600, 320), (760, 480), 'a1to6'), 129: ((600, 320), (760, 320), 'a1to3'), 131: ((760, 320), (920, 320), 'a1to2'), 133: ((760, 480), (920, 480), 'a1to2')}

circles_dict_2 =  {91: (80, 80, '#24A5A2'), 92: (240, 80, '#24A5A2'), 93: (400, 80, '#7BB23C'), 94: (560, 80, '#7BB23C'), 95: (720, 80, '#7BB23C'), 96: (880, 80, '#7BB23C'), 97: (1040, 80, '#24A5A2'), 98: (1200, 80, '#24A5A2'), 99: (1360, 80, '#24A5A2'), 100: (240, 240, '#AA4926'), 101: (560, 240, '#7BB23C'), 102: (720, 240, '#7BB23C'), 103: (880, 240, '#7BB23C'), 104: (720, 400, '#7BB23C'), 105: (880, 400, '#7BB23C')}
edges_dict_2 =  {106: ((80, 80), (240, 240), 'a1to6'), 108: ((80, 80), (240, 80), 'b1to4'), 110: ((240, 80), (400, 80), 'b1to4'), 112: ((400, 80), (560, 80), 'a1to3'), 114: ((400, 80), (560, 240), 'a1to6'), 116: ((560, 80), (720, 80), 'a1to2'), 118: ((720, 80), (880, 80), 'a1to2'), 120: ((560, 240), (720, 240), 'a1to3'), 122: ((720, 240), (880, 240), 'a1to2'), 124: ((560, 240), (720, 400), 'a1to6'), 126: ((720, 400), (880, 400), 'a1to2'), 128: ((880, 80), (1040, 80), 'a1to3'), 130: ((1040, 80), (1200, 80), 'a1to3'), 132: ((1200, 80), (1360, 80), 'a1to2')}


#
# pci_calculation_result = compute_derived_values_from_dicts(circles_dict, edges_dict)
# print(pci_calculation_result)


pci_calculation_result2 = compute_derived_values_from_dicts(circles_dict_2, edges_dict_2)
print(pci_calculation_result2)