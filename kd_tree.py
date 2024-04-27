
def insert(root, filename, point, depth=0):
    if root is None:
        return {'filename': filename, 'point': point, 'left': None, 'right': None}
    
    k = len(point)
    axis = depth % k
    
    if point[axis] <= root['point'][axis]:
        root['left'] = insert(root['left'], filename, point, depth + 1)
    else:
        root['right'] = insert(root['right'], filename, point, depth + 1)
    
    return root




# Find the inorder successor
def minValueNode(node):
    current = node
    
    while current['left'] is not None:
        current = current['left']
    
    return current


# Deleting a node
def deleteNode(root, point, depth=0):
    if root is None:
        return root

    k = len(point)
    axis = depth % k

    if point[axis] < root['point'][axis]:
        root['left'] = deleteNode(root['left'], point, depth + 1)
    elif point[axis] > root['point'][axis]:
        root['right'] = deleteNode(root['right'], point, depth + 1)
    else:
        if root['left'] is None and root['right'] is None:
            return None
        if root['left'] is None:
            return root['right']
        elif root['right'] is None:
            return root['left']
        else:
            if point[0] == root['point'][0] and point[1] == root['point'][1] and point[2] == root['point'][2]:
                temp = minValueNode(root['right'])
                root['point'] = temp['point']
                root['filename'] = temp['filename']
                root['right'] = deleteNode(root['right'], temp['point'], depth + 1)
            else:
                if point[axis] < root['point'][axis]:
                    root['left'] = deleteNode(root['left'], point, depth + 1)
                elif point[axis] > root['point'][axis]:
                    root['right'] = deleteNode(root['right'], point, depth + 1)

    return root






