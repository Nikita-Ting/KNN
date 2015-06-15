#encoding:utf-8 

"create on 2014-8-25"
'''
programing for implementing the KDtree-Binary tree'''

class Node: pass

#list to binarytree
def kdtree(point_list, depth=0):
    if not point_list:
        return None
    # Select axis based on depth so that axis cycles through all valid values
    k = len(point_list[0])-2 # assumes all points have the same dimension, the last one data is classify
    axis = depth % k
    # Sort point list and choose median as pivot element
    #lambda define a anonymous function same as:
#     def name(arguments):
#          return expression
    point_list.sort(key=lambda point: point[axis])
    median = len(point_list) // 2 # choose median

    # Create node and construct subtrees
    node = Node()
    node.location = point_list[median]
    node.split=axis #维度
    node.left_child = kdtree(point_list[:median], depth + 1)
    #列表的分片操作，通过冒号隔开的两个索引实现，第一个索引包含在分片内，第二个不包含；
    node.right_child = kdtree(point_list[median + 1:], depth + 1)
    return node

#先序遍历BinaryTree to list
def preorder(tree,nodelist=None):
    if nodelist is None:
        nodelist=[]
    if tree:
        nodelist.append(tree.location)
        preorder(tree.left_child,nodelist)
        preorder(tree.right_child,nodelist)
    return nodelist

#中序遍历?
def inorder(tree,nodelist=None):
    if nodelist is None:
        nodelist=[]
    if tree:
        inorder(tree.left_child,nodelist)
        nodelist.append(tree.location)
#         print (tree.location)
        inorder(tree.right_child,nodelist)
    return nodelist

#postorder travelsal
def postorder(tree,nodelist=None):
    if nodelist is None:
        nodelist=[]
    if tree:
        postorder(tree.left_child,nodelist)
        postorder(tree.right_child,nodelist)
        nodelist.append(tree.location)
    return nodelist  


def main():
    list=[(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
    node=kdtree(list, depth=0)
    print("!-----先序遍历------!")
    print(preorder(node))
    print("!-----中序遍历------!")
    print(inorder(node))
    print("!-----后序遍历------!")
    print(postorder(node))
    
    
if(__name__ == "__main__"):
    main();