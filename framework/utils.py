from random import sample, randint, choice

def sequence(sites, quantities):
    """Genera una sequencia de sitios segun las cantidades especificadas"""
    seq = list()
    while( sum(quantities) ):
        curr = choice([ i for i,j in enumerate(quantities) if j > 0])
        quantities[curr] -= 1

        seq.append( sites[curr] )
        
    return seq

def Newquences(archive:str, N:int, duplicates = False):
    """Entrega N sequencias. Si duplicates == False entonces, entonces no se repetiran las columnas del archivo ocupadas"""
    with open(archive,"r") as allSites:
        sites = allSites.readlines()

    if N > len(sites) or duplicates == True: 
        order = [ randint(0,len(sites)-1) for i in range(N) ]
    else:  
        order = sample(range(len(sites)),N)

    return [ sites[i].strip("\n").split(",") for i in order ]
