#!/usr/local/bin/python
# coding: utf-8

import pydotplus as pd
import graphviz
import pyparsing
import csv
import re
import sets

global e_in
global e_out
global e_in_A
global e_out_A
# associa vertices as arestas ancestrais (l_A no paper) que saem de cada um deles
e_in_A={}
# associa vertices as arestas ancestrais (l_A no paper) que chegam em  cada um deles
e_out_A={}
global seqnode
seqnode=1
e_in={}
e_out={}

def raw_formula(formula):
#        print("in raw_formula"+formula+"tem tipo")
        if re.match(r'\"\[[A-Za-z0-9 ]+\]\s*[0-9]+\"',formula):
           m=re.search(r'\[([A-Za-z0-9 ]+)\]\s*[0-9]+',formula)
#           print("====> "+formula+" =")
           res=m.group(1)
        elif re.match(r'\"\[\(.+\)\]\s*[0-9]+\"',formula):
           m=re.search(r'\[(\(.+\))\]\s*[0-9]+',formula)
#           print("====> suposicao com paren "+formula+" =")
           res=m.group(1)           
        elif re.match(r'\"\(.+\)\s*[0-9]+[0-9a-z]*\"',formula):
           m=re.match(r'\"\((.+)\).*\"',formula)
#           print( "ACHOU descarte =")
           res=m.group(1)
 #          print(m)
#           print("####")
#           print(res)
        elif re.match(r'\"\(.+\)\"', formula):
           m=re.match(r'\"\((.+)\)\"', formula)
 #          print( "achou o padrao com paren")           
           res=m.group(1)
        elif re.match(r'[A-Za-z0-9]+', formula):
           m=re.match(r'([A-Za-z0-9]+)', formula)
 #          print( "achou o padrao mais simples")                      
           res=m.group(1)
        else:
           res="error"
 #       print("===>OUT raw_formula"+res)
        return res


def associative_source_and_target_lists(g):
   list_in={}
   list_out={}
   list_in_Discharge={}
   list_out_Discharge={}
   edges=g.get_edge_list()
   nodes=g.get_node_list()
   for ns in nodes:
      list_out[ns.get_name()]=[]
      list_in[ns.get_name()]=[]
      list_out_Discharge[ns.get_name()]=[]
      list_in_Discharge[ns.get_name()]=[]
      for e in edges:
          if igual(e.get_source(),ns.get_name()) and not igual(e.get('color'),'red'):
             list_out[ns.get_name()].append(e)
             print("aresta= "+e.to_string()+" tem indice em list_out= "+ns.get_name())
          if igual(e.get_destination(),ns.get_name()) and not igual(e.get('color'),'red'):
             list_in[ns.get_name()].append(e)
             print("aresta= "+e.to_string()+" tem indice em list_in= "+ns.get_name())
          if igual(e.get_destination(),ns.get_name()) and igual(e.get('color'),'red'):
             print("Entrou aresta de descarte")
             list_in_Discharge[ns.get_name()].append(e)
             print("aresta= "+e.to_string()+" tem indice em list_in_Discharge= "+ns.get_name())
          if igual(e.get_source(),ns.get_name()) and igual(e.get('color'),'red'):
             list_out_Discharge[ns.get_name()].append(e)
             print("aresta= "+e.to_string()+" tem indice em list_out= "+ns.get_name())             
   return (list_out,list_in,list_in_Discharge,list_out_Discharge)

def find_root(g):
  global e_out
  global e_in
  global e_out_D
  global e_in_D  
  print(" finding the root ")
  print(e_out)
  print(e_in)
  print(" ======= ARESTAS de DESCARTE =======")
  print(e_out_D)
  n=g.get_node_list()
  i=0
  while i < len(n) and not (n[i]):
     i=i+1
  na=n[i]
  print("na="+na.get_name())
  print("label="+g.get_node(na.get_name())[0].get_label())
  print("na="+na.get_name()+"label="+g.get_node(na.get_name())[0].get_label())
  print(type(na))
  na=na.get_name()
  print("na="+na+"label="+g.get_node(na)[0].get_label())
  while na in e_out and len(e_out[na])>0:
    print("na="+na+"label="+g.get_node(na)[0].get_label())
    print(" Lista de nos sainde de na="+na+" ===> ")
    print(e_out[na][0])
    na=(e_out[na][0]).get_destination()
  
  print(" A Raiz do DLDS = "+g.get_node(na)[0].get_label()+" ou "+na)
  return na

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

def write_vetor_oc(t,nivel):
    header=["formulas"]
    for i in range(0,nivel):
        header.append(str(i))
    with open('img/vetorocorrencias.csv', 'w') as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(header)
        for f in list_formulas_proof:
            row=[f]
            for r in t[f]:
               row.append(str(r))     
            writer.writerow(row)

def ordem_formula(f,l):
   i=1
   
   while (l[i-1] != f) and (i<len(l)):
      i=i+1
   if l[i-1]==f:
     return i-1
   else:      
     return -1
   

def dependency_set(l):
   v=0
   i=0
   for b in reversed(l):
      v = v+b*2**i
      i=i+1
   return v

def antecedente(f):
   if re.match(r'\"?(.+) +imp +\(.+\)\"?',f):
      m=re.search(r'\"?(.+) +imp +\(.+\)\"?',f)
      res=m.group(1)
   elif re.match(r'\"?(.+) +imp +[A-Za-z0-9]+\"?',f):
      m=re.search(r'\"?(.+) +imp +[A-Za-z0-9]+\"?',f)
      res=m.group(1)
   else:
      res="error"
   return(res)

def conjunto(s):
  i=int(s)+(2**(len(list_formulas_proof)))
  l=[int(j) for j in bin(i)[2:]]
  return(l[1:])

def bitor(l1,l2):
  l=[0]*len(list_formulas_proof)
  for j in range(0,len(list_formulas_proof)):
    if l1[j]==1 or l2[j]==1:
            l[j]=1
  return(l)

        
def desliga_bit_ordem(l,n):
    l1=l
    l1[n]=0
    return(l1)
  


def label(e):
  global e_out
  global e_in
  global list_formulas_proof      
  conj_depen=[]
  node_source=graph_from_file.get_node(e.get_source())[0]
  if len(e_in[node_source.get_name()])==0:
      formula=raw_formula(node_source.get_label())
      conj_depen=[0]*len(list_formulas_proof)
      bit_formula=ordem_formula(formula,list_formulas_proof)
      conj_depen[bit_formula]=1
      valor_bitstring=dependency_set(conj_depen)
      grava_conjdepen(str(valor_bitstring), conj_depen)
      e.set_label("DS")
      e.set_comment(str(valor_bitstring))      
      e.set_URL(str(valor_bitstring)+".conjdep")
      return(str(valor_bitstring))
  elif len(e_in[node_source.get_name()])==1:
      formula=raw_formula(node_source.get_label())          
      label1=label(e_in[node_source.get_name()][0])
      formula_ant=antecedente(formula)
      ordem=ordem_formula(formula_ant,list_formulas_proof)
      if ordem>=0:
       label_set=conjunto(label1)
       label_set=desliga_bit_ordem(label_set,ordem)
       label1=dependency_set(label_set)
       e.set_label("DS")       
       e.set_URL(str(label1)+".conjdep")
       grava_conjdepen(str(label1), label_set)       
       return(str(label1))      
      else:
       return("Erro antecedente nao está em lista_formulas_proof"+" antecedente de "+formula+" ="+formula_ant)       
  elif len(e_in[node_source.get_name()])==2:
      label_set1=conjunto(label(e_in[node_source.get_name()][0]))
      label_set2=conjunto(label(e_in[node_source.get_name()][1]))

      label_set=bitor(label_set1,label_set2)
      label_2premissas=dependency_set(label_set)
      e.set_label("DS")
      e.set_comment(str(label_2premissas))
      e.set_URL(str(label_2premissas)+".conjdep")
      grava_conjdepen(str(label_2premissas), label_set)             
      return(str(label_2premissas))
  else:
      return("ERRO")

def grava_conjdepen(bs,cd):
  global list_formulas_proof
  global conjdepen_gravados
  if bs not in conjdepen_gravados:
     f=open("img/"+bs+".conjdep","a")
     follow=False
     for j in range(0,len(cd)):   
         if cd[j]==1:
                 if follow:
                    f.write(", ")
                 f.write(list_formulas_proof[j])
                 follow=True
     f.close()
     conjdepen_gravados.append(bs)

def collapsible_nodes(node_formula, node_formulas):
        f=raw_formula(node_formula.get_label())
        collapsibles=[]
        for node in node_formulas:
                if node != node_formula and f==raw_formula(node.get_label()):
                        collapsibles.append(node)
        return(collapsibles)

def Ancestor_Edge(s,d,l):
   global e_in_A
   global e_out_A
   if not d.get_name() in e_in_A:
      e_in_A[d.get_name()]=[]
   if not s.get_name() in e_out_A:
      e_out_A[s.get_name()]=[]
   e=pd.Edge(s,d,label="A["+str(l)+"]", color="blue")
   e_out_A[s.get_name()].append(e)
   e_in_A[d.get_name()].append(e)
   return e


def prepare_to_identify(detour_label,n,g):
  global e_in_A
  global e_in
  if not n.get_name() in e_in_A:
# There is no ancestor edge arriving in n             
   print(" PREPARE-TO-IDENTIFY: no "+n.get_name()+" rotulado com "+n.get_label()+" tem e_in_A[n.get_name()] vazio")
   if len(e_in[n.get_name()])==2:
    print(" PREPARE-TO-IDENTIFY: np "+n.get_name()+" rotulado com "+n.get_label()+" é conclusão de imply-Elim, premissas:")
    print(e_in[n.get_name()])
    e0=e_in[n.get_name()][0]
    e1=e_in[n.get_name()][1]
    p0=e0.get_source()
    p1=e1.get_source()    
    p0_node=g.get_node(p0)[0]    
    p1_node=g.get_node(p1)[0]
    e=e_out[n.get_name()][0]
    v=e.get_destination()
    v_node=g.get_node(v)[0]
    dep_set_e=e.get_comment()
    g.add_edge(Ancestor_Edge(v_node,p0_node,detour_label))
    g.add_edge(Ancestor_Edge(v_node,p1_node,detour_label))
    n_new=e.get_source()
    n_source=g.get_node(n_new)[0]
    e_conclusion=Deduction_Edge(n_source,v_node,detour_label)
    e_conclusion.set_comment(dep_set_e)
    g.add_edge(e_conclusion)
    detour_label=detour_label+1
  elif not n.get_name() in e_out_A:
# There is at least one ancestor edge arriving in n and no ancestor edge going out of n          
    print( "PREPARE-TO-IDENTIFY: Caso que no= "+n.get_name()+" rotulado com "+n.get_label()+" tem e_out_A vazio, mas e_in_A diferente de vazio")
    if  n.get_name() in e_in:
     deletion_list=[]
     for e in e_in_A[n.get_name()]:
       source_A=e.get_source()
       n_source_A=g.get_node(source_A)[0]
       for e_p in e_in[n.get_name()]:
           p_n=e_p.get_source()
           p_n_node=g.get_node(p_n)[0]
           dl=e_p.get_label()
           g.add_edge(Ancestor_Edge(n_source_A,p_n_node,dl))
       deletion_list.append(e)
     for e in deletion_list:
       e_out_A[e.get_source()].remove(e)
       e_in_A[e.get_destination()].remove(e)
       g.del_edge(e.get_source(),e.get_destination())
  else:
     print( "PREPARE-To-IDENTIFY: no= "+n.get_label()+" tem out_A diferente de vazio")

def identify(n,detour_label,v,g):
    global discharged_occurrences
    global conclusions
    global e_out_A
    global e_in_A
#    global detour_label
# storing the label of v before its deletion in the algorithm below
# the label of v will indicate whether it has discharging edges that must be attached to n
# besides this, the label of n has to incorporate the number discharged
    label_of_v=v.get_label()
    print( "vai identificar n="+str(n.get_label())+" e v="+str(v.get_label()))
    print( "vai identificar n="+str(n.get_name())+" e v="+str(v.get_name()))
    delete_from_sources=[]
    delete_from_targets=[]
#    print( "e_in_A.has_key(v.get_name())")
#    print( v.get_name() in e_in_A)
    if not v.get_name() in e_in_A:
     print("o no "+v.get_name()+" tem aresta ancestral chegando nele")       
     if v.get_name() in e_in:
      print("o no "+v.get_name()+" tem aresta de deducao chegando nele")
#  Rule 1 application      
      for e1 in e_in[v.get_name()]:
        print( "name = "+v.get_name())
        print( e1)
        p=e1.get_source()
        print( p)
        p_node=g.get_node(p)[0]
        print( "name e1 p ="+p_node.get_label()+" e "+"v = "+v.get_label())
#    Só adiciona aresta de dedução se não houver já uma aresta de dedução entre p_node e p
        if not Double_Deduction_Edge(p_node,n):
          g.add_edge(Deduction_Edge(p_node,n,0))
        delete_from_sources.append(e1)
        print( "LISTA DE EDGES SAINDO DE "+v.get_label()+v.get_name())
        print( e_out[v.get_name()])
        for e2 in e_out[v.get_name()]:
            v1=e2.get_destination()
            v_node=g.get_node(v1)[0]
            g.add_edge(Ancestor_Edge(v_node,p_node,detour_label))
            if not e2 in delete_from_targets:
               delete_from_targets.append(e2)
      for e2 in e_out[v.get_name()]:
#            print( e2)
            v1=e2.get_destination()
#            print( v1)
            v_node=g.get_node(v1)[0]
#            print "imrpimindo n e v_node "
#            print n
#            print v_node
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
#            print "VAI ADICIONAR UMA ARESTA de "+n.get_name()+" PARA "+v_node.get_name()
            if not Double_Deduction_Edge(n,v_node):
              g.add_edge(Deduction_Edge(n,v_node,detour_label))
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
      detour_label=detour_label+1
     else:
# Rule 3 or Rule 4             
      delete_from_targets=[]
      for e2 in e_out[v.get_name()]:
#        print e2
        v1=e2.get_destination()
        v_node=g.get_node(v1)[0]
#        print "VAI ADICONAR UMA ARESTA de "+n.get_label()+" PARA "+v_node.get_label()
        if not Double_Deduction_Edge(n,v_node):
          g.add_edge(Deduction_Edge(n,v_node,0))
          print(" we will annotate in the formula that it is the label of the node n that it is also an hypothesis for it was collapsed with one")
          n.set_label(n.get_label()+"H")
        if not e2 in delete_from_targets:
          delete_from_targets.append(e2)
      for e in delete_from_targets:
#          print "e_in[e.get_destination()]"
#          print e_in[e.get_destination()]
          e_in[e.get_destination()].remove(e)
          g.del_edge(e.get_source(),e.get_destination())
      g.del_node(v.get_name())
    elif not v.get_name() in e_out_A:
     print( "e_out_A.has_key(v.get_name())= "+str(v.get_name() in e_out_A))
     print( "IDENTIFY: elif not e_out_A.has_key(v.get_name()) Caso com no= "+v.get_label()+" com lista de ancestor-saindo vazia, mas ancestor-chegando (e_in_A) nao vazia")
     print( "IDENTIFY: e_in_A= ")
     print( e_in_A[v.get_name()])
     if v.get_name() in e_in:
      print(" e_in[v.get_name()] =")
      print(e_in[v.get_name()])
      for e1 in e_in[v.get_name()]:
        print( "name = "+v.get_name())
        p=e1.get_source()
        p_node=g.get_node(p)[0]
        print( "IDENTIFY: e_in.has_key(v.get_name()) name e1 p ="+p_node.get_label()+" e "+"v = "+v.get_label()+" n="+n.get_label()+" Double_Deduction_Edge= ")
        print( Double_Deduction_Edge(p_node,n))
        if not Double_Deduction_Edge(p_node,n):
          print( "VAI ADICIONAR ARESTA DE "+p_node.get_label()+" para "+n.get_label())
          g.add_edge(Deduction_Edge(p_node,n))
        delete_from_sources.append(e1)
#        print "LISTA DE EDGES SAINDO DE "+v.get_label()+v.get_name()
#        print e_out[v.get_name()]
        for e2 in e_out[v.get_name()]:
            v1=e2.get_destination()
            print(v1)
            v_node=g.get_node(v1)[0]
            g.add_edge(Ancestor_Edge(v_node,p_node))
            if not e2 in delete_from_targets:
               delete_from_targets.append(e2)
      delete_from_targets=[]
      for e2 in e_out[v.get_name()]:
            print("Aresta saindo")  
            print( e2)
            v1=e2.get_destination()
            print( "ponto de parada = "+v1)
            print(g.get_node(v1))
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
      print( "delete in_edge_Ancestor")
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
      print( "IDENTIFY: no= "+v.get_label()+" tem out_A diferente de vazio, portanto um grafo sintaticamente errado")
# this part takes care of the discharged edges that must be attached to n as well as the number discharged that has
# to be in the label of n
# Testing if the node v is the discharged formula  of a discharging rule (imply-intro)
    if re.match(r'\[.+\][0-9]+',label_of_v):
       m=re.search(r'\[.+\]([0-9][0-9a-z]*)',label_of_v)
       print( "v ====> "+label_of_v+" ="+m.group(1))
       if re.match(r'\[.+\][0-9]+',n.get_label()):
         m1=re.search(r'\[.+\]([0-9][0-9a-z]*)',n.get_label())
         print( "n ======> "+n.get_label()+" ="+m1.group(1))
         if m.group(1)==m1.group(1):
            print( "SAO IGUAIS")
# We do not need to add a new edge. Both edges got to the same intro-imply rule instance application (conclusion[m.group(1)])
# The only obligation is to delete the v node.
         else:
# Since n and v are discharged by different instance of intro-imply, after collapsing n and v in n we have to add the new edge
# from n to the conclusion that was obtained with the instance rule app that discharged v (conclusions[m.group(1)]) and
#  change the labels of n accordingly
            if conclusions[m.group(1)]!=conclusions[m1.group(1)]:
               g.add_edge(pd.Edge(n,conclusions[m.group(1)],color="red"))
            n.set_label(n.get_label()+str(m.group(1)))
# Deleting the node v.  I DO NOT KNOW WHETHER THE FORMER EDGE FROM v TO conclusions[m.group(1)] is deleted automaticaly when v is
         print( "APAGANDO ARESTA "+v.get_label()+"==> "+ conclusions[m.group(1)].get_label())
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
         print( "COLLAPSO DE REGRA DE INTRODUCAO v ====> "+label_of_v+" ="+m.group(1))
         if re.match(r'\(.+\)\s*[0-9]+',n.get_label()):
           m1=re.search(r'\(.+\)\s*([0-9][0-9a-z]*)',n.get_label())
           print( "COM REGRA DE INTRODUCAO n ====> "+ m1.group(1))
#          print "n ======>  ="+ m1.group(1)
           if m.group(1)==m1.group(1):
              print( "SAO IGUAIS, SERIA UM ERRO ?")
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
              print( "collapsing_nodes: atualizando conclusions: "+m1.group(1)+"--> "+n.get_label())
              print( "collapsing_nodes: atualizando conclusions: "+m.group(1)+"--> "+n.get_label())
              conclusions[m.group(1)]=n
              conclusions[m1.group(1)]=n
              g.del_node(v.get_name())
# FALTARIA ATUALIZAR A ESTRUTURA discharged_occurrence, mas precisa avaliar a necessidade DISSO
         else:
           print( "COM REGRA DE ELIMINACAO n ++++++> "+ m1.group(1))
           n.set_color("purple")
# Deleting the node v.  I DO NOT KNOW WHETHER THE FORMER EDGE FROM v TO conclusions[m.group(1)] is deleted automaticaly when v is
         # print "APAGANDO ARESTA "+v.get_label()+"==> "+ conclusions[m.group(1)].get_label()
         # g.del_edge(v,conclusions[m.group(1)])
         # g.del_node(v.get_name())
    return g


def Deduction_Edge(s,d,det_label):
   global e_in
   global e_out
#   print "CRIANDO EDGE de "+ s.get_name()+ "Para "+d.get_name()
#   print "CRIANDO EDGE de "+ s.get_label()+ "Para "+d.get_label()
#  Tem efeito nulo se ja existe aresta de s para d. O grafo de prova eh um grafo simples colorido (no maximo uma aresta de
#  cada cor entre cada par de vertices
   if not d.get_name() in e_in:
      e_in[d.get_name()]=[]
   if not s.get_name() in e_out:
      e_out[s.get_name()]=[]
   if det_label == 0:   
     e=pd.Edge(s,d)
   else:
     e=pd.Edge(s,d,label=det_label)
   e_out[s.get_name()].append(e)
   e_in[d.get_name()].append(e)
   return e


def Double_Deduction_Edge(s,d):
   print("Double_Deduction_Edge")
   v1 = set(e_out[s.get_name()])
   print( "conjunto v1")
   v1_labels={(x.get_source(),x.get_destination()) for x in v1}
   # print v1
   # print v1_labels
   # print s.get_label()
   v2 = e_in[d.get_name()]
   print( "conjunto v2")
   v2_edges={(x.get_source(),x.get_destination()) for x in v2}
   # print v2
   # print v2_edges
   # print d.get_label()
   inter = v1.intersection(v2)
   print( "INtersecao ====================")
   print( inter)
   return inter



def collapsing_nodes(i,f,node_keep,nodes_repeated,g):
    print( "Collapsing Equally Labeled Nodes in the list =>")
    print( nodes_repeated)
    print(" node_keep =")
    print( node_keep)
    node_keep.set_color( "green")
    node_keep.set_style("filled")
    # for n in nodes_repeated:
    #    print( "labels = "+n.get_label()+"name "+n.get_name())
    #    print(n)
    #    n.set_color( "blue")
    #    n.set_style("filled")
#   Gravando resultado parcial
    intermediograph=pd.graph_from_dot_data(g.to_string())
    print( "gravando dot file em collapsing_nodes somente com a marcação com cores azul e roxo")
    intermediograph.write("img/"+g.get_name()+"MarcacaoDoNiv"+str(i)+"Formula"+f+".dot")
#    node_keep=nodes_repeated[0]
    dl=1  # detour_label = 1
    prepare_to_identify(dl,node_keep,g)
    intermediograph=pd.graph_from_dot_data(g.to_string())
    print( "gravando dot file em collapsing_nodes após o prepare_to_identify em node_keep com a marcação com cores azul e roxo")
    intermediograph.write("img/"+g.get_name()+"PrepareNodeKeepDoNiv"+str(i)+"Formula"+f+".dot")    
#    del nodes_repeated[0]
    print( "nos node_repeated = ")
    print( nodes_repeated)
    for n in nodes_repeated:
       print( "n = "+n.get_label()+" name= "+n.get_name())
       print(" vai identificar ")
       print(node_keep)
       print(" com ")
       print(n)
       g=identify(node_keep,dl,n,g)
       print( "collapsing_nodes: Gerando dot string para gravacao")
       intermediograph=pd.graph_from_dot_data(g.to_string())
       print( "gravando dot file com collapso em sequencia das repeticoes")
       intermediograph.write("img/"+g.get_name()+"IntermediodeNiv"+str(i)+"For-"+f+"CollapsingSequel.dot")
    node_keep.set_color( "red" )
    intermediograph=pd.graph_from_dot_data(g.to_string())
    print( "gravando dot file em collapsing_nodes ANTES da compressao horizontal, nos  colapsados estao em azul")
    intermediograph.write("img/"+g.get_name()+"IntermediodeNiv"+str(i)+"ForCollapsed-"+f+".dot")
#    node_keep.set_color( "green" )
    return g

  
# ======================Start Main ==============================          
print(" Vai ler a prova ")
graph_from_file=pd.graph_from_dot_file("img/Prova.dot")

(e_out,e_in,e_in_D,e_out_D)=associative_source_and_target_lists(graph_from_file)
for (n,l) in list(e_in.items()):
   print(n+"e_in[n]=")
   for v in l:
       print(v.to_string()+" v.string() ")
       print(v)
root=find_root(graph_from_file)
print(root)
node_root=graph_from_file.get_node(root)
print(node_root[0].get_label())
nr=node_root
print("nr "+nr[0].get_name())
nivel=0
node_formulas={}
node_formulas[nivel]=nr
print(" node_formulas inicial")
print(node_formulas[0])


while len(node_formulas[nivel])>0:
   node_formulas[nivel+1]=[]
   print(" Inicio do while de formulas[nivel], nivel = "+ str(nivel)+" node_formulas[nivel]")
   print(node_formulas)
   for n in node_formulas[nivel]:
#    n.set_color( "blue")
#    n.set_style("filled")
    if len(e_in[n.get_name()])>0:
     print(" tem aresta chegando no node "+n.get_name())
     no=graph_from_file.get_node(n.get_name()) 
     print(no[0].get_label())
     for e in e_in[n.get_name()]:
       print( " mostra edge")
       node_up=graph_from_file.get_node(e.get_source())[0]
       node_formulas[nivel+1].append(node_up)
       print("DEPOIS de append de node_up")
       print(node_formulas[nivel+1])
    print("node_formulas depois do if len(e_in[n.get_name()])>0")
    print(node_formulas[nivel+1])
    if len(node_formulas[nivel+1])>0:
      print(" Nao vazia")       
      print({ n.get_label() for n in node_formulas[nivel+1]})
    else:
      print(" lista vazia")
   print("Fez o NIVEL="+str(nivel+1))
   graph_from_file.write("img/"+str(nivel)+"InputGraph-ProvaNonHamiltonicity-copia.dot")   
   nivel=nivel+1

# calculando vetores de ocorrencias

v_oc={}
repeated_node_formulas={}
global list_formulas_proof
global conjdepen_gravados
list_formulas_proof=[]
list_node_leaves=[]
conjdepen_gravados=[]


print("---------------------------------------------------------")
print("---------------------------------------------------------")
print("---------------------------------------------------------")


for (n,l) in list(node_formulas.items()):
  for node_formula in l:  
   formula=node_formula.get_label()
   if len(e_in[node_formula.get_name()])==0:
#          node_formula.set_color('red')
#          node_formula.set_style('filled')
          list_node_leaves.append((n,node_formula))
   print("formula no loop (n,l)"+formula)
   print(type(formula))
   formula_raw=raw_formula(formula)
   if formula not in list_formulas_proof:
     list_formulas_proof.append(formula_raw)
print(" Total List of Formulas in the proof ")
print(list_formulas_proof)

print("ordem de q"+str(ordem_formula('q',list_formulas_proof)))

# Labeling the edges with the dependdency-sets

print("nr "+nr[0].get_name())
print(e_in[nr[0].get_name()])
label_premiss1=label(e_in[nr[0].get_name()][0])
label_premiss2=label(e_in[nr[0].get_name()][1])
print("premissa1 label="+label_premiss1)
print("premissa2 label="+label_premiss2)
e_in[nr[0].get_name()][0].set_comment(label_premiss1)
print("printing "+e_in[nr[0].get_name()][0].get_comment())          
           
           

            


for f in list_formulas_proof:
     v_oc[f]=[]
     for n in range(0,nivel):
       v_oc[f].append(0)

       
       

print(v_oc)



for (n,l) in list(node_formulas.items()):
  for node_formula in l:  
   formula=node_formula.get_label()
   formula_raw=raw_formula(formula)
   v_oc[formula_raw][n]=v_oc[formula_raw][n]+1
   if (v_oc[formula_raw][n]>1):
     print("vetor v_oc nivel"+str(n)+" formula="+formula_raw)      
     print(str(v_oc[formula_raw][n]))

     
for (n,l) in node_formulas.items():
 print( "nivel="+str(n))
 print( "LISTA DE NOS=")
 print( l)
 print( "============FIM DE LISTA")


for n in range(0,nivel):
    print( "ocorrências do nível "+str(n))
    print(node_formulas[n])
    for node_formula in node_formulas[n]:
      f=node_formula.get_label()
      node_formula.set_color( "none")
      node_formula.set_style("filled")
      f=raw_formula(f)
      if v_oc[f][n]>1:
        print( "formula="+f+" ocorre "+str(v_oc[f][n])+" vezes no nivel"+str(n))
        list_collapsible=collapsible_nodes(node_formula, node_formulas[n])
        print("node_formula=")
        print(node_formula)
        print("Collapsible nodes=")
        print(list_collapsible)
        for no in list_collapsible:
                print("labels of collapsible nodes ="+raw_formula(no.get_label()))
        collapsing_nodes(n,f,node_formula,list_collapsible,graph_from_file)
        
        

write_vetor_oc(v_oc,nivel)
#-------   Final alteracao
print("seqnode="+str(seqnode))
# l_nodes=graph_from_file.get_node_list()
# num_oc_formulas=len(l_nodes)
# print("num_oc_formulas="+str(num_oc_formulas))
#  Starting the horizontal collapsing
print( "COLLAPSING THE REPEATED FORMULAS")
print( "Gerando graph_from_dot_data ANTES-COMPRESSAO ")
sgraph=pd.graph_from_dot_data(graph_from_file.to_string())
print( "gravando dot file")

sgraph.write("img/"+sgraph.get_name()+"ANTES.dot")
print( "GRAVOU")
#i=0
#while i < nivel and v_oc[i]:
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
#        grafo_compressed=collapsing_nodes(i,f,v_repeated_nodes[i][f],graph_from_file)

#     print "Gerando graph_from_dot_data  DEPOIS-COMPRESSAO do nivel "+str(i)
#     sgraph=pd.graph_from_dot_data(graph_from_file.to_string())
#     print "gravando dot file"
#     sgraph.write("img/"+sgraph.get_name()+"DEPOISniv"+str(i)+".dot")
# #    i=i+1






print(" Vai gravar o que leu ")
graph_from_file.write("img/InputGraph-ProvaNonHamiltonicity-copia.dot")

