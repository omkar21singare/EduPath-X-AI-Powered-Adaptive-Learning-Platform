import os
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models.models import (
    User, LearnerProfile, LearningGoal, Concept, ConceptPrerequisite, ContentSource,
    LearningMaterial, Question, KnowledgeState, SimulationProfile
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database(db: Session):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Check if already seeded
    if db.query(User).filter(User.email == "aarav@edupathx.edu").first():
        print("Database already seeded.")
        return

    print("Seeding EduPath-X Database...")

    # 1. Content Sources Registry
    sources = [
        ContentSource(
            source_name="MIT OpenCourseWare 6.006",
            official_url="https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/",
            license="CC BY-NC-SA 4.0",
            retrieved_at="2025-01-15",
            description="MIT 6.006 Introduction to Algorithms course notes and syllabus.",
            status="VERIFIED"
        ),
        ContentSource(
            source_name="OpenStax Computer Science",
            official_url="https://openstax.org/",
            license="CC BY 4.0",
            retrieved_at="2025-01-20",
            description="Open educational textbook resources for computer science and data structures.",
            status="VERIFIED"
        ),
        ContentSource(
            source_name="MDN Web Docs - Data Structures",
            official_url="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures",
            license="CC-BY-SA 2.5",
            retrieved_at="2025-02-01",
            description="Mozilla Developer Network guide to core computer science data structures.",
            status="VERIFIED"
        )
    ]
    for s in sources:
        db.add(s)
    db.commit()

    mit_src = db.query(ContentSource).filter(ContentSource.source_name.like("%MIT%")).first()
    openstax_src = db.query(ContentSource).filter(ContentSource.source_name.like("%OpenStax%")).first()

    # 2. DSA Curriculum Concepts (18 concepts)
    concept_definitions = [
        ("ALG_THINK", "Algorithmic Thinking", "Fundamentals of problem decomposition, step-by-step procedure design, and correctness invariants.", "Basic", "Easy", 1),
        ("COMP_ANALYSIS", "Complexity Analysis", "Big-O, Big-Theta, and Big-Omega notations for asymptotic time and space complexity evaluation.", "Basic", "Easy", 2),
        ("ARRAYS", "Arrays & Strings", "Contiguous memory allocation, random indexing O(1), dynamic arrays, and string manipulation techniques.", "Linear", "Easy", 3),
        ("LINKED_LIST", "Linked Lists", "Singly and doubly linked lists, pointer manipulation, node insertion/deletion, and list traversal.", "Linear", "Easy", 4),
        ("STACKS", "Stacks & Queues", "LIFO and FIFO linear abstract data types, call stacks, queue buffers, and array/linked-list implementations.", "Linear", "Easy", 5),
        ("HASH_TABLES", "Hash Tables", "Hash functions, collision resolution (chaining vs open addressing), load factor, and average O(1) operations.", "Linear", "Medium", 6),
        ("SORTING", "Sorting Algorithms", "Comparison and non-comparison sorting: Quicksort, Mergesort, Insertion sort, and lower bounds.", "Algorithms", "Medium", 7),
        ("BINARY_SEARCH", "Binary Search", "Divide-and-conquer search on sorted arrays in O(log N) time, search space reduction.", "Algorithms", "Medium", 8),
        ("TREES", "Binary Search Trees", "Hierarchical tree data structures, BST property, insertion, deletion, and inorder/preorder/postorder traversals.", "Trees", "Medium", 9),
        ("HEAPS", "Binary Heaps", "Priority queue data structure, max-heap and min-heap properties, heapify down/up in O(log N).", "Trees", "Medium", 10),
        ("AVL_TREES", "AVL Trees", "Self-balancing binary search trees, height invariants, single and double rotations.", "Trees", "Hard", 11),
        ("GRAPHS", "Graph Representations", "Adjacency matrix vs adjacency list, directed/undirected graphs, vertex degree, and connectivity.", "Graphs", "Medium", 12),
        ("BFS", "Breadth-First Search (BFS)", "Level-order queue-based graph traversal, unweighted shortest path discovery.", "Graphs", "Medium", 13),
        ("DFS", "Depth-First Search (DFS)", "Recursive and stack-based graph exploration, cycle detection, topological sorting.", "Graphs", "Medium", 14),
        ("SHORTEST_PATHS", "Shortest Path Fundamentals", "Path relaxation, weighted edges, single-source shortest path formulation.", "Graphs", "Hard", 15),
        ("DIJKSTRA", "Dijkstra's Algorithm", "Greedy single-source shortest path algorithm on non-negative weighted graphs using min-heaps.", "Graphs", "Hard", 16),
        ("DYNAMIC_PROG", "Dynamic Programming", "Optimal substructure, overlapping subproblems, memoization (top-down) vs tabulation (bottom-up).", "Advanced", "Hard", 17),
    ]

    concept_objs = {}
    for code, title, desc, cat, diff, order in concept_definitions:
        c = Concept(
            code=code,
            title=title,
            description=desc,
            category=cat,
            difficulty_level=diff,
            display_order=order
        )
        db.add(c)
        concept_objs[code] = c

    db.commit()
    # Refresh IDs
    for code in concept_objs:
        db.refresh(concept_objs[code])

    # 3. Prerequisites Graph DAG
    prerequisite_pairs = [
        ("COMP_ANALYSIS", "ALG_THINK", 0.70),
        ("ARRAYS", "COMP_ANALYSIS", 0.70),
        ("LINKED_LIST", "ARRAYS", 0.70),
        ("STACKS", "LINKED_LIST", 0.70),
        ("HASH_TABLES", "ARRAYS", 0.70),
        ("SORTING", "COMP_ANALYSIS", 0.70),
        ("BINARY_SEARCH", "ARRAYS", 0.70),
        ("BINARY_SEARCH", "SORTING", 0.70),
        ("TREES", "LINKED_LIST", 0.70),
        ("HEAPS", "TREES", 0.70),
        ("AVL_TREES", "TREES", 0.75),
        ("GRAPHS", "LINKED_LIST", 0.70),
        ("GRAPHS", "HASH_TABLES", 0.70),
        ("BFS", "GRAPHS", 0.70),
        ("BFS", "STACKS", 0.70),
        ("DFS", "GRAPHS", 0.70),
        ("DFS", "TREES", 0.70),
        ("SHORTEST_PATHS", "BFS", 0.75),
        ("SHORTEST_PATHS", "DFS", 0.75),
        ("DIJKSTRA", "SHORTEST_PATHS", 0.80),
        ("DIJKSTRA", "HEAPS", 0.80),
        ("DYNAMIC_PROG", "DFS", 0.75),
        ("DYNAMIC_PROG", "COMP_ANALYSIS", 0.75),
    ]

    for target_code, prereq_code, min_m in prerequisite_pairs:
        cp = ConceptPrerequisite(
            concept_id=concept_objs[target_code].id,
            prerequisite_id=concept_objs[prereq_code].id,
            minimum_mastery=min_m
        )
        db.add(cp)
    db.commit()

    # 4. Real Learning Material for Concepts
    materials_data = [
        (
            "ARRAYS",
            "Arrays & Dynamic Arrays Fundamentals",
            ["Understand contiguous memory indexing", "Analyze O(1) random access vs O(N) linear search", "Implement dynamic array resizing"],
            "An array is a collection of elements stored at contiguous memory locations. Because memory addresses are sequential, element index `i` can be directly calculated as `Base_Address + i * Element_Size`, providing instantaneous O(1) random access.",
            "arr = [10, 20, 30, 40, 50]\nprint(arr[2])  # Output: 30 (O(1) time)",
            "Visualizing contiguous RAM addresses: [0x100: 10] -> [0x104: 20] -> [0x108: 30]",
            {"time_access": "O(1)", "time_search": "O(N)", "time_insert": "O(N)", "space": "O(N)"},
            "Accessing the 5th element in a 1,000,000 item array takes the exact same time as accessing the 1st element.",
            mit_src.id
        ),
        (
            "TREES",
            "Binary Search Trees (BST) Fundamentals",
            ["Define the BST invariant property", "Perform Inorder, Preorder, and Postorder traversals", "Analyze search and insertion complexity"],
            "A Binary Search Tree (BST) is a node-based binary tree data structure which has the BST invariant: for any node N, all values in N's left subtree are strictly less than N.val, and all values in N's right subtree are strictly greater than N.val.",
            "class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef inorder(root):\n    if root:\n        inorder(root.left)\n        print(root.val)\n        inorder(root.right)",
            "Root (8) -> Left (3) -> Right (10). Inorder traversal yields sorted order [3, 8, 10].",
            {"time_search_avg": "O(log N)", "time_search_worst": "O(N)", "space": "O(N)"},
            "Given BST with root 8, searching for 3: 3 < 8, so move to left child. Match found in 2 steps.",
            mit_src.id
        ),
        (
            "DFS",
            "Depth-First Search (DFS) Graph Traversal",
            ["Understand call stack recursion in graph traversal", "Distinguish tree DFS from graph DFS (visited sets)", "Compute arrival and departure order"],
            "Depth-First Search (DFS) explores as far as possible along each branch before backtracking. It uses a LIFO call stack or explicit stack, along with a `visited` hash set to prevent infinite loops in cyclic graphs.",
            "def dfs(graph, node, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(node)\n    print(node)\n    for neighbor in graph[node]:\n        if neighbor not in visited:\n            dfs(graph, neighbor, visited)",
            "Graph: A-B, A-C, B-D. DFS path starting at A: A -> B -> D -> (backtrack) -> C.",
            {"time": "O(V + E)", "space": "O(V)"},
            "Traversing a social network graph to find all connected friends in a single path.",
            mit_src.id
        ),
        (
            "DIJKSTRA",
            "Dijkstra's Single-Source Shortest Path Algorithm",
            ["Understand greedy shortest path edge relaxation", "Utilize a min-heap priority queue for optimal extraction", "Analyze O((V + E) log V) complexity"],
            "Dijkstra's algorithm finds the shortest path from a starting source vertex to all other vertices in a non-negative weighted graph. It maintains a tentative distance array and greedily selects the unvisited node with the smallest tentative distance using a min-heap.",
            "import heapq\n\ndef dijkstra(graph, start):\n    distances = {node: float('inf') for node in graph}\n    distances[start] = 0\n    pq = [(0, start)]\n    while pq:\n        curr_dist, u = heapq.heappop(pq)\n        if curr_dist > distances[u]: continue\n        for v, weight in graph[u]:\n            if distances[u] + weight < distances[v]:\n                distances[v] = distances[u] + weight\n                heapq.heappush(pq, (distances[v], v))\n    return distances",
            "Start A (dist 0). Edge A->B (wt 4), A->C (wt 2). Extract C. Relax C->B (wt 1), new B dist = 3 < 4.",
            {"time": "O((V + E) log V)", "space": "O(V)"},
            "GPS Navigation routing: finding the fastest driving route from Boston to New York.",
            mit_src.id
        )
    ]

    for code, title, objs, expl, code_ex, vis_ex, comp_info, worked_ex, src_id in materials_data:
        lm = LearningMaterial(
            concept_id=concept_objs[code].id,
            title=title,
            learning_objectives=objs,
            explanation=expl,
            code_example=code_ex,
            visual_explanation=vis_ex,
            complexity_info=comp_info,
            worked_example=worked_ex,
            content_version="1.0.0",
            source_id=src_id
        )
        db.add(lm)
    db.commit()

    # 5. Real Question Bank (covering various types and difficulty levels)
    questions_data = [
        ("ARRAYS", "MCQ", "What is the time complexity of accessing an element by index in an array?", ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], "O(1)", "Accessing by index is direct memory access.", "Easy", 30),
        ("ARRAYS", "MCQ", "Which of the following is true about dynamic arrays?", ['Size is fixed', 'Resizes automatically', 'Only stores integers', 'Slower access than linked list'], "Resizes automatically", "Dynamic arrays resize when they hit capacity.", "Easy", 30),
        ("ARRAYS", "MCQ", "What is the worst-case time complexity for inserting an element at the beginning of an array?", ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], "O(N)", "All subsequent elements must be shifted.", "Medium", 45),
        ("ARRAYS", "MCQ", "In a 0-indexed array of size N, what is the index of the last element?", ['N', 'N-1', 'N+1', '1'], "N-1", "Indices range from 0 to N-1.", "Easy", 20),
        ("ARRAYS", "MCQ", "What happens if you try to access an index out of the array bounds?", ['Returns 0', 'Returns null', 'Throws an error/exception', 'Wraps around'], "Throws an error/exception", "Out of bounds access causes an exception in most languages.", "Easy", 20),
        ("ARRAYS", "MCQ", "Which operation is generally faster in an array compared to a linked list?", ['Insertion at beginning', 'Deletion at beginning', 'Random access', 'Resizing'], "Random access", "Arrays have O(1) random access.", "Medium", 30),
        ("ARRAYS", "MCQ", "How much memory does an array of 10 32-bit integers require?", ['10 bytes', '32 bytes', '40 bytes', '320 bytes'], "40 bytes", "10 integers * 4 bytes/integer = 40 bytes.", "Medium", 45),
        ("ARRAYS", "MCQ", "What is a common use case for an array?", ['Implementing a graph', 'Storing elements of varying types safely', 'When size is unknown and changes constantly', 'Storing a fixed-size collection of items of the same type'], "Storing a fixed-size collection of items of the same type", "Arrays are best for homogeneous, fixed-size data.", "Medium", 30),
        ("LINKED_LIST", "MCQ", "What is the time complexity to insert a node at the head of a linked list?", ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], "O(1)", "Head insertion only requires updating a few pointers.", "Easy", 30),
        ("LINKED_LIST", "MCQ", "What does each node in a singly linked list contain?", ['Value only', 'Value and next pointer', 'Value, next and prev pointers', 'Next pointer only'], "Value and next pointer", "Singly linked lists have data and a pointer to the next node.", "Easy", 30),
        ("LINKED_LIST", "MCQ", "How do you find the length of a singly linked list?", ['Return the size property', 'Traverse the list and count nodes', 'Multiply node size by capacity', 'It is not possible'], "Traverse the list and count nodes", "Without a cached size variable, traversal O(N) is required.", "Medium", 45),
        ("LINKED_LIST", "MCQ", "What is a disadvantage of a linked list compared to an array?", ['Slower insertion at head', 'Fixed size', 'No random access', 'Requires contiguous memory'], "No random access", "You must traverse from the head to access the i-th element.", "Medium", 30),
        ("LINKED_LIST", "MCQ", "In a doubly linked list, what does the prev pointer of the head node point to?", ['The tail node', 'The second node', 'Null', 'Itself'], "Null", "The head node has no previous node.", "Easy", 20),
        ("LINKED_LIST", "MCQ", "Which problem can occur if you lose the reference to the head of a linked list?", ['Memory leak', 'Stack overflow', 'Index out of bounds', 'Nothing'], "Memory leak", "Without the head, the list nodes cannot be accessed and may leak in unmanaged languages.", "Medium", 30),
        ("LINKED_LIST", "MCQ", "To delete a node X from a singly linked list (given only X), what is a common trick?", ['Copy data from X.next to X and delete X.next', 'Traverse from head', 'Set X to null', 'It is impossible'], "Copy data from X.next to X and delete X.next", "This works if X is not the tail.", "Hard", 60),
        ("LINKED_LIST", "MCQ", "What is the time complexity to search for a value in a linked list?", ['O(1)', 'O(N)', 'O(log N)', 'O(N^2)'], "O(N)", "You may have to check every node.", "Easy", 20),
        ("STACKS", "MCQ", "Which principle does a stack follow?", ['FIFO', 'LIFO', 'Random Access', 'Priority'], "LIFO", "Last-In, First-Out.", "Easy", 20),
        ("STACKS", "MCQ", "What is the operation to add an item to a stack called?", ['Push', 'Pop', 'Enqueue', 'Insert'], "Push", "Push adds an item.", "Easy", 20),
        ("STACKS", "MCQ", "What is the operation to remove an item from a stack called?", ['Push', 'Pop', 'Dequeue', 'Delete'], "Pop", "Pop removes the top item.", "Easy", 20),
        ("STACKS", "MCQ", "Which data structure can be used to easily reverse a string?", ['Queue', 'Linked List', 'Stack', 'Tree'], "Stack", "Pushing all characters and popping them reverses the order.", "Medium", 30),
        ("STACKS", "MCQ", "In a function call stack, what happens when a function returns?", ['Its frame is pushed', 'Its frame is popped', 'The stack is cleared', 'Nothing'], "Its frame is popped", "The stack frame is removed upon return.", "Medium", 30),
        ("STACKS", "MCQ", "What exception is thrown when popping from an empty stack?", ['Stack Overflow', 'Stack Underflow', 'Index Out of Bounds', 'Null Pointer'], "Stack Underflow", "Trying to pop an empty stack is an underflow.", "Medium", 30),
        ("STACKS", "MCQ", "Which problem is traditionally solved using a stack?", ['Breadth First Search', 'Shortest Path', 'Balanced Parentheses', 'Sorting'], "Balanced Parentheses", "Stacks are perfect for matching brackets.", "Hard", 45),
        ("STACKS", "MCQ", "If a stack is implemented using an array, what is the time complexity of push?", ['O(1) amortized', 'O(N)', 'O(log N)', 'O(N^2)'], "O(1) amortized", "If the array resizes, it is O(1) amortized.", "Hard", 45),
        ("STACKS", "MCQ", "Which principle does a queue follow?", ['FIFO', 'LIFO', 'Random', 'Priority'], "FIFO", "First-In, First-Out.", "Easy", 20),
        ("STACKS", "MCQ", "What is the operation to add an item to a queue?", ['Push', 'Pop', 'Enqueue', 'Dequeue'], "Enqueue", "Enqueue adds to the back.", "Easy", 20),
        ("STACKS", "MCQ", "Which algorithm uses a queue naturally?", ['Depth First Search', 'Breadth First Search', 'Binary Search', 'Quicksort'], "Breadth First Search", "BFS processes nodes level by level using a queue.", "Medium", 30),
        ("STACKS", "MCQ", "In a circular queue, how is the next position calculated?", ['(index + 1) % capacity', 'index + 1', 'index % capacity', 'index - 1'], "(index + 1) % capacity", "Modulo arithmetic wraps the index around.", "Hard", 45),
        ("TREES", "MCQ", "What is the topmost node of a tree called?", ['Leaf', 'Root', 'Branch', 'Head'], "Root", "The root is the top node.", "Easy", 20),
        ("TREES", "MCQ", "Nodes with no children are called?", ['Internal nodes', 'Roots', 'Leaves', 'Stems'], "Leaves", "Leaf nodes have no children.", "Easy", 20),
        ("TREES", "MCQ", "In a Binary Search Tree, where are smaller values placed relative to a node?", ['Right child', 'Left child', 'Parent', 'Sibling'], "Left child", "Smaller values go left, larger go right.", "Easy", 20),
        ("TREES", "MCQ", "What is the height of a tree with a single node?", ['0', '1', '-1', 'Undefined'], "0", "Height is usually defined as the number of edges on the longest path from root to leaf.", "Medium", 30),
        ("TREES", "MCQ", "Which traversal visits left child, root, right child?", ['Preorder', 'Inorder', 'Postorder', 'Level-order'], "Inorder", "Inorder is left-root-right.", "Medium", 30),
        ("TREES", "MCQ", "What is the time complexity of searching in a perfectly balanced BST?", ['O(1)', 'O(N)', 'O(log N)', 'O(N log N)'], "O(log N)", "Height of balanced BST is log N.", "Hard", 45),
        ("TREES", "MCQ", "Which property must an AVL tree maintain?", ['All leaves at same level', 'Max 2 children', 'Height difference of subtrees is at most 1', 'Root is the max value'], "Height difference of subtrees is at most 1", "AVL condition ensures balance.", "Hard", 45),
        ("TREES", "MCQ", "How many edges are in a tree with N nodes?", ['N', 'N-1', 'N+1', 'log N'], "N-1", "A tree with N nodes has exactly N-1 edges.", "Medium", 30),
        ("GRAPHS", "MCQ", "What are the two main components of a graph?", ['Nodes and Leaves', 'Vertices and Edges', 'Roots and Branches', 'Data and Pointers'], "Vertices and Edges", "Graphs consist of V and E.", "Easy", 20),
        ("GRAPHS", "MCQ", "In an undirected graph, an edge between A and B means?", ['A points to B', 'B points to A', 'A is connected to B bidirectionally', 'A and B are identical'], "A is connected to B bidirectionally", "Undirected means the connection goes both ways.", "Easy", 20),
        ("GRAPHS", "MCQ", "What is a graph with no cycles called?", ['Cyclic Graph', 'Acyclic Graph', 'Complete Graph', 'Dense Graph'], "Acyclic Graph", "Acyclic means no cycles.", "Easy", 20),
        ("GRAPHS", "MCQ", "Which data structure is often used to represent a dense graph?", ['Adjacency List', 'Adjacency Matrix', 'Binary Tree', 'Hash Map'], "Adjacency Matrix", "Matrix is space efficient for dense graphs.", "Medium", 30),
        ("GRAPHS", "MCQ", "What is the degree of a vertex in an undirected graph?", ['Number of edges connected to it', 'Its value', 'Distance from root', 'Number of cycles'], "Number of edges connected to it", "Degree = number of incident edges.", "Medium", 30),
        ("GRAPHS", "MCQ", "Which algorithm finds the shortest path in an unweighted graph?", ['DFS', 'BFS', 'Dijkstra', 'Kruskal'], "BFS", "BFS visits level by level, ensuring shortest path by edges.", "Hard", 45),
        ("GRAPHS", "MCQ", "A graph where every vertex is connected to every other vertex is called?", ['Directed', 'Acyclic', 'Bipartite', 'Complete'], "Complete", "A complete graph has all possible edges.", "Medium", 30),
        ("GRAPHS", "MCQ", "What is a topological sort?", ['Sorting vertices alphabetically', 'Linear ordering of vertices in a DAG', 'Finding the shortest path', 'Detecting a cycle'], "Linear ordering of vertices in a DAG", "It orders nodes such that for every directed edge u->v, u comes before v.", "Hard", 45),
    ]

    for code, qtype, text, opts, ans, expl, diff, est_t in questions_data:
        q = Question(
            concept_id=concept_objs[code].id,
            question_type=qtype,
            question_text=text,
            options=opts,
            correct_answer=ans,
            explanation=expl,
            difficulty=diff,
            estimated_time_seconds=est_t,
            verified_status="VERIFIED",
            source_id=mit_src.id
        )
        db.add(q)
    db.commit()

    demo_user = User(
        email="aarav@edupathx.edu",
        password_hash="fakehash",
        full_name="Aarav Sharma",
        role="student",
        is_demo=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    learner = LearnerProfile(
        user_id=demo_user.id,
        class_name="B.Tech CSE",
        semester="Semester 4",
        streak_count=7,
        last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
        target_date="30th June 2025"
    )
    db.add(learner)
    db.commit()
    db.refresh(learner)

    goal = LearningGoal(
        learner_id=learner.id,
        goal_name="Crack Placement Coding Round",
        target_mastery=0.85,
        progress_percentage=0.68,
        target_date="30th June 2025",
        status="ACTIVE"
    )
    db.add(goal)

    # Populate initial realistic knowledge states for Aarav Sharma
    # E.g. Strong in Arrays (0.91), Linked List (0.80), Stacks (0.90), Weak in Trees (0.54), DFS (0.37)
    initial_masteries = {
        "ALG_THINK": 0.95,
        "COMP_ANALYSIS": 0.88,
        "ARRAYS": 0.91,
        "LINKED_LIST": 0.80,
        "STACKS": 0.90,
        "HASH_TABLES": 0.75,
        "SORTING": 0.82,
        "BINARY_SEARCH": 0.78,
        "TREES": 0.54,
        "HEAPS": 0.40,
        "AVL_TREES": 0.20,
        "GRAPHS": 0.45,
        "BFS": 0.40,
        "DFS": 0.37,
        "SHORTEST_PATHS": 0.15,
        "DIJKSTRA": 0.10,
        "DYNAMIC_PROG": 0.10,
    }

    for code, mastery in initial_masteries.items():
        ks = KnowledgeState(
            learner_id=learner.id,
            concept_id=concept_objs[code].id,
            mastery_probability=mastery,
            total_attempts=12 if mastery > 0.7 else 5,
            correct_attempts=10 if mastery > 0.7 else 2
        )
        db.add(ks)

    db.commit()
    print("EduPath-X Database Seeded Successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    seed_database(db)
    db.close()
