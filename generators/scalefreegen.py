import numpy as np

def __InitNetwork(numNodes, deltaIn=1, deltaOut=1):
    return {
    'size': numNodes, 
    'edges': np.zeros((numNodes, numNodes), dtype=int),
    'inDegree': np.zeros(numNodes, dtype=int),
    'outDegree': np.zeros(numNodes, dtype=int),
    'deltaIn': deltaIn,
    'deltaOut': deltaOut
    }

def __AddEdge(net, src, dst):
    if net['edges'][src,dst] == 0:
        net['edges'][src,dst] = 1
        net['outDegree'][src] = 1 + net['outDegree'][src]
        net['inDegree'][dst] = 1 + net['inDegree'][dst]
        return True
    return False

def __PickPrefByInDegree(net, in_exclude=-1):
    exclution_diff = 0
    if in_exclude > -1:
        exclution_diff = net['inDegree'][in_exclude] + net['deltaIn']
    probs = (net['inDegree'] + net['deltaIn']) / (np.sum(net['inDegree']) + net['size'] * net['deltaIn'] - exclution_diff)
    if in_exclude > -1:
        probs[in_exclude] = 0
    return np.random.choice(net['size'], p=probs)

def __PickPrefByOutDegree(net, in_exclude=-1):
    exclution_diff = 0
    if in_exclude > -1:
        exclution_diff = net['outDegree'][in_exclude] + net['deltaOut']
    probs = (net['outDegree'] + net['deltaOut']) / (np.sum(net['outDegree']) + net['size'] * net['deltaOut'] - exclution_diff)
    if in_exclude > -1:
        probs[in_exclude] = 0
    return np.random.choice(net['size'], p=probs)

def GenerateScaleFreeNetwork(numNodes = 100, alpha = 1.0/3.0, beta = 1.0/3.0, deltaIn = 1, deltaOut = 1):
    net = __InitNetwork(numNodes, deltaIn, deltaOut)
    if numNodes < 2 :
        print("numNodes cannot be less than 2")
    #print("Number of Nodes : " + str(numNodes))
    #print("Beta : " + str(beta))
    #print("Alpha : " + str(alpha))
    #print("Gamma : " + str(1 - (alpha + beta)))
    currentNumNodes = 2
    src = 0
    dst = 1
    __AddEdge(net, src, dst)
    while currentNumNodes < numNodes :
        rnd = np.random.uniform()
        if rnd < alpha :
            # new node to existing
            src = currentNumNodes
            currentNumNodes += 1
            dst = __PickPrefByInDegree(net, src)
        elif rnd < alpha + beta:
            # existing to existing
            if 0.5 <= np.random.uniform():
                src = __PickPrefByOutDegree(net)
                dst = __PickPrefByInDegree(net, src)
            else:
                dst = __PickPrefByInDegree(net)
                src = __PickPrefByOutDegree(net, dst)
        else:
            # existing to new node
            dst = currentNumNodes
            src = __PickPrefByOutDegree(net, dst)
            currentNumNodes += 1
        __AddEdge(net, src, dst)
    return net

def GenerateScaleFreeNetworkByBeta(numNodes, beta, deltaIn, deltaOut):
    alpha = (1.0 - beta)/2.0
    return GenerateScaleFreeNetwork(numNodes, alpha, beta, deltaIn, deltaOut)