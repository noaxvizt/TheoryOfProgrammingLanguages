def DFS(node):
    print(node.value)
    if node.type == 'u':
        DFS(node.left)
    if node.type == 'b':
        DFS(node.left)
        DFS(node.right)