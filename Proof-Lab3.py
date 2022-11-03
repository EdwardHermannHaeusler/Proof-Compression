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
#  print "Vai encontrar raiz"
  n=g.get_node_list()
  i=0
  while i < len(n) and not (n[i]):
#    print "i="+str(i)
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

def write_vetor_oc(t):
# building the dict of all key-formulas in t
    formulas=set([])
    i=0
    vector_oc_by_level={}
    for n,l in list(t.items()):
        for f,n_oc in list(l.items()):
            formulas.add(raw_formula(f))
#    print len(formulas)
    header=['formulas']
    for i in range(0,len(t)):
        header.append(i)
    for f in formulas:
        vector_oc_by_level[f]=[f]
        for n in range(0,len(t)):
          if f in t[n]:
            vector_oc_by_level[f].append(t[n][f])
          else:
            vector_oc_by_level[f].append(0)
        with open('img/vetorocorrencias.csv', 'wb') as csv_file:
          writer=csv.writer(csv_file)
          writer.writerow(header)
          for f,formulas_oc in list(vector_oc_by_level.items()):
              writer.writerow(formulas_oc)

def ordem_formula(f,l):
   i=1
   
   while (l[i-1] != f) and (i<len(l)):
      print      
      i=i+1
   if l[i-1]==f:
     return i-1
   else:      
     return -1
   

def dependency_set(l):
   v=0
   i=0
   for b in reversed(l):
      print(v,i,b)     
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
  i=int(s)+(2**(len(list_formulas_proof))+1)
  l=[int(j) for j in bin(i)[2:]]
  print("len(l) de dentro de conjunto(s)="+str(len(l)))
  return(l[:len(list_formulas_proof)])

def bitor(l1,l2):
  l=[0]*len(list_formulas_proof)
  print("len(l1)="+str(len(l1))+" len(l2)="+str(len(l2))+" len(l)="+str(len(l)))
  for j in range(0,len(list_formulas_proof)-1):
    print("indice j= "+str(j)+"l1[j]= "+str(l1[j])+"l2[j]= "+str(l2[j]))      
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
#  print("e.get_source()"+node_source.get_label())
  if len(e_in[node_source.get_name()])==0:
      formula=raw_formula(node_source.get_label())
      conj_depen=[0]*len(list_formulas_proof)
      bit_formula=ordem_formula(formula,list_formulas_proof)
#      print("bit_formula="+str(bit_formula))
      conj_depen[bit_formula]=1
      valor_bitstring=dependency_set(conj_depen)
      grava_conjdepen(str(valor_bitstring)[:5], conj_depen)
#      print(valor_bitstring)
      e.set_label(str(valor_bitstring)[:5])
      e.set_URL(str(valor_bitstring)[:5]+".conjdep")
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
       e.set_label(str(label1)[:5])
       e.set_URL(str(label1)[:5]+".conjdep")
       grava_conjdepen(str(label1)[:5], label_set)       
       print("para formula_ant="+formula_ant+"a ordem foi"+str(ordem))
#       e.set_label(str(label1)[:5])       
       return(str(label1))      
      else:
       return("Erro antecedente nao está em lista_formulas_proof"+" antecedente de "+formula+" ="+formula_ant)       
  elif len(e_in[node_source.get_name()])==2:
      label_set1=conjunto(label(e_in[node_source.get_name()][0]))
      label_set2=conjunto(label(e_in[node_source.get_name()][1]))
      label_set=bitor(label_set1,label_set2)
      label_2premissas=dependency_set(label_set)
      e.set_label(str(label_2premissas)[:5])
      e.set_URL(str(label_2premissas)[:5]+".conjdep")
      grava_conjdepen(str(label_2premissas)[:5], label_set)             
      return(str(label_2premissas))
  else:
      return("ERRO")

def grava_conjdepen(bs,cd):
  global list_formulas_proof
  global conjdepen_gravados
  if bs not in conjdepen_gravados:
     f=open("img/"+bs+".conjdep","a")     
     for j in range(0,len(cd)):
         if cd[j]==1:
                 f.write(list_formulas_proof[j])
     f.close()
     conjdepen_gravados.append(bs)


  
          
print(" Vai ler a prova ")
graph_from_file=pd.graph_from_dot_file("img/Prova.dot")

(e_out,e_in,e_in_D,e_out_D)=associative_source_and_target_lists(graph_from_file)
#Display used during the development phase
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

# Defines node_formula[nivel], i.e., the list of formula nodes by level  

while len(node_formulas[nivel])>0:
   node_formulas[nivel+1]=[]
   print(" Inicio do while de formulas[nivel], nivel = "+ str(nivel)+" node_formulas[nivel]")
   print(node_formulas)
#
   for n in node_formulas[nivel]:
#    print " node_formulas[nivel] no nivel "+str(nivel)
#    print node_formulas
#    print " No n é do tipo "
#    print type(n)        
    n.set_color( "blue")
    n.set_style("filled")
#    print " n.get_name() = "+ n.get_name()
#    print " E_IN AVALIADO em n.get_name()" 
#    print e_in[n.get_name()]
    if len(e_in[n.get_name()])>0:
     print(" tem aresta chegando no node "+n.get_name())
     no=graph_from_file.get_node(n.get_name()) 
     print(no[0].get_label())
#     print " arestas sao ="
#     print e_in[n.get_name()]
#     print " PRIMEIRO node_formulas[nivel+1] "+str(nivel+1)
#     print node_formulas[nivel+1]
     for e in e_in[n.get_name()]:
       print( " mostra edge")
#       e.set_label('label')
#       print(e.get_label())
       node_up=graph_from_file.get_node(e.get_source())[0]
#       print node_up
       node_formulas[nivel+1].append(node_up)
       print("DEPOIS de append de node_up")
       print(node_formulas[nivel+1])
#       print "Fez o n="+n.get_name()
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
global list_formulas_proof
global conjdepen_gravados
#v_repeated_nodes={}
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
          node_formula.set_color('red')
          node_formula.set_style('filled')
          list_node_leaves.append((n,node_formula))
   print("formula no loop (n,l)"+formula)
   print(type(formula))
   formula_raw=raw_formula(formula)
#   print "formula_raw "+formula_raw
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
print("premissa1 label="+label_premiss2)


# conj_depen=[]
# list_edges_downwards=[]
# for (n,node) in list_node_leaves:     
#    if len(e_out[node.get_name()])>0:
#        e=e_out[node.get_name()][0]  
#        list_edges_downwards.append((n,e))
#        formula=raw_formula(node.get_label())
# #       print("CONTROLPOINT")
# #       print("formula raw"+formula)
# #       for i in range(0,len(list_formulas_proof))
#        conj_depen=[0]*len(list_formulas_proof)
# #       print(conj_depen)    
#        bit_formula=ordem_formula(formula,list_formulas_proof)
#        print("bit_formula="+str(bit_formula))
#        conj_depen[bit_formula]=1
#        print(conj_depen)
#        valor_bitstring=dependency_set(conj_depen)
#        print(valor_bitstring)
#        e.set_label(str(valor_bitstring)[:5])

# new_list_edges_downwards=[]       
# list_node_downwards=[]
# for (n,e) in list_edges_downwards:
#  node_dest=e.get_destination()
#  if len(e_out[node_dest])>0:
#     new_edge=e_out[node_dest][0]
#     print(e_in[node_dest])
#     if len(e_in[node_dest])==1:
#        print("e_in[node_dest][0]")
#        print(e_in[node_dest][0])
#        new_edge.set_label(e_in[node_dest][0].get_label()[:5]+"-"+ant)
#     elif len(e_in[node_dest])==2:
#        if isinstance(e_in[node_dest][0], str):    
#           print("e_in[node_dest][0].get_label()")
#           label1=e_in[node_dest][0].get_label()
#           print(label1)
#        else:
#           label1=label(e_in[node_dest][0])     
#        if isinstance(e_in[node_dest][1], str):
#           print("e_in[node_dest][1].get_label()")               
#           label2=e_in[node_dest][1].get_label()
#           print(label2)          
#        else:
#           label2=label(e_in[node_dest][1])               
#        new_edge.set_label(label1[:5]+"+"+label2[:5])
#     new_list_edges_downwards.append((n-1,new_edge))

         



        
 # for (n,e1) in list_edges_downwards:
 #  if i==n:      
 #  for e2 in list_edges_downwards:
 #    if (e1!=e2) and e1.get_destination()==e2.get_destination():
 #        flag=1    
 #        if len(e_out[e1.get_destination()])>0:
 #           e=e_out[e1.get_destination()][0]
 #           new_list_downwards.append(e)
 #           e.set_label(e1.get_label()[:5]+"+"+e2.get_label()[:5])
 #  if (flag==0):
 #        if len(e_out[e1.get_destination()])>0:
 #           e=e_out[e1.get_destination()][0]
 #           new_list_downwards.append(e)
 #           e.set_label(e1.get_label()[:5]+"-ant")
 # list_node_downwards=new_list_downwards
 # i=i+1
          
           
           

            
    # node=e.get_destination()
    # print("node")
    # print(node)
    # list_node_downwards.append(node)

    
       

# i=0       
# for e in list_edges_downwards:
#         e.set_label(str(i))
#         i=i+1

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
   
   



       
        
  # for node_formula in l:
  #  formula=node_formula.get_label()
  #  print "formula "+formula
  #  formula_raw=raw_formula(formula)
  #  print "formula_raw "+formula_raw
  #  if formula_raw in list_formulas_proof:
  #    v_oc[n][formula_raw]=v_oc[n][formula_raw]+1
  #  else:
  #    v_oc[n][formula_raw]=1
  #    list_formulas_proof.append(formula_raw)
     
# for (n,l) in node_formulas.items():
#  print "nivel="+str(n)
#  print "LISTA DE NOS="
#  print l
#  print "============FIM DE LISTA"

# for n in range(0,nivel):
#     print "ocorrências do nível "+str(n)
#     for f in list_formulas_proof:
#       if v_oc[n,f]>0:
#         print "formula="+f+" ocorre "+str(v_oc[n,f])+" vezes"
 
#  for node in l:
#    print node
#    print type(node)
# #   lista_nos_formula=graph_from_file.get_node(f)
#  for f in l:
#    lista_nos_formula=graph_from_file.get_node(f)
#    if lista_nos_formula <> []:
#      node_formula_f=graph_from_file.get_node(f)[0]
#      formula_f=node_formula_f.get_label()
#      formula_f=raw_formula(formula_f)
#      v_oc[n][formula_f]=v_oc[n][formula_f]+1
#      v_repeated_nodes[n][formula_f].append(node_formula_f)
#      #------Alteracao de Inspecao
# print " LISTANDO v_oc[n][formula_f] "
# for n in range(0,len(v_oc)):
#       formula_f=graph_from_file.get_node(f)[0].get_label()
#       if len(v_oc[n][formula_f]) > 1:
#          print "MAIS DE UMA OC = "+str(v_oc[n][formula_f])
#       print n
#       print l
#       print v_oc[n]
# #    Final da Alteracao
#write_vetor_oc(v_oc)
# -------   Final alteracao
print("seqnode="+str(seqnode))
l_nodes=graph_from_file.get_node_list()
num_oc_formulas=len(l_nodes)
print("num_oc_formulas="+str(num_oc_formulas))
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
#        grafo_compressed=collapsing_nodes(i,f,v_repeated_nodes[i][f],graph_from_file)

#     print "Gerando graph_from_dot_data  DEPOIS-COMPRESSAO do nivel "+str(i)
#     sgraph=pd.graph_from_dot_data(graph_from_file.to_string())
#     print "gravando dot file"
#     sgraph.write("img/"+sgraph.get_name()+"DEPOISniv"+str(i)+".dot")
# #    i=i+1






print(" Vai gravar o que leu ")
graph_from_file.write("img/InputGraph-ProvaNonHamiltonicity-copia.dot")

