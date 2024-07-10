import pydotplus as pd
import graphviz
import pyparsing
import csv
import re
import sets
import json

# def create_graph():

#     g = pd.graphviz.Dot(graph_type='digraph')
#     e_in = {}
#     e_out = {}
#     # Adicione os nós (nodes) ao gráfico
#     node_P1 = pd.graphviz.Node("p1")
#     node_P2 = pd.graphviz.Node("p4")
#     node_u = pd.graphviz.Node("u")
#     node_f1 = pd.graphviz.Node("f1")
#     node_f2 = pd.graphviz.Node("f3")

#     node_P3 = pd.graphviz.Node("p2")
#     node_P4 = pd.graphviz.Node("p3")
#     node_v = pd.graphviz.Node("v")
#     node_f3 = pd.graphviz.Node("f2")

#     node_n1 = pd.graphviz.Node("n1")
#     node_n2 = pd.graphviz.Node("n2")

#     g.add_node(node_P1)
#     g.add_node(node_P2)
#     g.add_node(node_P3)
#     g.add_node(node_P4)
#     g.add_node(node_u)
#     g.add_node(node_v)
#     g.add_node(node_f1)
#     g.add_node(node_f2)
#     g.add_node(node_f3)

#     g.add_node(node_n1)
#     g.add_node(node_n2)



#     # Adicione as arestas (edges) ao gráfico
#     edge_1 = pd.graphviz.Edge(node_P1, node_u, label=0, color = "black")
#     edge_2 = pd.graphviz.Edge(node_P2, node_u, label=0, color = "black")
#     edge_3 = pd.graphviz.Edge(node_u, node_f1, label=0, color = "black")
#     edge_4 = pd.graphviz.Edge(node_u, node_f2, label=1, color = "black")

#     edge_5 = pd.graphviz.Edge(node_P3, node_v, label=0, color = "black")
#     edge_6 = pd.graphviz.Edge(node_P4, node_v, label=0, color = "black")
#     edge_7 = pd.graphviz.Edge(node_v, node_f3, label=0, color = "black")

#     #ancestralidade

#     edge_8 = pd.graphviz.Edge(node_f1, node_P1, label= "[0]", color = "blue")
#     edge_9 = pd.graphviz.Edge(node_f2, node_P2, label= "[1]", color = "blue")

#     edge_10 = pd.graphviz.Edge(node_n1, node_u, label= "[0]", color = "blue")

#     g.add_edge(edge_1)
#     g.add_edge(edge_2)
#     g.add_edge(edge_3)
#     g.add_edge(edge_4)
#     g.add_edge(edge_5)
#     g.add_edge(edge_6)
#     g.add_edge(edge_7)
#     g.add_edge(edge_8)
# #    g.add_edge(edge_9)

# #    g.add_edge(edge_10)

#     for vertex in g.get_nodes():
#         e_in[vertex.get_name()] = []
#         e_out[vertex.get_name()] = []
#     for edge in g.get_edges():
#         v_in = edge.get_destination()
#         v_out = edge.get_source()
#         #if edge.get_color() == "black":
#         e_in[v_in].append(edge)
#         e_out[v_out].append(edge)

#     return g, e_in, e_out

def printable_version(g):
    gp = pd.graphviz.Dot(graph_type='digraph')
    for v in g.get_nodes():
        gp.add_node(pd.graphviz.Node(v.get_name()))
    for e in g.get_edges():
        if type(e.get_label())==list:
           list_as_string="["
           for d in e.get_label():
               list_as_string=list_as_string+str(d)   
           list_as_string=list_as_string+"]"    
           gp.add_edge(pd.graphviz.Edge(e.get_source(),
                                        e.get_destination(),
                                        label= list_as_string,
                                        color = e.get_color()))
           
        else: 
           gp.add_edge(pd.graphviz.Edge(e.get_source(),
                                        e.get_destination(),
                                        label= e.get_label(),
                                        color = e.get_color()))
    return gp


def create_json():
    json_string = '''
    {
    
    "name": "R1XE",
    "edges": ["apartamento-v","escritorio-v","v-estrela"],
    "new_edges":[
        {
            "edge_name": "apartamento-u",
            "edge_label": 0
        },
        {
            "edge_name": "u-estrela",
            "edge_label": -2
        },
        {
            "edge_name": "escritorio-u",
            "edge_label": 0
        }

    ],
    "ancestor_edges":[],
    "new_ancestor_edges":[
        {
            "edge_name": "estrela-escritorio",
            "edge_label": ["-2"]
        },
        {
            "edge_name": "estrela-apartamento",
            "edge_label": ["-2"]
        }
    ],
    "delete_edges":["apartamento-v","escritorio-v","v-estrela"]
    }
    '''
    return json_string
def find_node_by_name(graph, target_name):
    for node in graph.get_nodes():
        if node.get_name() == target_name:
            return node
    return None

def find_all_nodes_json(json_data, vertex_u, vertex_v, e_in, e_out):
    dict_vertex = {}
    dict_edges = {}
    dict_labels = {}
    used_edges = []
    dict_vertex["u"] = vertex_u.get_name()
    dict_vertex["v"] = vertex_v.get_name()
    missing_edges = []
    for edge in json_data["edges"]:
        vertex_out, vertex_in = edge.split('-')
        if(vertex_in in dict_vertex):
            index = 0
            while(e_in[dict_vertex[vertex_in]][index] in used_edges):
                index = index + 1
            used_edges.append(e_in[dict_vertex[vertex_in]][index])
            dict_edges[edge] = e_in[dict_vertex[vertex_in]][index]
            if(vertex_out not in dict_vertex):
                dict_vertex[vertex_out] = e_in[dict_vertex[vertex_in]][index].get_source()
                

        elif(vertex_out in dict_vertex):
            index = 0
            while(e_out[dict_vertex[vertex_out]][index] in used_edges):
                index = index + 1
            used_edges.append(e_out[dict_vertex[vertex_out]][index])   
            dict_edges[edge] = e_out[dict_vertex[vertex_out]][index]
            
            if(vertex_in not in dict_vertex):
                dict_vertex[vertex_in] = e_out[dict_vertex[vertex_out]][index].get_destination()
        else:
            missing_edges.append(edge)
        for missing_edge in missing_edges:
            vertex_out, vertex_in = missing_edge.split('-')
            if(vertex_in in dict_vertex):
                index = 0
                while(e_in[dict_vertex[vertex_in]][index] in used_edges):
                    index = index + 1
                used_edges.append(e_in[dict_vertex[vertex_in]][index])
                dict_edges[missing_edge] = e_in[dict_vertex[vertex_in]][index]
                if(vertex_out not in dict_vertex):
                    dict_vertex[vertex_out] = e_in[dict_vertex[vertex_in]][index].get_source()
                

            elif(vertex_out in dict_vertex):
                index = 0
                while(e_out[dict_vertex[vertex_out]][index] in used_edges):
                    index = index + 1
                used_edges.append(e_out[dict_vertex[vertex_out]][index])   
                dict_edges[missing_edge] = e_in[dict_vertex[vertex_out]][index]
                
                if(vertex_in not in dict_vertex):
                    dict_vertex[vertex_in] = e_out[dict_vertex[vertex_out]][index].get_destination()
    for edge in json_data["ancestor_edges"]:
        vertex_out, vertex_in = edge["edge_name"].split('-')
        index = 0
        target_edge = e_in[dict_vertex[vertex_in]][index]
        while target_edge.get_color() != "blue":
            index = index + 1
            target_edge = e_in[dict_vertex[vertex_in]][index]

        dict_edges[edge["edge_name"]] = target_edge
        if(vertex_out not in dict_vertex):
            dict_vertex[vertex_out] = target_edge.get_source()
        label_list = edge["edge_label"]
        try:
            int(label_list[0])

        except ValueError:
            dict_labels[label_list[0]] = target_edge.get_label()

    return dict_vertex, dict_edges, dict_labels
def find_dict_labels(node_u,e_out, dict_labels):
    biggest_label = 0
    for edge in e_out[node_u.get_name()]:
        label = edge.get_label()
        if label is None:
            label = 0
        if label > biggest_label:
            biggest_label = label
    list_biggest_label = []
    list_biggest_label.append(str(biggest_label))
    dict_labels["m"] = list_biggest_label

    return dict_labels
def add_ancestor_edges(graph,json_data, dict_label, dict_vertex):
    for edge in json_data["new_ancestor_edges"]:
        label_list = edge["edge_label"]
        for index, label in enumerate(label_list):
            try:
                print("Tipos ",type(label), type(index))
                int_label = int(label)
                if int_label < 0:
                     biggest_label = dict_label["m"][0]
                     new_label = -1* (int_label + 1) + int(biggest_label)
                     label_list[index]  = str(new_label)

            except ValueError:
                label_list = (label_list[0:index]) + dict_label[label]  + (label_list[index + 1:len(label_list)])
        vertex_out , vertex_in = edge["edge_name"].split('-')
        parsed_vertex_out = find_node_by_name(graph,dict_vertex[vertex_out])
        parsed_vertex_in = find_node_by_name(graph,dict_vertex[vertex_in])
        new_edge = pd.graphviz.Edge(parsed_vertex_out, parsed_vertex_in, label = label_list, color = "blue")
        graph.add_edge(new_edge)
    return graph
def add_edges(graph,json_data, dict_labels, dict_vertex):
    edge_color = "black"
    for edge in json_data["new_edges"]:
        new_label = edge["edge_label"]
        if new_label < 0:
            if new_label == -100:
                edge_color = "green"
            else:
                biggest_label = dict_labels["m"][0]
                new_label = -1* (new_label + 1) + int(biggest_label)

        vertex_out , vertex_in = edge["edge_name"].split('-')
        parsed_vertex_out = find_node_by_name(graph,dict_vertex[vertex_out])
        parsed_vertex_in = find_node_by_name(graph,dict_vertex[vertex_in])
        new_edge = pd.graphviz.Edge(parsed_vertex_out, parsed_vertex_in, label= new_label, color = edge_color)
        graph.add_edge(new_edge)
        
    return graph

def delete_edges(graph, json_data, dict_edges):
    for edge in json_data["delete_edges"]:
        parsed_edge = dict_edges[edge]
        graph.del_edge(parsed_edge.get_source(), parsed_edge.get_destination())
    return graph


def GetRuleCode(json_data, graph, node_u, node_v, e_in, e_out):
    

    dict_vertex, dict_edges, dict_labels = find_all_nodes_json(json_data, node_u,node_v, e_in, e_out)
    dict_labels = find_dict_labels(node_u, e_out, dict_labels)
    graph = add_edges(graph,json_data, dict_labels, dict_vertex)
    graph = delete_edges(graph, json_data, dict_edges)
    graph = add_ancestor_edges(graph,json_data, dict_labels, dict_vertex)

    graph.del_node(node_v.get_name())

    print("vertices \n")
    print(dict_vertex)
    print("\n")
    print(dict_edges)
    print("\n")
    print(dict_labels)
    print("\n")
    return graph


#graph,e_in,e_out = create_graph()

#graph.write("imgRules/grafoTeste.dot")

# node_u = find_node_by_name(graph, "u")
# node_v = find_node_by_name(graph, "v")

# json_data = json.loads(create_json())
# graph = GetRuleCode(json_data, graph, node_u, node_v, e_in, e_out)



# print("Vértices no gráfico:")
# for node in graph.get_nodes():
#     print(node.get_name())

# print("Arestas no grafo")
# for edge in graph.get_edges():
#     print(edge.get_source() + "-" + edge.get_destination(), edge.get_label(), edge.get_color())

# graph.write("imgRules/grafoTesteAfterRule.dot")    
