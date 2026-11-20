import re

seed_path = r"c:\Users\omkar\Documents\TY\ML LAB\CP\EduPath-X\EduPath-X\backend\app\database\seed_data.py"
with open(seed_path, "r") as f:
    seed_content = f.read()

questions = [
    # Arrays
    ('ARRAYS', 'MCQ', 'What is the time complexity of accessing an element by index in an array?', ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], 'O(1)', 'Accessing by index is direct memory access.', 'Easy', 30),
    ('ARRAYS', 'MCQ', 'Which of the following is true about dynamic arrays?', ['Size is fixed', 'Resizes automatically', 'Only stores integers', 'Slower access than linked list'], 'Resizes automatically', 'Dynamic arrays resize when they hit capacity.', 'Easy', 30),
    ('ARRAYS', 'MCQ', 'What is the worst-case time complexity for inserting an element at the beginning of an array?', ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], 'O(N)', 'All subsequent elements must be shifted.', 'Medium', 45),
    ('ARRAYS', 'MCQ', 'In a 0-indexed array of size N, what is the index of the last element?', ['N', 'N-1', 'N+1', '1'], 'N-1', 'Indices range from 0 to N-1.', 'Easy', 20),
    ('ARRAYS', 'MCQ', 'What happens if you try to access an index out of the array bounds?', ['Returns 0', 'Returns null', 'Throws an error/exception', 'Wraps around'], 'Throws an error/exception', 'Out of bounds access causes an exception in most languages.', 'Easy', 20),
    ('ARRAYS', 'MCQ', 'Which operation is generally faster in an array compared to a linked list?', ['Insertion at beginning', 'Deletion at beginning', 'Random access', 'Resizing'], 'Random access', 'Arrays have O(1) random access.', 'Medium', 30),
    ('ARRAYS', 'MCQ', 'How much memory does an array of 10 32-bit integers require?', ['10 bytes', '32 bytes', '40 bytes', '320 bytes'], '40 bytes', '10 integers * 4 bytes/integer = 40 bytes.', 'Medium', 45),
    ('ARRAYS', 'MCQ', 'What is a common use case for an array?', ['Implementing a graph', 'Storing elements of varying types safely', 'When size is unknown and changes constantly', 'Storing a fixed-size collection of items of the same type'], 'Storing a fixed-size collection of items of the same type', 'Arrays are best for homogeneous, fixed-size data.', 'Medium', 30),

    # Linked Lists
    ('LINKED_LIST', 'MCQ', 'What is the time complexity to insert a node at the head of a linked list?', ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], 'O(1)', 'Head insertion only requires updating a few pointers.', 'Easy', 30),
    ('LINKED_LIST', 'MCQ', 'What does each node in a singly linked list contain?', ['Value only', 'Value and next pointer', 'Value, next and prev pointers', 'Next pointer only'], 'Value and next pointer', 'Singly linked lists have data and a pointer to the next node.', 'Easy', 30),
    ('LINKED_LIST', 'MCQ', 'How do you find the length of a singly linked list?', ['Return the size property', 'Traverse the list and count nodes', 'Multiply node size by capacity', 'It is not possible'], 'Traverse the list and count nodes', 'Without a cached size variable, traversal O(N) is required.', 'Medium', 45),
    ('LINKED_LIST', 'MCQ', 'What is a disadvantage of a linked list compared to an array?', ['Slower insertion at head', 'Fixed size', 'No random access', 'Requires contiguous memory'], 'No random access', 'You must traverse from the head to access the i-th element.', 'Medium', 30),
    ('LINKED_LIST', 'MCQ', 'In a doubly linked list, what does the prev pointer of the head node point to?', ['The tail node', 'The second node', 'Null', 'Itself'], 'Null', 'The head node has no previous node.', 'Easy', 20),
    ('LINKED_LIST', 'MCQ', 'Which problem can occur if you lose the reference to the head of a linked list?', ['Memory leak', 'Stack overflow', 'Index out of bounds', 'Nothing'], 'Memory leak', 'Without the head, the list nodes cannot be accessed and may leak in unmanaged languages.', 'Medium', 30),
    ('LINKED_LIST', 'MCQ', 'To delete a node X from a singly linked list (given only X), what is a common trick?', ['Copy data from X.next to X and delete X.next', 'Traverse from head', 'Set X to null', 'It is impossible'], 'Copy data from X.next to X and delete X.next', 'This works if X is not the tail.', 'Hard', 60),
    ('LINKED_LIST', 'MCQ', 'What is the time complexity to search for a value in a linked list?', ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], 'O(N)', 'You may have to check every node.', 'Easy', 20),

    # Stacks
    ('STACKS', 'MCQ', 'Which principle does a stack follow?', ['FIFO', 'LIFO', 'Random Access', 'Priority'], 'LIFO', 'Last-In, First-Out.', 'Easy', 20),
    ('STACKS', 'MCQ', 'What is the operation to add an item to a stack called?', ['Push', 'Pop', 'Enqueue', 'Insert'], 'Push', 'Push adds an item.', 'Easy', 20),
    ('STACKS', 'MCQ', 'What is the operation to remove an item from a stack called?', ['Push', 'Pop', 'Dequeue', 'Delete'], 'Pop', 'Pop removes the top item.', 'Easy', 20),
    ('STACKS', 'MCQ', 'Which data structure can be used to easily reverse a string?', ['Queue', 'Linked List', 'Stack', 'Tree'], 'Stack', 'Pushing all characters and popping them reverses the order.', 'Medium', 30),
    ('STACKS', 'MCQ', 'In a function call stack, what happens when a function returns?', ['Its frame is pushed', 'Its frame is popped', 'The stack is cleared', 'Nothing'], 'Its frame is popped', 'The stack frame is removed upon return.', 'Medium', 30),
    ('STACKS', 'MCQ', 'What exception is thrown when popping from an empty stack?', ['Stack Overflow', 'Stack Underflow', 'Index Out of Bounds', 'Null Pointer'], 'Stack Underflow', 'Trying to pop an empty stack is an underflow.', 'Medium', 30),
    ('STACKS', 'MCQ', 'Which problem is traditionally solved using a stack?', ['Breadth First Search', 'Shortest Path', 'Balanced Parentheses', 'Sorting'], 'Balanced Parentheses', 'Stacks are perfect for matching brackets.', 'Hard', 45),
    ('STACKS', 'MCQ', 'If a stack is implemented using an array, what is the time complexity of push?', ['O(1) amortized', 'O(N)', 'O(log N)', 'O(N^2)'], 'O(1) amortized', 'If the array resizes, it is O(1) amortized.', 'Hard', 45),

    # Queues
    ('STACKS', 'MCQ', 'Which principle does a queue follow?', ['FIFO', 'LIFO', 'Random', 'Priority'], 'FIFO', 'First-In, First-Out.', 'Easy', 20),
    ('STACKS', 'MCQ', 'What is the operation to add an item to a queue?', ['Push', 'Pop', 'Enqueue', 'Dequeue'], 'Enqueue', 'Enqueue adds to the back.', 'Easy', 20),
    ('STACKS', 'MCQ', 'Which algorithm uses a queue naturally?', ['Depth First Search', 'Breadth First Search', 'Binary Search', 'Quicksort'], 'Breadth First Search', 'BFS processes nodes level by level using a queue.', 'Medium', 30),
    ('STACKS', 'MCQ', 'In a circular queue, how is the next position calculated?', ['(index + 1) % capacity', 'index + 1', 'index % capacity', 'index - 1'], '(index + 1) % capacity', 'Modulo arithmetic wraps the index around.', 'Hard', 45),

    # Trees
    ('TREES', 'MCQ', 'What is the topmost node of a tree called?', ['Leaf', 'Root', 'Branch', 'Head'], 'Root', 'The root is the top node.', 'Easy', 20),
    ('TREES', 'MCQ', 'Nodes with no children are called?', ['Internal nodes', 'Roots', 'Leaves', 'Stems'], 'Leaves', 'Leaf nodes have no children.', 'Easy', 20),
    ('TREES', 'MCQ', 'In a Binary Search Tree, where are smaller values placed relative to a node?', ['Right child', 'Left child', 'Parent', 'Sibling'], 'Left child', 'Smaller values go left, larger go right.', 'Easy', 20),
    ('TREES', 'MCQ', 'What is the height of a tree with a single node?', ['0', '1', '-1', 'Undefined'], '0', 'Height is usually defined as the number of edges on the longest path from root to leaf.', 'Medium', 30),
    ('TREES', 'MCQ', 'Which traversal visits left child, root, right child?', ['Preorder', 'Inorder', 'Postorder', 'Level-order'], 'Inorder', 'Inorder is left-root-right.', 'Medium', 30),
    ('TREES', 'MCQ', 'What is the time complexity of searching in a perfectly balanced BST?', ['O(1)', 'O(N)', 'O(log N)', 'O(N log N)'], 'O(log N)', 'Height of balanced BST is log N.', 'Hard', 45),
    ('TREES', 'MCQ', 'Which property must an AVL tree maintain?', ['All leaves at same level', 'Max 2 children', 'Height difference of subtrees is at most 1', 'Root is the max value'], 'Height difference of subtrees is at most 1', 'AVL condition ensures balance.', 'Hard', 45),
    ('TREES', 'MCQ', 'How many edges are in a tree with N nodes?', ['N', 'N-1', 'N+1', 'log N'], 'N-1', 'A tree with N nodes has exactly N-1 edges.', 'Medium', 30),

    # Graphs
    ('GRAPHS', 'MCQ', 'What are the two main components of a graph?', ['Nodes and Leaves', 'Vertices and Edges', 'Roots and Branches', 'Data and Pointers'], 'Vertices and Edges', 'Graphs consist of V and E.', 'Easy', 20),
    ('GRAPHS', 'MCQ', 'In an undirected graph, an edge between A and B means?', ['A points to B', 'B points to A', 'A is connected to B bidirectionally', 'A and B are identical'], 'A is connected to B bidirectionally', 'Undirected means the connection goes both ways.', 'Easy', 20),
    ('GRAPHS', 'MCQ', 'What is a graph with no cycles called?', ['Cyclic Graph', 'Acyclic Graph', 'Complete Graph', 'Dense Graph'], 'Acyclic Graph', 'Acyclic means no cycles.', 'Easy', 20),
    ('GRAPHS', 'MCQ', 'Which data structure is often used to represent a dense graph?', ['Adjacency List', 'Adjacency Matrix', 'Binary Tree', 'Hash Map'], 'Adjacency Matrix', 'Matrix is space efficient for dense graphs.', 'Medium', 30),
    ('GRAPHS', 'MCQ', 'What is the degree of a vertex in an undirected graph?', ['Number of edges connected to it', 'Its value', 'Distance from root', 'Number of cycles'], 'Number of edges connected to it', 'Degree = number of incident edges.', 'Medium', 30),
    ('GRAPHS', 'MCQ', 'Which algorithm finds the shortest path in an unweighted graph?', ['DFS', 'BFS', 'Dijkstra', 'Kruskal'], 'BFS', 'BFS visits level by level, ensuring shortest path by edges.', 'Hard', 45),
    ('GRAPHS', 'MCQ', 'A graph where every vertex is connected to every other vertex is called?', ['Directed', 'Acyclic', 'Bipartite', 'Complete'], 'Complete', 'A complete graph has all possible edges.', 'Medium', 30),
    ('GRAPHS', 'MCQ', 'What is a topological sort?', ['Sorting vertices alphabetically', 'Linear ordering of vertices in a DAG', 'Finding the shortest path', 'Detecting a cycle'], 'Linear ordering of vertices in a DAG', 'It orders nodes such that for every directed edge u->v, u comes before v.', 'Hard', 45)
]

q_str = "    questions_data = [\n"
for q in questions:
    q_str += f'        ("{q[0]}", "{q[1]}", "{q[2]}", {q[3]}, "{q[4]}", "{q[5]}", "{q[6]}", {q[7]}),\n'
q_str += "    ]\n"

new_content = re.sub(r'    questions_data = \[.*?    \]\n', q_str, seed_content, flags=re.DOTALL)

with open(seed_path, "w") as f:
    f.write(new_content)
print("Updated seed_data.py")
