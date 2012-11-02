#!/usr/bin/python

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
    output=""
    
    for c in str:"""
#+"return output"

#generates the code for the transitions from a single states.takes one item from the  list given by extract_g_info
def gen_state_if(info):
        body="\n\tif (state=="+str(info[0])+"):"
        info=info[1]
        transition=lambda x:"\n\t\tif (c==\'"+x[1]+"\'):\n\t\t\tstate="+str(x[0])+"\n\t\t\tcontinue"
        body=body+''.join(map(transition,info))+"\n\t\treturn \"fail\""
        return body


final_states=lambda states:"\n    if state in ["+','.join(map(str,states))+"]: return True\n    else: return False "

gen_automata=lambda name,edges,fstates:main_body_f(name)+''.join(map(gen_state_if,extract_g_info(edges)))+final_states(fstates)

if (__name__ == "__main__"):
        x=input("edges:")
        main_body=gen_automata("parse",x,[0])
        print main_body
        exec main_body        
        while (True) :
                x=raw_input("string:")
                print parse(x)



