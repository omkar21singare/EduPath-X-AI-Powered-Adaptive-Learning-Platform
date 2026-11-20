import json
from app.database.session import SessionLocal
from app.models.models import Question, Concept, ContentSource

DSA_QUESTIONS_50 = [
    # Sorting
    ("SORTING", "MCQ", "What is the worst-case time complexity of QuickSort?", ["O(N log N)", "O(N^2)", "O(N)", "O(log N)"], "O(N^2)", "QuickSort degrades to O(N^2) with poor pivot choices.", "Medium", 40),
    ("SORTING", "MCQ", "Which sorting algorithm is guaranteed to have O(N log N) worst-case time and is stable?", ["MergeSort", "QuickSort", "HeapSort", "SelectionSort"], "MergeSort", "MergeSort is always O(N log N) and stable.", "Medium", 45),
    ("SORTING", "MCQ", "What is the best-case time complexity of standard Bubble Sort with an early exit flag?", ["O(1)", "O(N)", "O(N log N)", "O(N^2)"], "O(N)", "When the array is already sorted, a single pass takes O(N).", "Easy", 25),
    ("SORTING", "MCQ", "In-place HeapSort requires how much auxiliary memory?", ["O(1)", "O(log N)", "O(N)", "O(N log N)"], "O(1)", "HeapSort sorts in-place using the array itself.", "Hard", 45),
    ("SORTING", "MCQ", "Counting sort runs in O(N + K) where K represents what?", ["Depth of recursion", "Range of input values", "Number of swaps", "Memory block size"], "Range of input values", "K is the maximum value minus minimum value.", "Hard", 50),

    # Binary Search
    ("BINARY_SEARCH", "MCQ", "Binary search requires which precondition on the underlying sequence?", ["Must be stored as a linked list", "Must be sorted", "Must have even length", "Must only contain unique values"], "Must be sorted", "Binary search relies on monotonic ordering.", "Easy", 20),
    ("BINARY_SEARCH", "MCQ", "What is the maximum number of comparisons for binary search on 1024 elements?", ["10", "11", "512", "1024"], "11", "ceil(log2(1024)) + 1 = 11 comparisons at most.", "Medium", 35),
    ("BINARY_SEARCH", "MCQ", "How can integer overflow be prevented when calculating mid = (low + high) // 2?", ["mid = low + (high - low) // 2", "mid = high - low // 2", "mid = (high * low) // 2", "mid = high // 2 + low"], "mid = low + (high - low) // 2", "Prevents (low + high) exceeding maximum integer bounds.", "Medium", 30),
    ("BINARY_SEARCH", "MCQ", "Binary search can be applied to find the square root of a number N within precision eps in time:", ["O(N)", "O(log(N/eps))", "O(sqrt(N))", "O(1)"], "O(log(N/eps))", "Bisection on continuous function takes logarithmic steps.", "Hard", 50),
    ("BINARY_SEARCH", "MCQ", "What does lower_bound in C++ STL return?", ["First element >= target", "First element > target", "First element == target", "Last element <= target"], "First element >= target", "lower_bound finds the first position where value >= target.", "Hard", 45),

    # Hash Tables
    ("HASH_TABLES", "MCQ", "What is the average time complexity of insertion and search in a Hash Table?", ["O(1)", "O(log N)", "O(N)", "O(N log N)"], "O(1)", "Hash tables offer constant time average operations.", "Easy", 20),
    ("HASH_TABLES", "MCQ", "Which collision resolution technique stores all colliding keys in a linked list at the bucket?", ["Linear Probing", "Quadratic Probing", "Chaining", "Double Hashing"], "Chaining", "Separate chaining keeps a list per bucket.", "Easy", 25),
    ("HASH_TABLES", "MCQ", "What happens to hash table performance as the load factor approaches 1.0 in open addressing?", ["Performance improves", "Clusters form and lookups degrade to O(N)", "Memory decreases to zero", "Collisions vanish"], "Clusters form and lookups degrade to O(N)", "Clustering severely degrades probe sequences.", "Medium", 40),
    ("HASH_TABLES", "MCQ", "Which hash function property is essential to minimize collisions across arbitrary datasets?", ["Uniform distribution", "Monotonicity", "Reversibility", "Linearity"], "Uniform distribution", "Uniform spreading across slots prevents hotspot buckets.", "Medium", 35),
    ("HASH_TABLES", "MCQ", "What is the expected complexity of finding a duplicate in an array of size N using a HashSet?", ["O(N^2)", "O(N)", "O(N log N)", "O(1)"], "O(N)", "Checking membership O(1) for N items totals O(N).", "Medium", 30),

    # BFS & DFS
    ("BFS", "MCQ", "Breadth First Search explores nodes using which supporting data structure?", ["Stack", "Queue", "Priority Queue", "Disjoint Set"], "Queue", "BFS uses a FIFO queue to traverse level by level.", "Easy", 20),
    ("BFS", "MCQ", "In an unweighted graph, the shortest path between two vertices is found using:", ["DFS", "BFS", "Topological Sort", "Prim's Algorithm"], "BFS", "BFS finds the shortest edge-count path.", "Easy", 25),
    ("BFS", "MCQ", "What is the space complexity of BFS on a tree with branching factor b and depth d?", ["O(d)", "O(b * d)", "O(b^d)", "O(1)"], "O(b^d)", "The queue must hold all nodes at the current frontier level.", "Hard", 50),
    ("DFS", "MCQ", "Depth First Search naturally aligns with which data structure or mechanism?", ["Queue", "Call Stack / Recursion", "Min-Heap", "Ring Buffer"], "Call Stack / Recursion", "DFS traverses deep branches using recursion or a LIFO stack.", "Easy", 20),
    ("DFS", "MCQ", "Which DFS edge type in a directed graph indicates the presence of a cycle?", ["Tree edge", "Forward edge", "Back edge", "Cross edge"], "Back edge", "A back edge points to an ancestor in the active DFS path.", "Hard", 45),
    ("DFS", "MCQ", "What is the time complexity of DFS on a graph with V vertices and E edges?", ["O(V + E)", "O(V * E)", "O(V^2)", "O(E log V)"], "O(V + E)", "DFS visits each vertex and edge once.", "Medium", 30),

    # Dijkstra & Shortest Paths
    ("DIJKSTRA", "MCQ", "Dijkstra's Algorithm cannot correctly handle which of the following?", ["Dense graphs", "Negative edge weights", "Directed cycles", "Disconnected components"], "Negative edge weights", "Greedy choice assumption fails when edges can reduce cost negatively.", "Medium", 35),
    ("DIJKSTRA", "MCQ", "When implemented with a Binary Min-Heap, the time complexity of Dijkstra's algorithm is:", ["O(V^2)", "O((V + E) log V)", "O(E + V)", "O(V * E)"], "O((V + E) log V)", "Heap operations take log V for each vertex and edge relaxation.", "Hard", 45),
    ("DIJKSTRA", "MCQ", "What algorithm should be used instead of Dijkstra when edges have negative weights without negative cycles?", ["Floyd-Warshall only", "Bellman-Ford", "BFS", "Kruskal's"], "Bellman-Ford", "Bellman-Ford relaxes all edges V-1 times and detects negative cycles.", "Medium", 40),
    ("SHORTEST_PATHS", "MCQ", "Floyd-Warshall algorithm computes what kind of shortest paths?", ["Single Source Shortest Path", "All-Pairs Shortest Path", "Minimum Spanning Tree", "Maximum Flow"], "All-Pairs Shortest Path", "Floyd-Warshall calculates shortest distances between all pairs in O(V^3).", "Medium", 35),
    ("SHORTEST_PATHS", "MCQ", "What is the time complexity of the Floyd-Warshall algorithm?", ["O(V^2)", "O(V^3)", "O(V * E)", "O(E log V)"], "O(V^3)", "Triple nested loops iterate over all intermediate vertices.", "Medium", 30),

    # Dynamic Programming
    ("DYNAMIC_PROG", "MCQ", "What two key characteristics determine if a problem can be solved using Dynamic Programming?", ["Greedy choice & divide-and-conquer", "Optimal substructure & overlapping subproblems", "Recursion & hashing", "Monotonicity & acyclicity"], "Optimal substructure & overlapping subproblems", "DP caches overlapping subproblems with optimal sub-solutions.", "Easy", 25),
    ("DYNAMIC_PROG", "MCQ", "Top-down DP with caching is formally called what?", ["Tabulation", "Memoization", "Backtracking", "Branch and Bound"], "Memoization", "Top-down utilizes a memo table to remember solved subproblems.", "Easy", 20),
    ("DYNAMIC_PROG", "MCQ", "What is the space complexity of computing the Nth Fibonacci number with basic memoization?", ["O(1)", "O(N)", "O(2^N)", "O(log N)"], "O(N)", "The call stack and table require O(N) memory.", "Medium", 30),
    ("DYNAMIC_PROG", "MCQ", "What is the recurrence relation for the 0/1 Knapsack Problem for item i and capacity w?", ["dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w - wt[i]])", "dp[i][w] = dp[i-1][w] + val[i]", "dp[i][w] = min(dp[i-1][w], dp[i][w - wt[i]])", "dp[i][w] = val[i] * wt[i]"], "dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w - wt[i]])", "Choice between excluding item i or including item i.", "Hard", 55),
    ("DYNAMIC_PROG", "MCQ", "The Longest Common Subsequence (LCS) of strings of lengths M and N runs in time:", ["O(M + N)", "O(M * N)", "O(2^(M+N))", "O(M log N)"], "O(M * N)", "2D DP matrix has dimensions (M+1) x (N+1).", "Medium", 40),

    # Heaps & Priority Queues
    ("HEAPS", "MCQ", "In a zero-indexed array implementation of a binary heap, what is the index of the left child of node i?", ["2*i", "2*i + 1", "2*i + 2", "i // 2"], "2*i + 1", "Zero-indexed left child is at 2*i + 1.", "Easy", 20),
    ("HEAPS", "MCQ", "What is the time complexity to build a binary heap from an unsorted array of N elements?", ["O(N log N)", "O(N)", "O(log N)", "O(N^2)"], "O(N)", "Bottom-up build_heap runs in linear O(N) time.", "Hard", 45),
    ("HEAPS", "MCQ", "Extracting the minimum element from a Min-Heap of size N takes what time complexity?", ["O(1)", "O(log N)", "O(N)", "O(N log N)"], "O(log N)", "Restoring heap invariant via sift_down takes O(log N).", "Easy", 25),
    ("HEAPS", "MCQ", "What property does a Max-Heap satisfy for every node i other than the root?", ["A[parent(i)] >= A[i]", "A[parent(i)] <= A[i]", "A[left(i)] > A[right(i)]", "A[i] == A[parent(i)]"], "A[parent(i)] >= A[i]", "Parent values are always greater than or equal to child values.", "Easy", 20),

    # AVL Trees
    ("AVL_TREES", "MCQ", "What is the maximum allowed balance factor in an AVL tree?", ["0", "1", "2", "Unlimited"], "1", "Balance factor must be -1, 0, or +1.", "Easy", 25),
    ("AVL_TREES", "MCQ", "Which rotation resolves a Left-Right (LR) imbalance in an AVL tree?", ["Single Left Rotation", "Single Right Rotation", "Left Rotation on left child, then Right Rotation on root", "Right Rotation on root, then Left on right child"], "Left Rotation on left child, then Right Rotation on root", "Double rotation resolves zigzag LR imbalance.", "Hard", 50),
    ("AVL_TREES", "MCQ", "What is the worst-case time complexity of insertion into an AVL tree with N nodes?", ["O(1)", "O(log N)", "O(N)", "O(N log N)"], "O(log N)", "AVL tree height remains strictly bounded by 1.44 * log2(N).", "Medium", 35),

    # Algorithmic Thinking & Complexity
    ("ALG_THINK", "MCQ", "What does the Master Theorem solve?", ["Recurrences of form T(N) = a*T(N/b) + f(N)", "Linear equations", "Shortest path graphs", "Matrix inversions"], "Recurrences of form T(N) = a*T(N/b) + f(N)", "Master Theorem provides closed-form asymptotic bounds for divide-and-conquer recurrences.", "Medium", 35),
    ("COMP_ANALYSIS", "MCQ", "If an algorithm runs in 3N^2 + 500N + 1000 operations, what is its Big-O time complexity?", ["O(N)", "O(N^2)", "O(500N)", "O(1000)"], "O(N^2)", "Big-O drops lower-order terms and constant coefficients.", "Easy", 15),
    ("COMP_ANALYSIS", "MCQ", "Which complexity class grows the fastest as N increases?", ["O(N log N)", "O(N^3)", "O(2^N)", "O(N!)"], "O(N!)", "Factorial O(N!) outgrows exponential O(2^N).", "Easy", 20),

    # Additional Array & String Problems
    ("ARRAYS", "MCQ", "What is the sliding window technique optimal for?", ["Searching in binary trees", "Finding subarrays or substrings satisfying specific bounds", "Inverting a matrix", "Sorting non-comparable items"], "Finding subarrays or substrings satisfying specific bounds", "Sliding window maintains state over contiguous intervals in linear time.", "Medium", 35),
    ("ARRAYS", "MCQ", "Kadane's algorithm finds what in an array of numbers?", ["Maximum product of two numbers", "Maximum subarray sum", "Median value", "Longest increasing subsequence"], "Maximum subarray sum", "Kadane's runs in O(N) time and O(1) space.", "Medium", 30),
    ("ARRAYS", "MCQ", "What is the prefix sum array used to compute in O(1) time?", ["Subarray sum queries", "Subarray multiplication queries", "Subarray reversals", "Subarray sorting"], "Subarray sum queries", "Sum(L..R) = Prefix[R] - Prefix[L-1].", "Easy", 20),

    # Linked List Advanced
    ("LINKED_LIST", "MCQ", "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) detects cycles using pointers moving at speeds:", ["1 and 2 steps per iteration", "1 and 3 steps per iteration", "2 and 4 steps per iteration", "Random steps"], "1 and 2 steps per iteration", "Slow pointer advances 1, fast pointer advances 2.", "Medium", 30),
    ("LINKED_LIST", "MCQ", "What is the space complexity of Floyd's Tortoise and Hare algorithm?", ["O(N)", "O(log N)", "O(1)", "O(N^2)"], "O(1)", "Requires only two pointer variables.", "Easy", 20),
    ("LINKED_LIST", "MCQ", "Reversing a singly linked list in-place requires how many pointers?", ["1", "2", "3", "N"], "3", "Typically prev, curr, and next_node.", "Medium", 25),

    # Stacks & Queues Advanced
    ("STACKS", "MCQ", "A monotonic stack is most effective for solving which category of problems?", ["Next Greater Element / Previous Smaller Element", "Breadth first traversal", "Dijkstra relaxation", "Longest common subsequence"], "Next Greater Element / Previous Smaller Element", "Maintains elements in strict order to find nearest extremes in O(N).", "Hard", 45),
    ("STACKS", "MCQ", "How can a queue be implemented using two stacks?", ["Pushing to Stack1, popping from Stack2 (refilling Stack2 from Stack1 when empty)", "Pushing to both simultaneously", "Interleaving elements alternately", "It cannot be done"], "Pushing to Stack1, popping from Stack2 (refilling Stack2 from Stack1 when empty)", "Amortized O(1) push and pop.", "Medium", 35)
]

def seed_50_questions():
    db = SessionLocal()
    concepts = {c.code: c for c in db.query(Concept).all()}
    mit_src = db.query(ContentSource).first()

    added = 0
    for code, qtype, text, opts, ans, expl, diff, est_t in DSA_QUESTIONS_50:
        if code not in concepts:
            continue
        c = concepts[code]
        # Check if already present by text
        exists = db.query(Question).filter(Question.question_text == text).first()
        if not exists:
            q = Question(
                concept_id=c.id,
                question_type=qtype,
                question_text=text,
                options=opts,
                correct_answer=ans,
                explanation=expl,
                difficulty=diff,
                estimated_time_seconds=est_t,
                verified_status="VERIFIED",
                source_id=mit_src.id if mit_src else None,
                calibrated_slip=0.08 if diff == "Easy" else (0.12 if diff == "Medium" else 0.16),
                calibrated_guess=0.25 if diff == "Easy" else (0.20 if diff == "Medium" else 0.15),
                calibrated_difficulty=-0.5 if diff == "Easy" else (0.1 if diff == "Medium" else 0.8)
            )
            db.add(q)
            added += 1

    db.commit()
    print(f"Added {added} new DSA curriculum questions across all modules.")
    db.close()

if __name__ == "__main__":
    seed_50_questions()
