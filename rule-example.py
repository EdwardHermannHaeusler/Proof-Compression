import pydotplus as pd
import graphviz
import Rules
import json

def create_graph():

    g = pd.graphviz.Dot(graph_type='digraph')
    e_in = {}
    e_out = {}
    # Adicione os nós (nodes) ao gráfico
    node_P1 = pd.graphviz.Node("p1")
    node_P2 = pd.graphviz.Node("p4")
    node_u = pd.graphviz.Node("u")
    node_f1 = pd.graphviz.Node("f1")
#    node_f2 = pd.graphviz.Node("f3")

    node_P3 = pd.graphviz.Node("p2")
    node_P4 = pd.graphviz.Node("p3")
    node_v = pd.graphviz.Node("v")
    node_f2 = pd.graphviz.Node("f2")

#    node_n1 = pd.graphviz.Node("n1")
#    node_n2 = pd.graphviz.Node("n2")

    g.add_node(node_P1)
    g.add_node(node_P2)
    g.add_node(node_P3)
    g.add_node(node_P4)
    g.add_node(node_u)
    g.add_node(node_v)
    g.add_node(node_f1)
    g.add_node(node_f2)
#    g.add_node(node_f3)

#    g.add_node(node_n1)
#    g.add_node(node_n2)



    # Adicione as arestas (edges) ao gráfico
    edge_1 = pd.graphviz.Edge(node_P1, node_u, label=0, color = "black")
    edge_2 = pd.graphviz.Edge(node_P2, node_u, label=0, color = "black")
    edge_3 = pd.graphviz.Edge(node_u, node_f1, label=0, color = "black")
#    edge_4 = pd.graphviz.Edge(node_u, node_f2, label=1, color = "black")

    edge_5 = pd.graphviz.Edge(node_P3, node_v, label=0, color = "black")
    edge_6 = pd.graphviz.Edge(node_P4, node_v, label=0, color = "black")
    edge_7 = pd.graphviz.Edge(node_v, node_f2, label=0, color = "black")

    #ancestralidade

#    edge_8 = pd.graphviz.Edge(node_f1, node_P1, label= ["0"], color = "blue")
#    edge_9 = pd.graphviz.Edge(node_f2, node_P2, label= ["1"], color = "blue")

#    edge_10 = pd.graphviz.Edge(node_n1, node_u, label= ["0"], color = "blue")

    g.add_edge(edge_1)
    g.add_edge(edge_2)
    g.add_edge(edge_3)
#    g.add_edge(edge_4)
    g.add_edge(edge_5)
    g.add_edge(edge_6)
    g.add_edge(edge_7)
#    g.add_edge(edge_8)
#    g.add_edge(edge_9)

#    g.add_edge(edge_10)

    for vertex in g.get_nodes():
        e_in[vertex.get_name()] = []
        e_out[vertex.get_name()] = []
    for edge in g.get_edges():
        v_in = edge.get_destination()
        v_out = edge.get_source()
        #if edge.get_color() == "black":
        e_in[v_in].append(edge)
        e_out[v_out].append(edge)

    return g, e_in, e_out







graph,e_in,e_out = create_graph()

print("Vértices no grafo original:")
for node in graph.get_nodes():
    print(node.get_name())

print("Arestas no grafo original:")
for edge in graph.get_edges():
    print(edge.get_source() + "-" + edge.get_destination(), edge.get_label(), edge.get_color())


printable_graph= Rules.printable_version(graph)

printable_graph.write("imgRules/grafoTestePrintable.dot")

print("Vértices no grafo printable_graph:")
for node in printable_graph.get_nodes():
    print(node.get_name())

print("Arestas no grafo printable_graph")
for edge in printable_graph.get_edges():
    print(edge.get_source() + "-" + edge.get_destination(), edge.get_label(), edge.get_color())




node_u = Rules.find_node_by_name(graph, "u")
node_v = Rules.find_node_by_name(graph, "v")

f = open("RegraR0EE.json", "r")
json_data = json.load(f)
f.close()
graph = Rules.GetRuleCode(json_data, graph, node_u, node_v, e_in, e_out)

printable_graph= Rules.printable_version(graph)

printable_graph.write("imgRules/grafoTestePrintableAfterRule.dot")

# print("Vértices no gráfico:")
# for node in graph.get_nodes():
#     print(node.get_name())

# print("Arestas no grafo")
# for edge in graph.get_edges():
#     print(edge.get_source() + "-" + edge.get_destination(), edge.get_label(), edge.get_color())
