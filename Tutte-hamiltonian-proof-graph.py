#!/usr/local/bin/python
# coding: utf-8

import pydotplus as pd
import graphviz
import pyparsing
import csv
import re
import sets



def tab_coloring(gin):
    tab={}
    color=0
    for no in gin.get_node_list():
        # print "NO="+no.to_string()
        # print "NOGETLABEL="+str(no.get('label'))
        if not tab.has_key(no.get('label')):
            tab[no.get('label')]=color
            color=color+1
    return tab

def draw_discharging_edges(gin):
    global discharged_occurrences
    global conclusions
#    print "Entrou no draw_discharging_edges"
    for no in gin.get_node_list():
#        print "LABEL DISCHARGING ="+no.get('label')
        if re.match(r'\[.+\][0-9]+',no.get('label')):
           m=re.search(r'\[.+\]([0-9][0-9a-z]*)',no.get('label'))
#           print "====> "+no.get('label')+" ="+m.group(1)
           if discharged_occurrences.get(m.group(1),"empty")=="empty":
              discharged_occurrences[m.group(1)]=[no]
           else:
              discharged_occurrences[m.group(1)].append(no)
        if re.match(r'.+[\s]([0-9][0-9a-z]*)',no.get('label')):
           m=re.match(r'.+[\s]([0-9][0-9a-z]*)',no.get('label'))
#           print "ACHOU descarte ="+m.group(1)
           if conclusions.get(m.group(1),"empty")=="empty":
              conclusions[m.group(1)]=no
           else:
              print "prova errada"
    for i,l in discharged_occurrences.items():
        for nd in l:
#            print "adicionando aresta de "+nd.get('label')+" para "+conclusions[i].get('label')
         if conclusions.has_key(i):
           gin.add_edge(pd.Edge(nd,conclusions[i],color="red"))
#    print "IMPRIMINDO DE DENTRO DE DRAWING"
#    z=raw_input(" PAROU ")
#    print gin.to_string()
#    print "SAINDO do draw_discharging_edges"
    print discharged_occurrences
    print conclusions
    return gin

def coloring(gin,tab):
    for n in gin.get_nodes():
         print "NO="+n.to_string()
         print "NOGETLABEL="+str(n.get('label'))+" ANTES=>"
         if tab.has_key(n.get('label')):
            print "VALORTAB[LABEL]="+str(tab[n.get('label')])
            n.set_label(tab[n.get('label')])
         print "NOGETLABEL="+str(n.get('label'))+" =>DEPOIS"
         print n.to_string()
    return gin



def node_id_hid(s):
    return pd.Node(vertex_id(s),label=vertex_label(s))


def is_labeled_formula(form):
    if re.match(r'[0-9]+=X[0-9]*v[0-9][0-9]?', form):
       return True
    else:
       return False

def vertex_name(w):
    i=0
    while w[i] <> "v":
       i=i+1
    return w[i:]

def vertex_id(w):
    i=0
    while w[i]<> "=":
       i=i+1
    return w[:i]

def vertex_label(w):
##    print "vertex_labl = "+w
    i=0
    while (w[i]<> "X") and (w[i]<> "O") and (w[i]<> "(") and (w[i]<>"q") and (w[i]<>"["):
       i=i+1
    return w[i:]

def maior(y,v):
    i=0
    while y[i] <> "v":
      i=i+1
    if i == 0:
      ya=y[(i+1):]
    i=0
    while v[i] <> "v":
      i=i+1
    if i == 0:
      va=v[i+1:]
##    print ya, va
    return int(va)<int(ya)

def get_k(v,vis):
    for ((i,w),j) in vis:
      if igual(v,w):
        i1=i
    return i1

def get_descarte(v,vis):
    for ((i,w),j) in vis:
      if igual(v,w):
        j1=j
    return j1

def igual(c1, c2):
 if not c1 or not c1:
  return False
 else:
   i=0
   l1=len(c1)
   l2=len(c2)
   while i<=l1-1 and i<=l2-1 and c1[i]==c2[i]:
       i=i+1
   return c1[i-1]==c2[i-1] and i==l1 and i==l2


def linked(g,a,b):
   l=g.get_edge_list()
   res=False
   for e in l:
     if igual(e.get_source(),a) and igual(e.get_destination(),b):
        res=True
   return res

def Deduction_Edge(s,d):
   global e_in
   global e_out
#   print "CRIANDO EDGE de "+ s.get_name()+ "Para "+d.get_name()
#   print "CRIANDO EDGE de "+ s.get_label()+ "Para "+d.get_label()
#  Tem efeito nulo se ja existe aresta de s para d. O grafo de prova eh um grafo simples colorido (no maximo uma aresta de
#  cada cor entre cada par de vertices
   if not e_in.has_key(d.get_name()):
      e_in[d.get_name()]=[]
   if not e_out.has_key(s.get_name()):
      e_out[s.get_name()]=[]
   e=pd.Edge(s,d)
   e_out[s.get_name()].append(e)
   e_in[d.get_name()].append(e)
   return e

def Double_Deduction_Edge(s,d):
   print s
   v1 = sets.Set(e_out[s.get_name()])
   print "conjunto v1"
   v1_labels={(x.get_source(),x.get_destination()) for x in v1}
   print v1
   print v1_labels
   print s.get_label()
   v2 = e_in[d.get_name()]
   print "conjunto v2"
   v2_edges=sets.Set({(x.get_source(),x.get_destination()) for x in v2})
   print v2
   print v2_edges
   print d.get_label()
   inter = v1.intersection(v2)
   print "INtersecao ===================="
   print inter
   return inter



def Ancestor_Edge(s,d):
   global e_in_A
   global e_out_A
   if not e_in_A.has_key(d.get_name()):
      e_in_A[d.get_name()]=[]
   if not e_out_A.has_key(s.get_name()):
      e_out_A[s.get_name()]=[]
   e=pd.Edge(s,d,label='Ancestor', color="blue")
   e_out_A[s.get_name()].append(e)
   e_in_A[d.get_name()].append(e)
   return e




# def associative_source_and_target_lists(g):
#    list_in={}
#    list_out={}
#    edges=g.get_edge_list()
#    nodes=g.get_node_list()
#    for ns in nodes:
#       list_out[ns.get_name()]=[]
#       list_in[ns.get_name()]=[]
#       for e in edges:
#           if igual(e.get_source(),ns.get_name()) and not igual(e.get('color'),'red'):
#              list_out[ns.get_name()].append(e)
#              print "aresta= "+e.to_string()+" tem indice em list_out= "+ns.get_name()
#           if igual(e.get_destination(),ns.get_name()) and not igual(e.get('color'),'red'):
#              list_in[ns.get_name()].append(e)
#              print "aresta= "+e.to_string()+" tem indice em list_in= "+ns.get_name()
#    return (list_out,list_in)

def find_root(g):
#  print e_out
  global e_out
  global e_in
#  print "Vai encontrar raiz"
  n=g.get_node_list()
  i=0
  while i < len(n) and not (n[i]):
     # print "i="+str(i)
     i=i+1
  na=n[i]
  # print "na="+na.get_name()
  # print "label="+g.get_node(na.get_name())[0].get_label()
  # print "na="+na.get_name()+"label="+g.get_node(na.get_name())[0].get_label()
  # print type(na)
  na=na.get_name()
  # print "na="+na+" label="+g.get_node(na)[0].get_label()
  while e_out.has_key(na):
    # print "na="+na+" label="+g.get_node(na)[0].get_label()
    na=(e_out[na][0]).get_destination()
  return na

def raw_formula(formula):
#        print "in raw_formula"+formula
        if re.match(r'\[.+\][\s]*[0-9]+',formula):
           m=re.search(r'\[(.+)\][\s]*[0-9]+[0-9a-z]*',formula)
#           print "====> "+formula+" ="+m.group(1)
           res=m.group(1)
        elif re.match(r'\(.+\)[\s]*[0-9]+[0-9a-z]*',formula):
           m=re.match(r'\((.+)\)[\s]*[0-9]+[0-9a-z]*',formula)
           res=m.group(1)
#           print "ACHOU descarte ="+m.group(1)
        elif re.match(r'([A-Za-z0-9]+|\(.+\))', formula):
           m=re.match(r'([A-Za-z0-9]+|\(.+\))', formula)
           res=m.group(1)
        else:
           res="error"
#        print "OUT raw_formula"+res
        return res


def gera_grafo_ja_visitado(hg,w,i,v,k,label_descarte):
   global seqnode
#   print str(seqnode)+"vai gerar grafo_ja_visitado"+"w= "+w+"i= "+str(i)+"v= "+v+"k="+str(k)
##   print hg[0]
#   hg[0].add((k,v))
   novo_w=node_id_hid(str(seqnode)+"=[X"+str(i)+v+"]"+str(label_descarte))
   hg[1].add_node(novo_w)
   seqnode=seqnode+1
   nova_imp_w=node_id_hid(str(seqnode)+"=(X"+str(i)+vertex_name(v)+" imp "+"(X"+str(k)+v+" imp q))")
   hg[1].add_node(nova_imp_w)
   seqnode=seqnode+1
   w_negado=node_id_hid(str(seqnode)+"=(X"+str(k)+v+" imp q)")
   hg[1].add_node(w_negado)
   hg[1].add_edge(Deduction_Edge(novo_w,w_negado))
   hg[1].add_edge(Deduction_Edge(nova_imp_w,w_negado))
   seqnode=seqnode+1
   hg[1].root=w_negado
   seqnode=seqnode+1
   return hg

def gera_grafo_proibido(hg,w,v,k,label_descarte):
   global seqnode
#   print str(seqnode)+"vai gerar grafo_proibido"+"w= "+w+"v= "+v+"k="+str(k)+ "  hg[0]="
#   print hg[0]
#   hg[0].add((k,v))
#   print hg[0]
   novo_w=node_id_hid(str(seqnode)+"=[X"+str(k-1)+w+"]"+str(label_descarte))
   hg[1].add_node(novo_w)
#   novo_w=node_id_hid(str(seqnode)+"=X"+str(k-1)+vertex_name(w))
#   hg[1].add_node(novo_w)
   seqnode=seqnode+1
   nova_imp_w=node_id_hid(str(seqnode)+"=(X"+str(k-1)+vertex_name(w)+" imp "+"(X"+str(k)+v+" imp q))" )
   hg[1].add_node(nova_imp_w)
   seqnode=seqnode+1
   w_negado=node_id_hid(str(seqnode)+"=(X"+str(k)+v+" imp q)")
   hg[1].add_node(w_negado)
   hg[1].add_edge(Deduction_Edge(novo_w,w_negado))
   hg[1].add_edge(Deduction_Edge(nova_imp_w,w_negado))
#   print hg[1]
   hg[1].root=w_negado
   seqnode=seqnode+1
   return hg

def update_ref(est, ent, t):
   # print "atualiza a entrada ent=(k-1,w) com a adicao da tupla t=((k,v), grf)"
   # print "DENTRO de UPDATE_REF: Estrutura"
   # print est
   # print ent
   data=est.get(ent)
   data.append(t)
   est[ent]=data
   return est

def constroi_grafo_disjuntivo(hg,nivel,no,lista_provas):
#   print "construindo grafo disjuntivo nivel="+str(nivel)+"no="+no
   global seqnode
#   k=1
#   while lista_provas[k][0]<>(nivel,no):
#     k=k+1
   # n_descarte=get_k(no,hg[0])
   # no_prova_pleft=node_id_hid(str(seqnode)+"=[X"+str(nivel)+no+"]"+str(n_descarte))
   # hg[1].add_node(no_prova_pleft)
   # seqnode=seqnode+1
   # no_prova_pright=node_id_hid(str(seqnode)+"=(X"+str(nivel)+no+") imp (X"+str(nivel+1)+no+" imp q)")
   # hg[1].add_node(no_prova_pright)
   # seqnode=seqnode+1
   # no_prova=node_id_hid(str(seqnode)+"=(X"+str(nivel+1)+no+" imp q)")
   # hg[1].add_node(no_prova)
   # hg[1].add_edge(pd.Edge(no_prova_pleft,no_prova))
   # hg[1].add_edge(pd.Edge(no_prova_pright,no_prova))
   # seqnode=seqnode+1
   disjunctive_formula="(ORX"+str(nivel+1)+" imp q)"
   labeled_disjunctive_formula_conclusion=node_id_hid(str(seqnode)+"="+disjunctive_formula)
   seqnode=seqnode+1
   hg[1].root=labeled_disjunctive_formula_conclusion
   for ((i1,v1),v) in lista_provas.items():
 #    print "k="+str(k)+" lista_provas[k]= "
 #    print "(i1, v1),v "+str(i1)+v1+" "+v
     hg[1].add_node(labeled_disjunctive_formula_conclusion)
     disjunctive_formula="(X"+str(i1)+v1+" imp q) imp ("+ disjunctive_formula+ ")"
     labeled_disjunctive_formula_premiss=node_id_hid(str(seqnode)+"="+disjunctive_formula)
     seqnode=seqnode+1
     hg[1].add_node(labeled_disjunctive_formula_premiss)
     hg[1].add_edge(Deduction_Edge(labeled_disjunctive_formula_premiss,labeled_disjunctive_formula_conclusion))
#     print v.get('label') + "LABEL"+"  "+ no
#     if igual(v1,no):
#         hg[1].add_edge(pd.Edge(no_prova, labeled_disjunctive_formula_conclusion))
#     else:
     v_prova=v
     hg[1].add_edge(Deduction_Edge(v_prova, labeled_disjunctive_formula_conclusion))
     labeled_disjunctive_formula_conclusion=labeled_disjunctive_formula_premiss
   # print "grafo retornado="
   # print hg[1].to_string()
   # print "ROOT="
   # print hg[1].root
   left_premiss_disjunctive_formula="ORX"+str(nivel+1)
   labeled_left_premiss_disjunctive_formula=node_id_hid(str(seqnode)+"="+left_premiss_disjunctive_formula)
   hg[1].add_node(labeled_left_premiss_disjunctive_formula)
   seqnode=seqnode+1
   absurdity_conclusion="q"
   labeled_absurdity_conclusion=node_id_hid(str(seqnode)+"="+absurdity_conclusion)
   hg[1].add_node(labeled_absurdity_conclusion)
   hg[1].add_edge(Deduction_Edge(labeled_left_premiss_disjunctive_formula,labeled_absurdity_conclusion))
   hg[1].add_edge(Deduction_Edge(hg[1].root,labeled_absurdity_conclusion))
   hg[1].root=labeled_absurdity_conclusion
   seqnode=seqnode+1
##   print "GRAFO DISJUNTIVO RETORNADO"
##   print hg[1].to_string()
   return hg



def destroi_visitados_ref_nivel(hg,k,vw,n_descarte):
#   print "destruindo tentativas de visita a partir do no="+vw+"no nível="+str(k)
#   print hg[0]
   R=(hg[0]-set([((k,vw),n_descarte)]),hg[1])
   hg=(R,hg[1])
#   print "depois de removido (k,vw)"
#   print R[0]
   return R



#g=pd.Graph()

#g.add_node(pd.Node("v1"))
#g.add_node(pd.Node("v2"))

#g.add_edge(pd.Edge("v2","v1"))

#sgraph=pd.graph_from_dot_data(g.to_string())

# sgraph.write_pdf('img/testepdf')

# sgraph.write_svg('img/testesvg')

def add_nodes(graph, nodes):
    for n in nodes:
        graph.add_node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        graph.add_edge(pd.Edge(e[0],e[1]))
    return graph

def prepare_to_identify(n,g):
  if not e_in_A.has_key(n.get_name()):
#   print e_in.has_key(n.get_name())
   if  e_in.has_key(n.get_name()):
    for e1 in e_in[n.get_name()]:
        p=e1.get_source()
        p_node=g.get_node(p)[0]
        for e2 in e_out[n.get_name()]:
            v=e2.get_destination()
            v_node=g.get_node(v)[0]
            g.add_edge(Ancestor_Edge(v_node,p_node))
  elif not e_out_A.has_key(n.get_name()):
    print "PREPARE-TO-IDENTIFY: Caso que no= "+n.get_label()+" tem e_out_A vazio, mas e_in_A diferente de vazio"
    if  e_in.has_key(n.get_name()):
     deletion_list=[]
     for e in e_in_A[n.get_name()]:
       source_A=e.get_source()
       n_source_A=g.get_node(source_A)[0]
       for e_p in e_in[n.get_name()]:
           p_n=e_p.get_source()
           p_n_node=g.get_node(p_n)[0]
           g.add_edge(Ancestor_Edge(n_source_A,p_n_node))
       deletion_list.append(e)
     for e in deletion_list:
       e_out_A[e.get_source()].remove(e)
       e_in_A[e.get_destination()].remove(e)
       g.del_edge(e.get_source(),e.get_destination())
  else:
     print "PREPARE-To-IDENTIFY: no= "+n.get_label()+" tem out_A diferente de vazio"

def identify(n,v,g):
    global discharged_occurrences
    global conclusions
    global e_out_A
    global e_in_A
# storing the label of v before its deletion in the algorithm below
# the label of v will indicate whether it has discharging edges that must be attached to n
# besides this, the label of n has to incorporate the number discharged
    label_of_v=v.get_label()
    print "vai identificar n="+str(n.get_label())+" e v="+str(v.get_label())
    print "vai identificar n="+str(n.get_name())+" e v="+str(v.get_name())
    delete_from_sources=[]
    delete_from_targets=[]
    print "e_in_A.has_key(v.get_name())"
    print e_in_A.has_key(v.get_name())
    if not e_in_A.has_key(v.get_name()):
     if e_in.has_key(v.get_name()):
      for e1 in e_in[v.get_name()]:
        print "name = "+v.get_name()
        print e1
        p=e1.get_source()
        print p
        p_node=g.get_node(p)[0]
#        print "name e1 p ="+p_node.get_label()+" e "+"v = "+v.get_label()
#    Só adiciona aresta de dedução se não houver já uma aresta de dedução entre p_node e p
        if not Double_Deduction_Edge(p_node,n):
          g.add_edge(Deduction_Edge(p_node,n))
        delete_from_sources.append(e1)
#        print "LISTA DE EDGES SAINDO DE "+v.get_label()+v.get_name()
#        print e_out[v.get_name()]
        for e2 in e_out[v.get_name()]:
            v1=e2.get_destination()
            v_node=g.get_node(v1)[0]
            g.add_edge(Ancestor_Edge(v_node,p_node))
            if not e2 in delete_from_targets:
               delete_from_targets.append(e2)
      for e2 in e_out[v.get_name()]:
#            print e2
            v1=e2.get_destination()
#            print v1
            v_node=g.get_node(v1)[0]
#            print "imrpimindo n e v_node "
#            print n
#            print v_node
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_name()+" PARA "+v_node.get_name()
            if not Double_Deduction_Edge(n,v_node):
              g.add_edge(Deduction_Edge(n,v_node))
#      print "delete_from_targets"
#      print delete_from_targets
      for e in delete_from_sources:
          e_out[e.get_source()].remove(e)
#          print "VAI DELETAR "+e.get_source()+" PARA "+e.get_destination()
          g.del_edge(e.get_source(),e.get_destination())
      for e in delete_from_targets:
#          print "e_in[e.get_destination()]"
#          print e_in[e.get_destination()]
          e_in[e.get_destination()].remove(e)
#          print "VAI DELETAR "+e.get_source()+" PARA "+e.get_destination()
          g.del_edge(e.get_source(),e.get_destination())
      g.del_node(v.get_name())
     else:
      delete_from_targets=[]
      for e2 in e_out[v.get_name()]:
#        print e2
        v1=e2.get_destination()
        v_node=g.get_node(v1)[0]
#        print "VAI ADICONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
        if not Double_Deduction_Edge(n,v_node):
          g.add_edge(Deduction_Edge(n,v_node))
        if not e2 in delete_from_targets:
            delete_from_targets.append(e2)
      for e in delete_from_targets:
#          print "e_in[e.get_destination()]"
#          print e_in[e.get_destination()]
          e_in[e.get_destination()].remove(e)
          g.del_edge(e.get_source(),e.get_destination())
      g.del_node(v.get_name())
    elif not e_out_A.has_key(v.get_name()):
     print "e_out_A.has_key(v.get_name())= "+str(e_out_A.has_key(v.get_name()))
     print "IDENTIFY: elif not e_out_A.has_key(v.get_name()) Caso com no= "+v.get_label()+" com lista de ancestor-saindo vazia, mas ancestor-chegando (e_in_A) nao vazia"
     print "IDENTIFY: e_in_A= "
     print e_in_A[v.get_name()]
     if e_in.has_key(v.get_name()):
      for e1 in e_in[v.get_name()]:
#        print "name = "+v.get_name()
        p=e1.get_source()
        p_node=g.get_node(p)[0]
        print "IDENTIFY: e_in.has_key(v.get_name()) name e1 p ="+p_node.get_label()+" e "+"v = "+v.get_label()+" n="+n.get_label()+" Double_Deduction_Edge= "
        print Double_Deduction_Edge(p_node,n)
        if not Double_Deduction_Edge(p_node,n):
          print "VAI ADICIONAR ARESTA DE "+p_node.get_label()+" para "+n.get_label()
          g.add_edge(Deduction_Edge(p_node,n))
        delete_from_sources.append(e1)
#        print "LISTA DE EDGES SAINDO DE "+v.get_label()+v.get_name()
#        print e_out[v.get_name()]
        # for e2 in e_out[v.get_name()]:
        #     v1=e2.get_destination()
        #     v_node=g.get_node(v1)[0]
        #     g.add_edge(Ancestor_Edge(v_node,p_node))
        #     if not e2 in delete_from_targets:
        #        delete_from_targets.append(e2)
      delete_from_targets=[]
      for e2 in e_out[v.get_name()]:
#            print e2
            v1=e2.get_destination()
#            print v1
            v_node=g.get_node(v1)[0]
#            print "imrpimindo n e v_node "
#            print n
#            print v_node
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_name()+" PARA "+v_node.get_name()
#            if not linked(g,n.get_name(),v_node.get_name()):
            if not Double_Deduction_Edge(n,v_node):
                g.add_edge(Deduction_Edge(n,v_node))
            if not e2 in delete_from_targets:
               delete_from_targets.append(e2)
      delete_edge_ancestor=[]
      for e3 in e_in_A[v.get_name()]:
            r1=e3.get_source()
            r_node=g.get_node(r1)[0]
            for e4 in e_in[v.get_name()]:
              r2=e4.get_source()
              p_node=g.get_node(r2)[0]
              g.add_edge(Ancestor_Edge(r_node,p_node))
            delete_edge_ancestor.append(e3)
      print "delete in_edge_Ancestor"
      for e3 in delete_edge_ancestor:
          e_in_A[v.get_name()].remove(e3)
          g.del_edge(e3.get_source(), e3.get_destination())
 #     print "delete_from_targets"
 #     print delete_from_targets
      for e in delete_from_sources:
          e_out[e.get_source()].remove(e)
 #         print "VAI DELETAR "+e.get_source()+" PARA "+e.get_destination()
          g.del_edge(e.get_source(),e.get_destination())
      for e in delete_from_targets:
 #         print "e_in[e.get_destination()]"
 #         print e_in[e.get_destination()]
          e_in[e.get_destination()].remove(e)
 #         print "VAI DELETER "+e.get_source()+" PARA "+e.get_destination()
          g.del_edge(e.get_source(),e.get_destination())
      g.del_node(v.get_name())
     else:
      delete_edge_ancestor=[]
      for e3 in e_in_A[v.get_name()]:
            r1=e3.get_source()
            r_node=g.get_node(r1)[0]
            g.add_edge(Ancestor_Edge(r_node,n))
            delete_edge_ancestor.append(e3)
 #     print "delete in_edge_Ancestor"
      for e3 in delete_edge_ancestor:
          e_in_A[v.get_name()].remove(e3)
          g.del_edge(e3.get_source(), e3.get_destination())
      delete_from_targets=[]
      for e2 in e_out[v.get_name()]:
 #       print e2
        v1=e2.get_destination()
        v_node=g.get_node(v1)[0]
 #       print "VAI ADICIONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
        if not linked(g,n.get_name(),v_node.get_name()):
          if not Double_Deduction_Edge(n,v_node):
            g.add_edge(Deduction_Edge(n,v_node))
        if not e2 in delete_from_targets:
            delete_from_targets.append(e2)
      for e in delete_from_targets:
 #         print "e_in[e.get_destination()]"
 #         print e_in[e.get_destination()]
          e_in[e.get_destination()].remove(e)
          g.del_edge(e.get_source(),e.get_destination())
      g.del_node(v.get_name())
    else:
      print "IDENTIFY: no= "+v.get_label()+" tem out_A diferente de vazio, portanto um grafo sintaticamente errado"
# this part takes care of the discharged edges that must be attached to n as well as the number discharged that has
# to be in the label of n
# Testing if the node v is the discharged formula  of a discharging rule (imply-intro)
    if re.match(r'\[.+\][0-9]+',label_of_v):
       m=re.search(r'\[.+\]([0-9][0-9a-z]*)',label_of_v)
       print "v ====> "+label_of_v+" ="+m.group(1)
       if re.match(r'\[.+\][0-9]+',n.get_label()):
         m1=re.search(r'\[.+\]([0-9][0-9a-z]*)',n.get_label())
         print "n ======> "+n.get_label()+" ="+m1.group(1)
         if m.group(1)==m1.group(1):
            print "SAO IGUAIS"
# We do not need to add a new edge. Both edges got to the same intro-imply rule instance application (conclusion[m.group(1)])
# The only obligation is to delete the v node.
         else:
# Since n and v are discharged by different instance of intro-imply, after collapsing n and v in n we have to add the new edge
# from n to the conclusion that was obtained with the instance rule app that discharged v (conclusions[m.group(1)]) and
#  change the labels of n accordingly
            if conclusions[m.group(1)]<>conclusions[m1.group(1)]:
               g.add_edge(pd.Edge(n,conclusions[m.group(1)],color="red"))
            n.set_label(n.get_label()+str(m.group(1)))
# Deleting the node v.  I DO NOT KNOW WHETHER THE FORMER EDGE FROM v TO conclusions[m.group(1)] is deleted automaticaly when v is
         print "APAGANDO ARESTA "+v.get_label()+"==> "+ conclusions[m.group(1)].get_label()
         g.del_edge(v,conclusions[m.group(1)])
         g.del_node(v.get_name())
    #    conclusions[m.group(1)]=
    #    for l in discharged_occurrences[m.group(1)]:
    #       print l
    #       print "label de l="+str(l.get_label())
    #       g.add_edge(pd.Edge(l,n,color="red"))
    #    n.set_label(n.get_label()+str(m.group(1)))
    else:
       if re.match(r'\(.+\)\s*[0-9]+',label_of_v):
         m=re.search(r'\(.+\)\s*([0-9][0-9a-z]*)',label_of_v)
         print "COLLAPSO DE REGRA DE INTRODUCAO v ====> "+label_of_v+" ="+m.group(1)
         if re.match(r'\(.+\)\s*[0-9]+',n.get_label()):
           m1=re.search(r'\(.+\)\s*([0-9][0-9a-z]*)',n.get_label())
           print "COM REGRA DE INTRODUCAO n ====> "+ m1.group(1)
#          print "n ======>  ="+ m1.group(1)
           if m.group(1)==m1.group(1):
              print "SAO IGUAIS, SERIA UM ERRO ?"
# We do not need to add a new edge. Both edges got to the same intro-imply rule instance application (conclusion[m.group(1))
# The only obligation is to delete the v node.
           else:
# Since n and v are discharged by different instance of intro-imply, after collapsing n and v in n we have to add the new edge
# from n to the conclusion that was obtained with the instance rule app that discharged v (conclusions[m.group(1)]) and
#  change the labels of n accordingly
              for node_dhg_by_v in discharged_occurrences[m.group(1)]:
                  g.add_edge(pd.Edge(node_dhg_by_v,n,color="red"))
                  g.del_edge(node_dhg_by_v,v)
              n.set_label(n.get_label()+" "+str(m.group(1)))
              print "collapsing_nodes: atualizando conclusions: "+m1.group(1)+"--> "+n.get_label()
              print "collapsing_nodes: atualizando conclusions: "+m.group(1)+"--> "+n.get_label()
              conclusions[m.group(1)]=n
              conclusions[m1.group(1)]=n
              g.del_node(v.get_name())
# FALTARIA ATUALIZAR A ESTRUTURA discharged_occurrence, mas precisa avaliar a necessidade DISSO
         else:
           print "COM REGRA DE ELIMINACAO n ++++++> "+ m1.group(1)
           n.set_color("purple")
# Deleting the node v.  I DO NOT KNOW WHETHER THE FORMER EDGE FROM v TO conclusions[m.group(1)] is deleted automaticaly when v is
         # print "APAGANDO ARESTA "+v.get_label()+"==> "+ conclusions[m.group(1)].get_label()
         # g.del_edge(v,conclusions[m.group(1)])
         # g.del_node(v.get_name())
    return g


def collapsing_nodes(i,f,nodes_repeated,g):
    print "Collapsing Equally Labeled Nodes in the list =>"
    print nodes_repeated
    for n in nodes_repeated:
       print "labels = "+n.get_label()
       for e1 in e_out[n.get_name()]:
          p=e1.get_destination()
          p_node=g.get_node(p)[0]
       if (p_node.get_style() != "filled"):
           n.set_color("gray"+str(3*i+50))
           n.set_style("filled")
       elif (len(e_in[p_node.get_name()])==1): 
           n.set_color(n.get_color())
           n.set_style(n.get_style())
       else:
           
           print(" Aqui vai o caso mais complicado")

           
       print " Um filho de "+n.get_label()+" é "+p_node.get_label()
#       n.set_color( "gray52")
#       n.set_style("filled")
#      print "COR definida = " + n.get_color()
#   Gravando resultado parcial
    intermediograph=pd.graph_from_dot_data(g.to_string())
    print "gravando dot file em collapsing_nodes ANTES da compressao horizontal, nos a serem colapsados em estao em azul"
    intermediograph.write("img/"+g.get_name()+"IntermediodeNivANTES"+str(i)+"For-"+f+".dot")
    # ALTERADO PARA PINTAR SOMENTE OS REPETIDOS
#     node_keep=nodes_repeated[0]
#     prepare_to_identify(node_keep,g)
#     del nodes_repeated[0]
#     print "nos node_repeated = "
#     print nodes_repeated
#     for n in nodes_repeated:
#        print "n = "+n.get_label()+" name= "+n.get_name()
#        g=identify(node_keep,n,g)
# #       print "collapsing_nodes: Gerando dot string para gravacao"
#     node_keep.set_color( "red" )
#     intermediograph=pd.graph_from_dot_data(g.to_string())
#     print "gravando dot file em collapsing_nodes ANTES da compressao horizontal, nos a serem colapsados em estao em azul"
#     intermediograph.write("img/"+g.get_name()+"IntermediodeNiv"+str(i)+"ForCollapsed-"+f+".dot")
#     node_keep.set_color( "green" )
    # FIM DA ALTERACAO
    return g



def constroi_ramo(est,k, grafo, visitados_hips, w,descarte_counter):
# Build and return the derivation of the absurdity (q) that a partial cycle having the (k-1)th visited node as w and descarte_counter and
# is the label that discharges the next step assumption, namely, in the k-th visited node in the whole derivation yet to be constructed
  global seqnode
  hg=(visitados_hips, grafo)
#  print "\rNIVEL"+" = "+str(k),
#  sys.stdout.write("\rNIVEL= %i" % str(k))
#  sys.stdout.flush()
  vw=vertex_name(w)
  novo_est={}
  this_context_descarte_counter=descarte_counter-1
#  descarte_counter=label_descarte
  if k < (Max+1):
#     print "visitados_hips"
#     print visitados_hips
     visitados=set([])
     for ((i,v),n) in visitados_hips:
        visitados.add(v)
#     visitados={ v for v in nos for j in range(1,k) if (j,v) in visitados_hips}
##     print "VISITADOS"
##     print visitados
     proibidos={v for v in nos if not linked(g,vw,v) and not linked(g,v,vw)}
##     print "PROIBIDOS"
##     print proibidos
     for v in nos:
#         print "atuando em v= "+v
         if v in visitados:
            i=get_k(v,visitados_hips)
            n_descarte=get_descarte(v,visitados_hips)
            hg=gera_grafo_ja_visitado(hg,w,i,v,k,n_descarte)
#            print "DENTRO DO CONSTROI RAMO:visitados"
            # print hg[0]
            # print hg[1].to_string()
            # print "ROOT"
            # print hg[1].root.to_string()
#            print type(est[(k-1,vw)])
            est[(k,v)]=hg[1].root
#            est=update_ref(est, (k-1,vw), ((k,v), hg[1].root))
            # print "ESTRUTURA"
            # print est
         elif v in proibidos:
              hg=gera_grafo_proibido(hg,w,v,k,this_context_descarte_counter)
#              label_descarte=label_descarte+1
#              print "DENTRO DO CONSTROI RAMO:proibidos"
              # print hg[0]
              # print hg[1].to_string()
              # print "ROOT"
              # print hg[1].root.to_string()
              est[(k,v)]=hg[1].root
#              est=update_ref(est, (k-1,vw), ((k,v), hg[1].root))
              # print "ESTRUTURA"
              # print est
         else:
#              print "CHAMANDO CONSTROI_RAMO DE DENTRO DELE MESMO:Sem Restricoes"
              # print "Visitando "+v+" no passo k= "+str(k)
              # print hg[0]
              hg[0].add(((k,v),descarte_counter))
              # print "ESTADOS"
              # print est
              novo_est={}
              (hg,novo_est,descarte_counter)=constroi_ramo(novo_est,k+1,hg[1],hg[0] ,v,descarte_counter+1)
#              print "descarte_counter="+str(descarte_counter)
#              label_descarte=label_descarte+1
              # print "depois de constroi ramo novo_est= em k="+str(k)+"v="+v
              # print novo_est
#              print novo_est.get((k,v))
              est[(k,v)]=novo_est[(k,v)]
#              print "est antes do grafo disjuntivo"
#              print "k="+str(k)+" v="+ v
#              print est
#              z=raw_input("est depois de atualizado com novo_est")
#     print "construindo grafo disjuntivo"
#     print "a partir do par ="+str(k-1)+" "+vw+"aqui"
#     print est
     hg=constroi_grafo_disjuntivo(hg,k-1,vw,est)
     imply_intro_conclusion_com_descarte=node_id_hid(str(seqnode)+"=(X"+str(k-1)+vw+" imp q)"+" "+str(this_context_descarte_counter))
     seqnode=seqnode+1
     hg[1].add_node(imply_intro_conclusion_com_descarte)
     hg[1].add_edge(Deduction_Edge(hg[1].root,imply_intro_conclusion_com_descarte))
     hg[1].root=imply_intro_conclusion_com_descarte
     hg=destroi_visitados_ref_nivel(hg,k-1,vw,this_context_descarte_counter)
     est[(k-1,vw)]=hg[1].root
#     print "ESTRUTURA APOS GRAFO DISJUNTIVO"
#     print est
#     print "hg[0] apos construir grafo disjuntivo"
#     print hg[0]
#     print "hg[1] apos construir grafo disjuntivo"
#     print hg[1].to_string()
#     z=raw_input("vai retornar depois de vir de destroi_visitados")
#     print hg[0]
     return (hg,est,descarte_counter)
  else:
#    Verifica se e vw no passo 3 alcanca ini (primeiro) no passo Max+1
#     print "chegou no passo Max+1"
#     print "k="+str(k)+" vw="+vw
#     print "visitados"
#     print hg[0]
#     z=raw_input("pausa ")
     ini=str(0)
     for v in nos:
##         print "par de="+str(type(1))+str(type(v))
         for j in range(0,descarte_counter+1):
          if ((1,v),j) in hg[0]:
            ini=v
            label=j
#     print "ini="+ini
     if not linked(g,vw, ini):
        no_prova_pleft=node_id_hid(str(seqnode)+"=[X"+str(1)+ini+"]"+str(label))
        label_descarte_local=str(descarte_counter)+"a"
        hg[1].add_node(no_prova_pleft)
        seqnode=seqnode+1
        no_prova_pright=node_id_hid(str(seqnode)+"=(X"+str(1)+ini+" imp (X"+str(Max+1)+ini+"))")
        hg[1].add_node(no_prova_pright)
        seqnode=seqnode+1
        no_prova_l=node_id_hid(str(seqnode)+"=X"+str(Max+1)+ini)
        hg[1].add_node(no_prova_l)
        hg[1].add_edge(Deduction_Edge(no_prova_pleft,no_prova_l))
        hg[1].add_edge(Deduction_Edge(no_prova_pright,no_prova_l))
        seqnode=seqnode+1
        no_provaright_pleft=node_id_hid(str(seqnode)+"=[X"+str(Max)+vw+"]"+label_descarte_local)
        seqnode=seqnode+1
        no_provaright_pright=node_id_hid(str(seqnode)+"=(X"+str(Max)+vw+" imp (X"+str(Max+1)+ini+" imp q))")
        seqnode=seqnode+1
        no_provaright=node_id_hid(str(seqnode)+"=(X"+str(Max+1)+ini+" imp q)")
        seqnode=seqnode+1
        no_absurdity=node_id_hid(str(seqnode)+"=q")
        seqnode=seqnode+1
        no_conclusao=node_id_hid(str(seqnode)+"=(X"+str(Max)+vw+" imp q)"+label_descarte_local)
        seqnode=seqnode+1
        hg[1].add_node(no_absurdity)
        hg[1].add_node(no_conclusao)
        hg[1].add_node(no_provaright)
        hg[1].add_node(no_provaright_pleft)
        hg[1].add_node(no_provaright_pright)
        hg[1].add_edge(Deduction_Edge(no_provaright_pleft,no_provaright))
        hg[1].add_edge(Deduction_Edge(no_provaright_pright,no_provaright))
        hg[1].add_edge(Deduction_Edge(no_prova_l,no_absurdity))
        hg[1].add_edge(Deduction_Edge(no_provaright,no_absurdity))
        hg[1].add_edge(Deduction_Edge(no_absurdity,no_conclusao))
        hg[1].root=no_conclusao
        hg=destroi_visitados_ref_nivel(hg,k-1,vw,descarte_counter)
        est[(Max,vw)]=hg[1].root
##        print "gerou o X1v1  X1v1 --> (X4v_vw --> q) / X4v_vw --> q"
##        print hg[0]
        # text_file = open("img/testestring", "w")
        # text_file.write(hg[1].to_string())
        # text_file.close()
        return (hg,est,descarte_counter)
     else:
#        print "Achou um ciclo Hamiltoniano"
        return pd.Graph()
#     z=raw_input("tratou o caso que representa o ciclo")


 #     if len(proximos) > 0:
 #        print "SEQNODEPAI"+" "+str(seqnodepai)
 #        for n in proximos:
 #            grafo.add_node(pd.Node(str(seqnode)+"=X"+str(k)+n))
 #            grafo.add_edge(pd.Edge(str(seqnodepai)+"=X"+str(k-1)+vw,str(seqnode)+"=X"+str(k)+n))
 #            print grafo.to_string()
 #            seqnode=seqnode+1
 #            visitados.add((k,n))
 #            grafo=constroi_ramo(seqnode,k+1, grafo, visitados,str(seqnode-1)+"=X"+str(k)+n)
 #            visitados=visitados.difference(set((k,n)))
 # #           seqnode=seqnode-1
 #        return grafo
 #     else:
 #        print("terminou")
 #        return grafo
 #  else:
 #     return grafo



def inicia(grafoteste):
    global seqnode
    global Max
    descarte_counter=1
    est={}
    seqnode=1
    vis=set([])
    hg=(vis,grafoteste)
    for v in nos:
       novo_est={}
       hg[0].add(((1,v),descarte_counter))
#       n_descarte=n_descarte+1
#       hg=(vis,grafoteste)
##       print "rotulo do DESCARTE="+str(n_descarte)
       (hg,novo_est,descarte_counter)=constroi_ramo(novo_est,2,hg[1], hg[0],v,descarte_counter+1)
##       print "construindo grafo disjuntivo primeiro nível"
##       print "a partir do par ="+str(1)+" "+v+"aqui"
##       print novo_est
#       est[(1,v)]=novo_est[(1,v)]
       # imply_intro_conclusion_com_descarte=node_id_hid(str(seqnode)+"=X"+str(1)+v+" imp q"+" "+str(1))
       # seqnode=seqnode+1
       # hg[1].add_node(imply_intro_conclusion_com_descarte)
       # hg[1].add_edge(pd.Edge(hg[1].root,imply_intro_conclusion_com_descarte))
       # hg[1].root=imply_intro_conclusion_com_descarte
       hg=destroi_visitados_ref_nivel(hg,1,v,descarte_counter)
       est[(1,v)]=hg[1].root
       descarte_counter=descarte_counter+1
    # hg=constroi_grafo_disjuntivo(hg,1,v,est)
##    print "ESTRUTURA APOS (1,v1),(1,v2) e (1,v3)"
##    print est
# vai contruir o ultimo grafo disjuntivo
    hg=constroi_grafo_disjuntivo(hg,0,"basis",est)
#    print "Numero de Descartes = "+ str(descarte_counter)
##    print "hg[0] apos construir grafo disjuntivo"
##    print hg[0]
##    print "hg[1] apos construir grafo disjuntivo"
##    print hg[1].to_string()
#    z=raw_input("vai retornar depois de vir de destroi_visitados")
#       return (hg,est)
#       est[1,v]=novo_est[1,v]
#    n_descarte=n_descarte+1
#       return hg[1]
#       return "FIM"



# A partir daqui monta-se os ramos que se conectam com v
#    grafo=add_nodes(grafo,

# sequencia de comandos para testar o constroi_ramo

# grafoteste=pd.Graph()

#grafoteste.add_node(pd.Node("X1v1"+"-"+str(seq_node)))


def final(gin):
#    print "quantidade de nós no grafo de prova="+str(seqnode)
#    print "entrou no final, vai gerar to_string"
    garf=pd.graph_from_dot_data(gin.to_string())
#    print "Gerou to_string(), vai gravar o dot"
    garf.write("img/"+garf.get_name()+".dot")

    # garf=pd.graph_from_dot_data(gin.to_string())
    # print "gerou to_string(), vai gravar no arquivo"
    # garf.write_pdf("img/"+garf.get_name()+".pdf")
    # print "generated the graph from the dot"
    # print "gravou"
#    table_gin=tab_coloring(gin)
#    writetable(table_gin)
#    graf.write(filename)
#    gin_savecopy=pd.graph_from_dot_file(filename)
#    gin_savecopy.write_pdf(filename+"saved.pdf")
#    gincor=coloring(gin,table_gin)
#    gincor.set_name(gin.get_name()+"colorido")
#    print "Vai gerar o to_string do colorido"
#    sgraph=pd.graph_from_dot_data(gincor.to_string())
#    dotname="img/"+gincor.get_name()
#    print "Vai gravar o dot do colorido"
#    sgraph.write(dotname+".dot")
#    print "Vai gravar os  arquivos pdfs"
#    print "pdf do original, gravando"
#    garf.write_pdf("img/"+gincor.get_name()+".pdf")
#    print "pdf do colorido, gravando"
#    sgraph.write_pdf(dotname+".pdf")



def writetable(t):
    with open('img/tabelaLabels.csv', 'wb') as csv_file:
       writer=csv.writer(csv_file)
       for key, value in t.items():
          writer.writerow([key, value])

def write_vetor_oc(t):
# building the dict of all key-formulas in t
    formulas=set([])
    i=0
    vector_oc_by_level={}
    for n,l in t.items():
        for f,n_oc in l.items():
            formulas.add(raw_formula(f))
#    print len(formulas)
    header=['formulas']
    for i in range(0,len(t)):
        header.append(i)
    for f in formulas:
        vector_oc_by_level[f]=[f]
        for n in range(0,len(t)):
          if t[n].has_key(f):
            vector_oc_by_level[f].append(t[n][f])
          else:
            vector_oc_by_level[f].append(0)
        with open('img/vetorocorrencias.csv', 'wb') as csv_file:
          writer=csv.writer(csv_file)
          writer.writerow(header)
          for f,formulas_oc in vector_oc_by_level.items():
              writer.writerow(formulas_oc)



# FIm de codigo


visitados=set()

global seqnode

discharged_occurrences={}
conclusions={}


# relativo a eficiencia da versao linked
# associa vertices as arestas incidented que chegam nele
e_in={}
# associa vertices as arestas incidentes que saem dele
e_out={}
# associa vertices as arestas ancestrais (l_A no paper) que saem de cada um deles
e_in_A={}
# associa vertices as arestas ancestrais (l_A no paper) que chegam em  cada um deles
e_out_A={}






seqnode=1

# supondo X[1,v1] como inicio.

visitados.add("v1")

# 3 vezes o Fragmento de Tutte (grafico cubico de 46 nós)

Max=46
nos={"v"+str(i) for i in range(1,Max+1)}
# set(['v1', 'v2', 'v3', 'v4', 'v5'])

list_nodes=[]
for i in range(1,Max+1):
    list_nodes=list_nodes+[pd.Node("v"+str(i))]

# Especificacao do Grafo

# # # # # Grafo 
g=pd.Graph()
g=add_nodes(g,list_nodes)
g=add_edges(g, [('v1', 'v2'),('v1','v17'),('v1','v32')])
g=add_edges(g, [('v2', 'v3'), ('v2', 'v4')])
g=add_edges(g, [('v3','v5'),('v3', 'v6')])
g=add_edges(g, [('v4', 'v5'), ('v4', 'v10')])
g=add_edges(g, [('v5', 'v8'), ('v5', 'v4')])
g=add_edges(g, [('v6', 'v7'),('v6','v11')])
g=add_edges(g, [('v7', 'v8'),('v7','v12')])
g=add_edges(g, [('v8', 'v7'),('v8','v9')])
g=add_edges(g, [('v9', 'v13'),('v9','v10')])             
g=add_edges(g, [('v10', 'v9'),('v10','v15')])
g=add_edges(g, [('v11', 'v12'),('v11','v16')])
g=add_edges(g, [('v12', 'v7'),('v12','v13')])
g=add_edges(g, [('v13', 'v9'),('v13','v14')])
g=add_edges(g, [('v14', 'v15'),('v14','v16')])
g=add_edges(g, [('v15', 'v10'),('v15','v14')])
g=add_edges(g, [('v16', 'v11'),('v16','v14')])             
             
             # g=add_edges(g, [('v6', 'v8'), ('v6','v9')])
# g=add_edges(g, [('v7', 'v10'), ('v7','v9')])
# g=add_edges(g, [('v8', 'v10')])

# # Grafo G3
# g=pd.Graph()
# g=add_nodes(g,list_nodes)
# g=add_edges(g, [('v1', 'v2'), ('v1','v3')])

# Grafo G5
# g=pd.Graph()
# g=add_nodes(g, list_nodes)
# g=add_edges(g,[('v1','v2'),('v2','v3'),('v3','v1'),('v1','v4'), ('v2','v4'), ('v3','v4'), ('v4''v5')])

# # # # # Grafo tough
g=pd.Graph()
g=add_nodes(g,list_nodes)
g=add_edges(g, [('v1', 'v2'), ('v1','v4'),('v1','v7'),('v1','v3')])
g=add_edges(g, [('v2', 'v7'), ('v2', 'v6'),('v2','v3'),('v2','v1')])
g=add_edges(g, [('v3','v7'),('v3', 'v5')])
g=add_edges(g, [('v4', 'v7')])
g=add_edges(g, [('v6', 'v7')])
g=add_edges(g, [('v5', 'v7')])
# g=add_edges(g, [('v7', 'v10'), ('v7','v9')])
# g=add_edges(g, [('v8', 'v10')])



# MAIN ###############

# GrafoPetersenDescartes=pd.Graph()
# GrafoPetersenDescartes.set_name("GrafoPetersenDescartes")
# inicia(GrafoPetersenDescartes)
# GrafoPetersenDescartes=draw_discharging_edges(GrafoPetersenDescartes)
GrafoProva=pd.Graph()
GrafoProva.set_name("ArvoreProvaG3")
inicia(GrafoProva)

print("Grafo com "+str(len(GrafoProva.get_node_list()))+ "nós")

# print GrafoProva.to_string()
GrafoProva=draw_discharging_edges(GrafoProva)
garf=pd.graph_from_dot_data(GrafoProva.to_string())
garf.write("img/"+garf.get_name()+".dot")
# for i,l in discharged_occurrences.items():
#    print "descarte num= "+str(i)+" lista:"
#    for n in l:
#        print n.to_string()
# for i,n in conclusions.items():
#    print str(i)+" descartado em "+n.to_string()
#print GrafoPetersenDescartes.to_string()
# print "GERANDO O GRAFO COLORIDO e Gravando os dots"
# final(GrafoProva)

# juntando a geracao e a estatistica

graph_from_file=GrafoProva


print " TERMINOU A GERACAO. VERSAO NOVA"



#graph_from_file=pd.graph_from_dot_file("img/GrafoPetersenDescartes.dot")
#graph_from_file.write_pdf("img/copiaG3.pdf")
# Very inefficent for large proof-graphs. Must be used only in the case that the proof was not build by this
# program itself.
#(e_out,e_in)=associative_source_and_target_lists(graph_from_file)
# Display used during the deveopment phase
# for (n,l) in e_in.items():
#    print n+"e_in[n]="
#    for v in l:
#        print v.to_string()
root=find_root(graph_from_file)
print root
node_root=graph_from_file.get_node(root)
print node_root[0].get_label()
nr=node_root[0].get_name()
print "nr"+nr
nivel=0
node_formulas={}
node_formulas[nivel]=[nr]
while node_formulas[nivel]:
#   print node_formulas[nivel]
# for l in node_formulas[nivel]:
#   print l
   node_formulas[nivel+1]=[]
   for n in node_formulas[nivel]:
    if e_in.has_key(n):
     for e in e_in[n]:
 #      if e.get_source():
 #        z=raw_input("ENCONTROU e.get_source() vazio")
 #        print e
 #        print "FIM DO ENCONTROU"
 #      else:
         node_formulas[nivel+1].append(e.get_source())
#     print "DEPOIS"
#     print node_formulas[nivel+1]
#     print "Fez o n="+n
#   print "node_formulas="
#   print  { graph_from_file.get_node(n)[0].get_label() for n in node_formulas[nivel+1]}
#   print "Fez o NIVEL="+str(nivel+1)
   nivel=nivel+1
# calculando vetores de ocorrencias
v_oc={}
v_repeated_nodes={}
i=0
while i< len(node_formulas):
  v_repeated_nodes[i]={}
  v_oc[i]={}
  i=i+1
for (n,l) in node_formulas.items():
#  print "nivel="+str(n)
#  print "LISTA DE NOS="
#  print l
#  print "============FIM DE LISTA"
  for f in l:
   lista_nos_formula=graph_from_file.get_node(f)
#   print "lista_nos_formula==>"
#   print lista_nos_formula
   if lista_nos_formula <> []:
     node_formula_f=graph_from_file.get_node(f)[0]
     # print "lista de nos"
     # print node_formula_f
     formula_f=node_formula_f.get_label()
#     print "formula_f"+formula_f
     formula_f=raw_formula(formula_f)
     v_oc[n][formula_f]=0
     v_repeated_nodes[n][formula_f]=[]
  for f in l:
   lista_nos_formula=graph_from_file.get_node(f)
   if lista_nos_formula <> []:
     node_formula_f=graph_from_file.get_node(f)[0]
     formula_f=node_formula_f.get_label()
     formula_f=raw_formula(formula_f)
     v_oc[n][formula_f]=v_oc[n][formula_f]+1
     v_repeated_nodes[n][formula_f].append(node_formula_f)
maximo_oc=0
for niv in range(0,len(v_oc)):  
    for f_r in v_oc[niv]:
#        node_formula_f=graph_from_file.get_node(f)[0]
#        formula_f=node_formula_f.get_label()
#        formula_f=raw_formula(formula_f)
        print "ocorrencias de "+f_r+"no nivel "+str(niv)+" eh "+str(v_oc[niv][f_r])
        if (v_oc[niv][f_r]>maximo_oc):
            maximo_oc=v_oc[niv][f_r]
            niv_maximo=niv
            formula_maximo=f_r
print "o nivel "+str(niv_maximo)+" tem a formula "+formula_maximo+" que ocorre mais vezes ="+str(maximo_oc)
        
#          formula_f=graph_from_file.get_node(f)[0].get_label()
#      if v_oc[n][formula_f] > 1:
#         print "MAIS DE UMA OC = "+str(v_oc[n][formula_f])
#      print n
#      print l
#      print v_oc[n]
#write_vetor_oc(v_oc)
print "seqnode="+str(seqnode)
l_nodes=graph_from_file.get_node_list()
num_oc_formulas=len(l_nodes)
print "num_oc_formulas="+str(num_oc_formulas)
# #  Starting the horizontal collapsing
# print "COLLAPSING THE REPEATED FORMULAS"
# print "Gerando graph_from_dot_data ANTES-COMPRESSAO "
# sgraph=pd.graph_from_dot_data(graph_from_file.to_string())
# print "gravando dot file"

# sgraph.write("img/"+sgraph.get_name()+"ANTES.dot")
# print "GRAVOU"
# i=0
# while i < len(v_oc) and v_oc[i]:
#     repeated_formulas=[]
#     while not repeated_formulas and v_oc[i]:
#        i=i+1
# #       if not v_oc[i]:
#        print "nivel "+str(i)
#        print v_oc[i].keys()
#        for f in v_oc[i].keys():
# #            print "Formulas do nivel "+str(i)
# #            print v_oc[i]
# #            print f+"i= "+str(i)+"v_oc[i][f]= "+ str(v_oc[i][f])
#             if v_oc[i][f]>1:
#                 repeated_formulas.append(f)
#     print "REPEATED_FORMULAS =====> "
#     print repeated_formulas
#     print "=========="
#     for f in repeated_formulas:
#        print "nivel da formula que repete= "+str(i)
#        print "formula que repete= "+ f
#        print "vai collapsar "+f+" "+str(v_oc[i][f])+" vezes, no nivel "+str(i)
# #      ALTERACAO 29-05-2020
#        grafo_compressed=collapsing_nodes(i,f,v_repeated_nodes[i][f],graph_from_file)
#     print "Gerando graph_from_dot_data  DEPOIS-COMPRESSAO do nivel "+str(i)
#     sgraph=pd.graph_from_dot_data(graph_from_file.to_string())
#     print "gravando dot file"
#     sgraph.write("img/"+sgraph.get_name()+"DEPOISniv"+str(i)+".dot")
# #    i=i+1


# FIM DA ALTERACAO 29-05-2020

# Inicio da prova de que não há caminho hamiltoniano

# Iniciando o array de variavies proposicionais


# visitados_antes={ v for v in nos for j in range(1,k-1) if (j,v) in visitados}

# proibidos={"not "+v for v in nos if not linked(g,v,"v1") and not linked(g,"v1",v)}

# proibidos[2]={v for v in nos if linked(g,v,"v1") or linked(g,"v1",v)}
