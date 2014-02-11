#!/usr/bin/python

#input is of the form [(sourcestate,targetstate,chars),...]
def gen_edge_list(description):
        ret=[]
        for i in description:
                ret+=[(i[0],i[1],c) for c in i[2]]
        return ret

#given a list of edges of an automata,returns a list of tuples of nodes and outgoing edges
def extract_g_info(edges):
	nodes=[]
	for i in edges:
		if ([i[0],[]] not in nodes):
			nodes.append([i[0],[]])
		if ([i[1],[]] not in nodes):
			nodes.append([i[1],[]])
	for n in nodes:
		for e in edges:
			if e[0]==n[0]:
				n[1].append(e[1:])
	return nodes

    

main_body_f=lambda x: "def "+x+"""(str):
    state=0
    
    
    for c in str:"""


#generates the code for the transitions from a single states.takes one item from the  list given by extract_g_info
def gen_state_if(info):
        body="\n\tif (state=="+str(info[0])+"):"
        info=info[1]
        transition=lambda x:"\n\t\tif (c==\'"+x[1]+"\'):\n\t\t\tstate="+str(x[0])+"\n\t\t\tcontinue"
        body=body+''.join(map(transition,info))+"\n\t\treturn False"
        return body


final_states=lambda states:"\n    if state in ["+','.join(map(str,states))+"]: return True\n    else: return False "

gen_automata=lambda name,edges,fstates:main_body_f(name)+''.join(map(gen_state_if,extract_g_info(gen_edge_list(edges))))+final_states(fstates)




#random word generator from an automata goes here
rand_main_body_f=lambda x,body: "def "+x+"""(length):
    from random import choice
    state=0
    ret=""
    while_cond=True
    while ((len(ret)<length) or (state!=0)):"""+body+"""
    return ret"""

def rand_gen_one_state(info):
        return "\n\tif (state=="+str(info[0])+"):\n\t\tret+=choice(\""+info[2]+"\")\n\t\tstate="+str(info[1])

def gen_gen(edges):
        return rand_main_body_f("gen",''.join(map(rand_gen_one_state,edges)))
        
        






if (__name__ == "__main__"):
        c=input("1 for parser,2 for generator:")
        if c==1:
                x=input("edges:")
                main_body=gen_automata("parse",x,[0])
                print main_body
                exec main_body        
                while (True) :
                        x=raw_input("string:")
                        print parse(x)
        elif c==2:
                x=input("edges:")
                main_body=gen_gen(x)
                print main_body
                exec main_body
                x=input("length:")
                while (x!=-1) :
                        print gen(x)
                        x=input("length:")
