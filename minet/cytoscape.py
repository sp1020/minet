"""
This module creates a graph model and converts it into an XGMML format file for visualization in Cytoscape.

Nodes:
    Each node has a unique "identifier" and "properties".

    - "identifier": A string that uniquely identifies an individual node.
    - "properties": A dictionary containing the node's attributes, where keys are Cytoscape properties and values are the corresponding property values.

Edges:
    An edge has two node "identifiers" and one set of "properties".

    - An edge object connects two node objects, so edges should be added only after the corresponding nodes are defined.
    - If an edge is added before defining the nodes, a warning message will be displayed, and the edge will not be added to the graph.
    - The identifiers must match those of the nodes.
    - Similar to nodes, edge properties are stored in a dictionary, with keys representing Cytoscape properties and values representing the corresponding property values.
"""

import os
import sys

VERBOSE = True


class CytNode:
    """
    Represents a node of the interaction network.
    """

    def __init__(self, nid, properties):
        """
        Initializes a node with index and node properties (dictionary)
        """
        self.nid = nid
        self.properties = properties


class CytEdge:
    """
    Represents an edge of the interaction network.
    """

    def __init__(self, nid1, nid2, properties):
        """
        Initializes an edge with index pairs and edge properties (dictionary)
        """
        self.nid1 = nid1
        self.nid2 = nid2
        self.properties = properties


class CytGraph:
    """
    Represents an interaction network or graph
    """

    def __init__(self, GraphName='graph'):
        """
        Initializes an interaction network or graph
        """
        self.GraphName = GraphName
        self.Nodes = []
        self.Edges = []

        self.node_set = set()

    def print_graph(self):
        """
        Prints the graph into XGMML format.
        """
        line = ''

        # The header for the graph
        line += "<graph directed=\"1\" id=\"42\" label=\"%s\" xmlns=\"http://www.cs.rpi.edu/XGMML\">\n" % self.GraphName

        # Node elements
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

        # Edge elements
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

        # Footer of the graph
        line += "</graph>\n"

        return line

    def add_node(self, nid, properties):
        """
        Adds a node to the graph 

        1. Check the presence of the input node index. 
        2. Create a new node if not present.  
        """
        global VERBOSE

        j = self.get_node_index(nid)
        if j == -1:  # not found
            self.Nodes.append(CytNode(nid, properties))
            self.node_set.add(nid)
        else:
            if VERBOSE:
                print('Warning: the node %s is already present' % nid)
                print(
                    '         the following properties will not be added:', str(properties))

    def add_edge(self, nid1, nid2, properties):
        """
        Adds an edge to the graph

        1. Check the presense of the edge 
        2. Add a new edge if not present in the graph
        """
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
                    print('         this edge will not be added: (%s, %s)' %
                          (nid1, nid2))
        else:
            print('Warning: the nodes in the edge not found.')
            print('         this edge will not be added: (%s, %s)' % (nid1, nid2))

    def get_node_index(self, nid):
        """
        Retrieves the internal node index corresponding to the given node index.
        """
        for i, n in enumerate(self.Nodes):
            if nid == n.nid:
                return i
        return -1

    def get_edge_index(self, nid1, nid2):
        """
        Retrieves the internal edge index corresponding to the given edge indices.
        """
        for i, e in enumerate(self.Edges):
            if e.nid1 == nid1 and e.nid2 == nid2:
                return i
        else:
            return -1


class CytoscapeXGMML:
    """
    Represents an XGMML format graph for visualizaing of the graph using Cytoscape.
    """

    def __init__(self, GraphName='graph'):
        """
        Initializes the graph
        """
        self.Header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n"
        self.Graph = CytGraph(GraphName)

    def add_node(self, nid, properties={}):
        """
        Adds a new node to the graph
        """
        nid = str(nid)
        self.Graph.add_node(nid, properties)

    def add_edge(self, nid1, nid2, properties={}):
        """
        Adds a new edge to the graph
        """
        nid1 = str(nid1)
        nid2 = str(nid2)
        self.Graph.add_edge(nid1, nid2, properties)

    def print_graph(self):
        """
        Convert graph into XML (text).
        """
        lines = self.Header[:]
        lines += self.Graph.print_graph()

        return lines

    def write_graph(self, fn):
        """
        Write the graph into a file
        """
        ls = self.print_graph()
        f = open(fn, 'w')
        f.write(ls)
        f.close()

    def turn_off_warning(self):
        global VERBOSE
        VERBOSE = False
