# Node stores each point of the block
class Node:
    def __init__(self, coordinates, color):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.color = color

# Face stores 4 nodes that make up a face of the block
class Face:
    def __init__(self, nodes, color):
        self.nodeIndexes = nodes
        self.color = color

# Wireframe stores the details of the block
class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.faces = []

    def addNodes(self, nodeList, colorList):
        for node, color in zip(nodeList, colorList):
            self.nodes.append(Node(node, color))

    def addFaces(self, faceList, colorList):
        for indexes, color in zip(faceList, colorList):
            self.faces.append(Face(indexes, color))

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f) \t Color: (%d, %d, %d)" %
                 (i, node.x, node.y, node.z, node.color[0], node.color[1], node.color[2]))

    def outputFaces(self):
        print("\n --- Faces --- ")
        for i, face in enumerate(self.faces):
            print("Face %d:" % i)
            print("Color: (%d, %d, %d)" % (face.color[0], face.color[1], face.color[2]))
            for nodeIndex in face.nodeIndexes:
                print("\tNode %d" % nodeIndex)