"""
This code convert the conventional graph into CYTOSCAPE format


NODE 
    Each node has unique "identifier" and "properties"

    "identifier" is a STRING which is uniquely assigned to individual nodes


    "properties" is a dictionary of variables

    the key will be the cytoscape properties of the node
    and the value will be the corresponding values for the property


EDGE

    An edge will have two node "identifier"s and one "properties"

    As an edge object connect two edge object, the addition of the edge object should be done after the nodes are defined. 

    Otherwise, warning message will be displayed and the edge will not be added to the graph. 

    The identifier should be matched to that of the node

    Similar to node the properties are the directory object
    with the key for the cytoscape properties and the corresponding values 
"""

import os
import sys

VERBOSE = True


class CytNode:
    def __init__(self, nid, properties):
        self.nid = nid
        self.properties = properties


class CytEdge:
    def __init__(self, nid1, nid2, properties):
        self.nid1 = nid1
        self.nid2 = nid2
        self.properties = properties


class CytGraph:
    def __init__(self, GraphName='graph'):
        self.GraphName = GraphName
        self.Nodes = []
        self.Edges = []

        self.node_set = set()

    def print_graph(self):
        line = ''
        # graph begin
        line += "<graph directed=\"1\" id=\"42\" label=\"%s\" xmlns=\"http://www.cs.rpi.edu/XGMML\">\n" % self.GraphName

        # print node information
        for n in self.Nodes:
            if 'label' in n.properties:
                label = n.properties['label']
            else:
                label = n.nid
            line += '<node id=\"%s\" label=\"%s\">\n' % (n.nid, label)
            for p in n.properties:
                p = p.lower()

                if type(n.properties[p]) == type(0):  # integer
                    line += '<att name=\"%s\" type=\"integer\" value=\"%d\"/>\n' % (
                        p, int(n.properties[p]))
                elif type(n.properties[p]) == type(1.0):  # float
                    line += '<att name=\"%s\" type=\"real\" value=\"%f\"/>\n' % (
                        p, n.properties[p])
                else:
                    line += '<att name=\"%s\" type=\"string\" value=\"%s\"/>\n' % (
                        p, n.properties[p])

            line += '</node>\n'

        # print edge information
        for e in self.Edges:
            if 'label' in e.properties:
                label = e.properties['label']
            else:
                label = 'gg'
            line += '<edge source=\"%s\" target=\"%s\" label=\"%s\">\n' % (
                e.nid1, e.nid2, label)

            for p in e.properties:

                if type(e.properties[p]) == type(0):  # integer
                    line += '<att name=\"%s\" type=\"integer\" value=\"%d\"/>\n' % (
                        p, int(e.properties[p]))
                elif type(e.properties[p]) == type(1.0):  # float
                    line += '<att name=\"%s\" type=\"real\" value=\"%f\"/>\n' % (
                        p, e.properties[p])
                else:
                    line += '<att name=\"%s\" type=\"string\" value=\"%s\"/>\n' % (
                        p, e.properties[p])

            line += '</edge>\n'

        # graph end
        line += "</graph>\n"

        return line

    def add_node(self, nid, properties):
        global VERBOSE

        j = self.get_node_index(nid)
        if j == -1:  # not found
            self.Nodes.append(CytNode(nid, properties))
            self.node_set.add(nid)
        else:
            if VERBOSE:
                print('Warning: the node %s is already present' % nid)
                print('         the following properties will not be added:', str(properties))

    def add_edge(self, nid1, nid2, properties):
        global VERBOSE
        if nid1 in self.node_set and nid2 in self.node_set:
            j1 = self.get_node_index(nid1)
            j2 = self.get_node_index(nid2)

            je = self.get_edge_index(nid1, nid2)
            if je == -1:  # not found
                self.Edges.append(CytEdge(nid1, nid2, properties))
            else:
                if VERBOSE:
                    print('Warning: the edge (%s, %s) is found' % (nid1, nid2))
                    print('         this edge will not be added: (%s, %s)' % (nid1, nid2))
        else:
            print('Warning: the nodes in the edge not found.')
            print('         this edge will not be added: (%s, %s)' % (nid1, nid2))

    def get_node_index(self, nid):
        for i, n in enumerate(self.Nodes):
            if nid == n.nid:
                return i
        return -1

    def get_edge_index(self, nid1, nid2):
        for i, e in enumerate(self.Edges):
            if e.nid1 == nid1 and e.nid2 == nid2:
                return i
        else:
            return -1


class CytoscapeXGMML:
    def __init__(self, GraphName='graph'):
        self.Header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n"
        self.Graph = CytGraph(GraphName)

    def add_node(self, nid, properties={}):
        nid = str(nid)
        self.Graph.add_node(nid, properties)

    def add_edge(self, nid1, nid2, properties={}):
        nid1 = str(nid1)
        nid2 = str(nid2)
        self.Graph.add_edge(nid1, nid2, properties)

    def print_graph(self):
        lines = self.Header[:]
        lines += self.Graph.print_graph()

        return lines

    def write_graph(self, fn):
        ls = self.print_graph()
        f = open(fn, 'w')
        f.write(ls)
        f.close()

    def turn_off_warning(self):
        global VERBOSE
        VERBOSE = False
