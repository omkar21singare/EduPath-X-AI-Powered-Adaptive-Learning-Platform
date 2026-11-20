export interface QuickCheck {
  id: string;
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface ExternalReference {
  name: string;
  source_type: 'MIT OpenCourseWare' | 'GeeksforGeeks' | 'OpenStax' | 'Official Documentation';
  url: string;
  description: string;
}

export interface Lesson {
  id: string;
  title: string;
  learning_objectives: string[];
  explanation: string;
  code_example?: {
    language: string;
    code: string;
    explanation: string;
    output?: string;
  };
  complexity?: {
    time: string;
    space: string;
    rationale: string;
  };
  common_mistakes: string[];
  key_takeaways: string[];
  quick_check?: QuickCheck;
  external_references: ExternalReference[];
}

export interface LearningModule {
  id: string;
  title: string;
  description: string;
  lessons: Lesson[];
}

export interface ConceptContent {
  concept_code: string;
  concept_title: string;
  overview: string;
  has_practice: boolean;
  practice_notice?: string;
  modules: LearningModule[];
}

export const LEARNING_CONTENT_REGISTRY: Record<string, ConceptContent> = {
  ARRAYS: {
    concept_code: 'ARRAYS',
    concept_title: 'Arrays & Strings',
    overview: 'Arrays are the most fundamental linear data structure, storing elements in contiguous memory blocks. This layout enables instant O(1) random indexing, while requiring O(N) linear shifts for intermediate insertions and deletions.',
    has_practice: true,
    modules: [
      {
        id: 'arrays-mod-1',
        title: 'Module 1: Memory Architecture & Representation',
        description: 'Understand contiguous physical memory allocation and why index arithmetic delivers instant random access.',
        lessons: [
          {
            id: 'arrays-m1-l1',
            title: 'Contiguous Memory & Random Access Mechanics',
            learning_objectives: [
              'Understand physical contiguous storage layout in RAM',
              'Derive the mathematical offset formula for array indexing',
              'Explain why random access executes in strictly O(1) time'
            ],
            explanation: `An array is a fixed-sequence data structure stored in unbroken, consecutive memory addresses. When a program allocates an array of size N, the operating system assigns a single contiguous block of physical RAM.\n\nBecause every element occupies an identical number of bytes (S), any element at index i can be located instantaneously without scanning preceding elements. The computer calculates the exact byte address using direct arithmetic:\n\nAddress(i) = Base_Address + (i * S)\n\nBecause this calculation involves only one multiplication and one addition on CPU hardware registers, accessing any element—whether arr[0], arr[49], or arr[100000]—requires exactly the same number of clock cycles: O(1) constant time.`,
            code_example: {
              language: 'python',
              code: `# Direct O(1) Random Access Demonstration\nscores = [88, 92, 79, 95, 84]\n\n# Accessing index 0 (Base Address + 0 * 8 bytes)\nfirst_student = scores[0]\n\n# Accessing index 3 (Base Address + 3 * 8 bytes)\ntop_student = scores[3]\n\nprint(f"Index 0: {first_student}, Index 3: {top_student}")`,
              explanation: 'Line 5 & 8 calculate the memory offset directly from the array base address in constant O(1) time without inspecting intervening elements.',
              output: 'Index 0: 88, Index 3: 95'
            },
            complexity: {
              time: 'O(1)',
              space: 'O(N)',
              rationale: 'Time is O(1) because accessing by index requires only a single multiplication and addition to compute the physical memory address. Space is O(N) because N contiguous memory cells are reserved in physical RAM.'
            },
            common_mistakes: [
              'Assuming arrays can grow infinitely without memory reallocation.',
              'Confusing element values with zero-based indices, leading to Off-By-One errors at array boundaries.',
              'Attempting to access index len(arr) which triggers IndexError in Python.'
            ],
            key_takeaways: [
              'Arrays store elements contiguously in physical hardware memory.',
              'Random access operates in O(1) time via base address + index * element_size offset arithmetic.',
              'Contiguous storage provides superior CPU cache locality compared to pointer-based structures.'
            ],
            quick_check: {
              id: 'qc-arr-1',
              question: 'Why is random access in an array O(1) rather than O(N)?',
              options: [
                'Because the CPU sequentially searches every memory cell at light speed.',
                'Because the element physical address is calculated directly using Base + (index * size) arithmetic.',
                'Because arrays store pointers to linked structures in hardware registers.',
                'Because arrays can only contain numbers less than 256.'
              ],
              correct_index: 1,
              explanation: 'Because memory addresses are contiguous and element sizes are identical, index offset math directly yields the memory address in a single CPU instruction.'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-2-data-structures-and-dynamic-arrays/',
                description: 'Lecture 2: Data Structures and Dynamic Arrays (Prof. Erik Demaine).'
              },
              {
                name: 'GeeksforGeeks Array Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/array-data-structure-guide/',
                description: 'Comprehensive guide covering memory allocation, indexing, and array algorithms.'
              }
            ]
          },
          {
            id: 'arrays-m1-l2',
            title: 'Static vs. Dynamic Arrays & Amortized Doubling',
            learning_objectives: [
              'Differentiate between fixed-size static arrays and resizable dynamic arrays',
              'Analyze the geometric doubling reallocation mechanism',
              'Formally explain why dynamic array append is amortized O(1)'
            ],
            explanation: `Static arrays (like standard C/Java arrays) have fixed size chosen at creation. If the capacity is exhausted, no further elements can be inserted without manually creating a larger array.\n\nDynamic arrays (such as Python lists or C++ std::vector) automatically resize. When an insertion exceeds current capacity, the runtime:\n1. Allocates a new contiguous block with double the previous capacity (2x geometric growth).\n2. Copies all N existing elements into the new block.\n3. Frees the old memory block.\n4. Inserts the new element.\n\nWhile copying N elements costs O(N) on a reallocation step, geometric doubling ensures that resizes occur exponentially infrequently. Summing the copy costs across N appends yields a total cost bounded by 2N, making the average cost per append exactly O(1) amortized.`,
            code_example: {
              language: 'python',
              code: `import sys\n\n# Inspecting Python dynamic array capacity growth\ndata = []\nprint(f"Init: len={len(data)}, byte_size={sys.getsizeof(data)}")\n\nfor i in range(10):\n    data.append(i)\n    print(f"Added {i}: len={len(data)}, byte_size={sys.getsizeof(data)}")`,
              explanation: 'Observe that byte_size increases in discrete jumps rather than every insertion, proving that Python over-allocates capacity using geometric growth.',
              output: 'Init: len=0, byte_size=56\nAdded 0: len=1, byte_size=88\nAdded 4: len=5, byte_size=120'
            },
            complexity: {
              time: 'Amortized O(1) append, O(N) worst-case resize',
              space: 'O(N) with capacity over-allocation',
              rationale: 'A resize costs O(N) to copy existing items, but after doubling, N new appends happen at O(1) before the next resize. Total cost divided by operations gives constant amortized time.'
            },
            common_mistakes: [
              'Assuming dynamic arrays grow by 1 element on each insert (an arithmetic growth strategy that leads to catastrophic O(N^2) total copy time).',
              'Forgetting that inserting at the beginning of a dynamic array is always O(N) because all items must shift right.'
            ],
            key_takeaways: [
              'Geometric doubling (2x or 1.5x) guarantees amortized O(1) append performance.',
              'Resizing incurs temporary O(N) latency spikes and requires spare memory overhead.',
              'Pre-allocating array capacity eliminates resize latency in high-performance pipelines.'
            ],
            quick_check: {
              id: 'qc-arr-2',
              question: 'Why does doubling capacity yield amortized O(1) time instead of O(N)?',
              options: [
                'Because memory copying in modern OS kernels takes zero CPU cycles.',
                'Because the expensive O(N) copy happens so rarely that the average cost per append is constant.',
                'Because dynamic arrays avoid physical memory allocation.',
                'Because only the first 2 elements are ever copied.'
              ],
              correct_index: 1,
              explanation: 'N appends share the cost of a single doubling event. Dividing O(N) copy operations across N appends yields O(1) amortized cost per operation.'
            },
            external_references: [
              {
                name: 'OpenStax Computer Science Foundations',
                source_type: 'OpenStax',
                url: 'https://openstax.org/details/books/computer-science',
                description: 'Section on Dynamic Arrays and Amortized Analysis.'
              }
            ]
          }
        ]
      },
      {
        id: 'arrays-mod-2',
        title: 'Module 2: Core Array Operations, Shifting & Traversal',
        description: 'Analyze time complexities of searching, inserting, and deleting elements in array structures.',
        lessons: [
          {
            id: 'arrays-m2-l1',
            title: 'Searching & Traversal Complexity',
            learning_objectives: [
              'Implement linear search on unsorted arrays',
              'Understand the prerequisites and logarithmic efficiency of binary search',
              'Compare iteration patterns and cache behavior'
            ],
            explanation: `Searching through an unsorted array requires checking each item one by one from index 0 to N-1. In the worst case (element absent or at the final index), linear search inspects all N items, giving O(N) time complexity.\n\nWhen an array is sorted, we can exploit random access via Binary Search. By probing the midpoint index mid = (low + high) // 2, we discard half the remaining search space with each comparison. Halving the problem space repeatedly gives O(log N) time.\n\nBinary search is only possible on arrays because index arithmetic allows jumping to the middle element in O(1) time—a property that linked lists lack.`,
            code_example: {
              language: 'python',
              code: `def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nsorted_arr = [11, 23, 34, 45, 56, 67, 78, 89]\nprint("Found at index:", binary_search(sorted_arr, 56))`,
              explanation: 'At each iteration, mid is accessed in O(1) time and half the array is eliminated, terminating in at most ceil(log2(N)) steps.',
              output: 'Found at index: 4'
            },
            complexity: {
              time: 'O(log N) for binary search on sorted array; O(N) for linear search',
              space: 'O(1) auxiliary iterative space',
              rationale: 'Repeatedly halving an array of length N reaches 1 element after log2(N) divisions.'
            },
            common_mistakes: [
              'Attempting binary search on an unsorted array, returning incorrect indices.',
              'Potential integer overflow when computing mid = (low + high) // 2 in languages with fixed integer widths (mitigated in C/Java via low + (high - low) // 2).'
            ],
            key_takeaways: [
              'Linear search runs in O(N) time on arbitrary arrays.',
              'Binary search runs in O(log N) time but strictly requires sorted data.',
              'Array random access is what enables binary search to inspect the midpoint in O(1) time.'
            ],
            quick_check: {
              id: 'qc-arr-3',
              question: 'What is the maximum number of comparisons binary search needs on an array of 1,024 sorted elements?',
              options: ['1,024', '512', '10 or 11', '1'],
              correct_index: 2,
              explanation: 'log2(1024) = 10. Binary search inspects at most 10 or 11 elements to find any target or confirm its absence.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Binary Search',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/binary-search/',
                description: 'Complete tutorial on iterative and recursive binary search implementations.'
              }
            ]
          },
          {
            id: 'arrays-m2-l2',
            title: 'Insertion, Deletion & The Shifting Overhead',
            learning_objectives: [
              'Trace memory movements when inserting or deleting elements',
              'Understand why middle/beginning operations require O(N) time',
              'Contrast end operations O(1) with head operations O(N)'
            ],
            explanation: `Because arrays must maintain strictly contiguous storage without memory gaps, inserting or deleting elements at arbitrary positions requires shifting elements:\n\n1. Insertion at index k: All elements from index k to N-1 must be shifted one position to the right to create an empty cell. In the worst case (inserting at index 0), all N elements must be copied, costing O(N) time.\n2. Deletion at index k: After removing the element at index k, all subsequent elements from index k+1 to N-1 must be shifted one position to the left to close the gap. Deleting from index 0 costs O(N) time.\n\nOnly operations at the end of the array (append / pop) avoid element shifting, executing in O(1) amortized time.`,
            code_example: {
              language: 'python',
              code: `nums = [10, 20, 30, 40, 50]\n\n# Insertion at index 1 forces shifting [20, 30, 40, 50] to the right\nnums.insert(1, 99)\nprint("After insert at index 1:", nums)\n\n# Deletion at index 1 forces shifting remaining elements left\nremoved = nums.pop(1)\nprint("After pop at index 1:", nums)`,
              explanation: 'Line 4 shifts 4 elements to the right. Line 8 shifts 4 elements back to the left, taking O(N) operations proportional to array size.',
              output: 'After insert at index 1: [10, 99, 20, 30, 40, 50]\nAfter pop at index 1: [10, 20, 30, 40, 50]'
            },
            complexity: {
              time: 'O(N) for insertion/deletion at index 0 or middle; O(1) at end',
              space: 'O(1) in-place auxiliary space',
              rationale: 'To maintain contiguous physical addresses without holes, every element to the right of the target index must be moved by 1 position.'
            },
            common_mistakes: [
              'Using array insert(0, item) inside a loop, turning an otherwise linear algorithm into O(N^2).',
              'Using array pop(0) in a queue implementation instead of collections.deque.'
            ],
            key_takeaways: [
              'Contiguity is a double-edged sword: gives O(1) access, but imposes O(N) shifting on insertions and deletions.',
              'Prepend and middle insertions cost O(N). End append costs O(1) amortized.',
              'When frequent insertions at both ends are needed, choose a Deque or Linked List instead.'
            ],
            quick_check: {
              id: 'qc-arr-4',
              question: 'Why does deleting the first element of an array of size N take O(N) time?',
              options: [
                'Because the CPU must recalculate the base address of RAM.',
                'Because the remaining N-1 elements must each be shifted left by one cell to maintain contiguity.',
                'Because Python requires garbage collection on every element.',
                'Because deleting from memory always requires re-allocating the entire OS stack.'
              ],
              correct_index: 1,
              explanation: 'An array cannot contain unallocated holes in the middle. Removing index 0 requires copying index 1 to 0, 2 to 1, ..., N-1 to N-2.'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Lecture Notes',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture notes on array shifting and sequences.'
              }
            ]
          }
        ]
      },
      {
        id: 'arrays-mod-3',
        title: 'Module 3: Essential Array Algorithmic Patterns',
        description: 'Master practical interview and production patterns: Two-Pointers, Sliding Window, and Prefix Sums.',
        lessons: [
          {
            id: 'arrays-m3-l1',
            title: 'Two-Pointer Technique & Sliding Window',
            learning_objectives: [
              'Apply the opposite-end Two-Pointer pattern to sorted arrays',
              'Apply the Sliding Window pattern to contiguous subsegment problems',
              'Reduce brute-force O(N^2) searches to linear O(N) time'
            ],
            explanation: `When working with arrays, brute-force checks often examine all pairs or subarrays in O(N^2) time. Two essential patterns leverage array random access to achieve O(N) linear time:\n\n1. Two Pointers (Opposite Ends): On a sorted array, placing one pointer at left=0 and another at right=N-1 allows converging toward the solution. If arr[left] + arr[right] is too small, increment left; if too large, decrement right. Each step eliminates a candidate in O(1) time.\n2. Sliding Window: Maintains a contiguous range [start, end]. By expanding end and contracting start based on window conditions, all valid subarrays are inspected in a single pass of 2N steps: O(N) total.`,
            code_example: {
              language: 'python',
              code: `def two_sum_sorted(arr, target):\n    left, right = 0, len(arr) - 1\n    while left < right:\n        current_sum = arr[left] + arr[right]\n        if current_sum == target:\n            return (left, right)\n        elif current_sum < target:\n            left += 1\n        else:\n            right -= 1\n    return None\n\nprint("Pair indices:", two_sum_sorted([2, 7, 11, 15, 22], 18))`,
              explanation: 'Because the array is sorted, the pointers move deterministically inward. Total operations never exceed N, achieving optimal O(N) time and O(1) space.',
              output: 'Pair indices: (1, 2)'
            },
            complexity: {
              time: 'O(N)',
              space: 'O(1)',
              rationale: 'Left pointer increments at most N times and right pointer decrements at most N times. Total iterations are bounded by N.'
            },
            common_mistakes: [
              'Applying the two-pointer sorted technique to an unsorted array without sorting first.',
              'Failing to handle duplicate values when counting unique pairs.'
            ],
            key_takeaways: [
              'Two Pointers reduces O(N^2) pair matching to O(N) on sorted arrays.',
              'Sliding Window dynamically maintains running state across subarrays in linear time.',
              'Both patterns leverage constant-time array indexing to achieve optimal algorithmic bounds.'
            ],
            quick_check: {
              id: 'qc-arr-5',
              question: 'In the Two-Pointer sorted pair search, what should you do if arr[left] + arr[right] is less than target?',
              options: [
                'Decrement right to reduce the sum.',
                'Increment left to test a larger value.',
                'Reset both pointers to the center.',
                'Terminate because no solution exists.'
              ],
              correct_index: 1,
              explanation: 'Because the array is sorted in ascending order, incrementing left increases the sum toward the target.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Two Pointers Technique',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/two-pointers-technique/',
                description: 'Comprehensive problem set and walkthrough of two-pointer paradigms.'
              }
            ]
          }
        ]
      }
    ]
  },

  LINKED_LIST: {
    concept_code: 'LINKED_LIST',
    concept_title: 'Linked Lists',
    overview: 'A linked list is a linear collection of data nodes linked together through memory pointers or object references. Unlike arrays, nodes are not stored contiguously, trading random access for constant O(1) boundary insertions.',
    has_practice: true,
    modules: [
      {
        id: 'll-mod-1',
        title: 'Module 1: Pointer Architecture & Node Anatomy',
        description: 'Examine nodes, memory references, and the fundamental dichotomy between Singly and Doubly Linked Lists.',
        lessons: [
          {
            id: 'll-m1-l1',
            title: 'Node Structure & Non-Contiguous Allocation',
            learning_objectives: [
              'Understand the node abstraction: data field and next pointer',
              'Contrast heap-allocated pointer chains with contiguous array memory',
              'Trace pointer reassignment during list operations'
            ],
            explanation: `A linked list consists of independent node objects dynamically allocated on the heap. Each node encapsulates two primary elements:\n1. Data: The value stored in this element.\n2. Next: A memory address (pointer or reference) directing to the successor node in the sequence.\n\nThe list maintains a reference to the first node, termed the Head. The last node has its Next reference set to None / Null, indicating the boundary of the list.\n\nBecause nodes are scattered throughout RAM, elements cannot be accessed via address math. To reach node k, one must begin at the head and hop through k consecutive pointers—giving O(N) sequential access.`,
            code_example: {
              language: 'python',
              code: `class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n# Constructing a 3-node chain: 10 -> 20 -> 30 -> None\nnode3 = ListNode(30)\nnode2 = ListNode(20, node3)\nhead = ListNode(10, node2)\n\n# Traversing the list sequentially\ncurr = head\nwhile curr:\n    print(f"Node value: {curr.val}")\n    curr = curr.next`,
              explanation: 'Each node points to the next node in the heap. Traversal hops pointer-to-pointer until curr becomes None.',
              output: 'Node value: 10\nNode value: 20\nNode value: 30'
            },
            complexity: {
              time: 'O(N) for traversal / access; O(1) for head insertion',
              space: 'O(N) total storage with pointer overhead per node',
              rationale: 'Reaching element k requires traversing k pointers from the head. Each node requires additional memory for the pointer reference.'
            },
            common_mistakes: [
              'Losing the head reference during updates, causing the entire list to be orphan-collected by garbage collection.',
              'Dereferencing curr.next without verifying that curr is not None (Null Pointer Exception).'
            ],
            key_takeaways: [
              'Nodes are individually allocated across physical memory and linked via references.',
              'Random access is impossible: all lookups are sequential O(N).',
              'Boundary insertions do not require element shifting, enabling O(1) time.'
            ],
            quick_check: {
              id: 'qc-ll-1',
              question: 'Why does finding the k-th element in a singly linked list take O(k) time?',
              options: [
                'Because the CPU must rehash the linked list addresses.',
                'Because nodes are not contiguous, requiring the program to follow k consecutive next pointers from head.',
                'Because linked lists store values in reverse lexicographical order.',
                'Because garbage collection runs before each memory lookup.'
              ],
              correct_index: 1,
              explanation: 'Without contiguous memory, pointer chasing from the head node is the only way to locate downstream nodes.'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Lecture 3',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture 3: Linked Data Structures and Pointer-Based Sets.'
              },
              {
                name: 'GeeksforGeeks Linked List Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/data-structures/linked-list/',
                description: 'Complete guide on singly, doubly, and circular linked lists.'
              }
            ]
          },
          {
            id: 'll-m1-l2',
            title: 'Singly vs. Doubly Linked Lists',
            learning_objectives: [
              'Compare single pointer vs two-way pointer architectures',
              'Understand the prev pointer in Doubly Linked Lists (DLL)',
              'Evaluate memory overhead vs operational flexibility'
            ],
            explanation: `In a Singly Linked List, traversal is strictly unidirectional (head to tail). Deleting a known node requires access to its predecessor, which takes O(N) time to locate if not already held.\n\nA Doubly Linked List (DLL) equips every node with two pointers: Next and Prev. This enables:\n1. Bidirectional traversal (head-to-tail or tail-to-head).\n2. Instant O(1) deletion of any node when given a direct reference to that node, because node.prev.next and node.next.prev can be rewritten directly.\n\nThe tradeoff is memory: DLL nodes consume roughly 33-50% more pointer overhead per element.`,
            code_example: {
              language: 'python',
              code: `class DoublyNode:\n    def __init__(self, val=0, prev=None, next=None):\n        self.val = val\n        self.prev = prev\n        self.next = next\n\n# Instant O(1) deletion of a node given its reference\ndef delete_node(node):\n    if node.prev:\n        node.prev.next = node.next\n    if node.next:\n        node.next.prev = node.prev\n    node.prev = None\n    node.next = None`,
              explanation: 'Because node has a direct prev pointer, its predecessor can be linked to its successor in O(1) steps without traversing from the head.',
              output: 'Node detached in O(1) time.'
            },
            complexity: {
              time: 'O(1) deletion of a known node in DLL; O(N) in singly linked list',
              space: '2 pointer references per node (prev and next)',
              rationale: 'Doubly linked lists store both forward and backward connections, allowing immediate neighbor rewiring.'
            },
            common_mistakes: [
              'Forgetting to update node.next.prev when rewiring node.prev.next.',
              'Failing to handle boundary deletions when node is head (node.prev is None) or tail (node.next is None).'
            ],
            key_takeaways: [
              'Singly linked lists save memory with one pointer per node.',
              'Doubly linked lists enable two-way traversal and O(1) node deletion given a pointer.',
              'LRU Caches (Least Recently Used) standardly use Doubly Linked Lists paired with Hash Maps.'
            ],
            quick_check: {
              id: 'qc-ll-2',
              question: 'Given only a pointer to node X in the middle of a singly linked list, why is standard deletion tricky without copying values?',
              options: [
                'Because the CPU prohibits memory deallocation.',
                'Because you cannot access the node immediately preceding X without traversing from head.',
                'Because singly linked lists do not support deletion.',
                'Because node values are immutable in RAM.'
              ],
              correct_index: 1,
              explanation: 'In a singly linked list, there is no prev pointer. To bypass X, you must update the predecessor next pointer.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Doubly Linked List',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/doubly-linked-list/',
                description: 'Implementation and operations on Doubly Linked Lists.'
              }
            ]
          }
        ]
      },
      {
        id: 'll-mod-2',
        title: 'Module 2: Core Operations & Array Comparison',
        description: 'Implement insertion and deletion algorithms and critically contrast linked lists against arrays.',
        lessons: [
          {
            id: 'll-m2-l1',
            title: 'Insertion and Deletion Mechanics',
            learning_objectives: [
              'Implement O(1) head insertion',
              'Implement O(N) middle insertion and deletion',
              'Use dummy/sentinel nodes to simplify edge cases'
            ],
            explanation: `Manipulating linked lists requires careful pointer discipline. Inserting a new node at the head is a constant O(1) operation:\n1. Set new_node.next = head\n2. Set head = new_node\n\nNo elements are shifted in memory! Similarly, removing the head node takes O(1) by setting head = head.next.\n\nHowever, inserting or deleting at arbitrary index k requires traversing k-1 nodes to locate the predecessor: an O(k) = O(N) operation. Sentinel (Dummy) nodes—a temporary node placed before head—are an essential engineering technique that eliminates special-casing for empty lists or head modifications.`,
            code_example: {
              language: 'python',
              code: `class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef insert_at_head(head, val):\n    new_node = ListNode(val)\n    new_node.next = head\n    return new_node  # New head in O(1) time\n\nhead = None\nhead = insert_at_head(head, 30)\nhead = insert_at_head(head, 20)\nhead = insert_at_head(head, 10)\n\n# Output chain: 10 -> 20 -> 30\nvals = []\ncurr = head\nwhile curr:\n    vals.append(str(curr.val))\n    curr = curr.next\nprint(" -> ".join(vals))`,
              explanation: 'insert_at_head updates two pointers in constant O(1) time regardless of how many elements are already in the list.',
              output: '10 -> 20 -> 30'
            },
            complexity: {
              time: 'O(1) at head; O(N) at middle or arbitrary index',
              space: 'O(1) auxiliary space per insertion',
              rationale: 'Head insertion only reassigns pointer references. Middle insertion requires linear pointer chasing to find the predecessor.'
            },
            common_mistakes: [
              'Assigning head = new_node before setting new_node.next = head, permanently losing the rest of the list.',
              'Creating memory cycles by accidentally pointing a node back to one of its ancestors.'
            ],
            key_takeaways: [
              'Head insertion and head deletion are strictly O(1) without element shifting.',
              'Dummy head nodes eliminate null-check branching when deleting the first node.',
              'Always verify pointer order when re-linking nodes.'
            ],
            quick_check: {
              id: 'qc-ll-3',
              question: 'What is the primary advantage of using a dummy (sentinel) head node when writing linked list algorithms?',
              options: [
                'It reduces the time complexity of traversal from O(N) to O(1).',
                'It avoids special-case if-statements when modifying or removing the first node of the list.',
                'It automatically sorts the elements in ascending order.',
                'It stores backup copies of all deleted nodes.'
              ],
              correct_index: 1,
              explanation: 'A sentinel node guarantees that every real node has a valid predecessor, unifying head operations with middle operations.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Linked List Insertion',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/insertion-in-linked-list/',
                description: 'Step-by-step illustrations of head, tail, and middle linked list insertions.'
              }
            ]
          }
        ]
      }
    ]
  },

  STACKS: {
    concept_code: 'STACKS',
    concept_title: 'Stacks & Queues',
    overview: 'Stacks (LIFO) and Queues (FIFO) are constrained linear data structures with strict access protocols. Stacks manage execution contexts and nested structures; Queues orchestrate sequential workflows and breadth-first traversals.',
    has_practice: true,
    modules: [
      {
        id: 'sq-mod-1',
        title: 'Module 1: The Stack (LIFO) Abstraction',
        description: 'Examine Last-In First-Out mechanics, constant-time operations, and structural applications.',
        lessons: [
          {
            id: 'sq-m1-l1',
            title: 'LIFO Principle & Core Operations',
            learning_objectives: [
              'Define the Last-In First-Out (LIFO) ordering principle',
              'Implement push, pop, peek, and is_empty in O(1) time',
              'Trace stack state during execution'
            ],
            explanation: `A Stack is an abstract data type where all insertions and deletions occur exclusively at one designated end, termed the Top. It strictly enforces the LIFO protocol: the element inserted most recently is always the first to be retrieved.\n\nCore Stack Operations:\n- push(item): Appends item onto the top of the stack — O(1) time.\n- pop(): Removes and returns the item currently on top — O(1) time.\n- peek() / top(): Inspects the top item without modifying the stack — O(1) time.\n- is_empty(): Returns true if the stack contains zero items — O(1) time.\n\nStacks can be implemented using either dynamic arrays (pushing/popping at the array end in amortized O(1)) or singly linked lists (inserting/removing at the head in O(1)).`,
            code_example: {
              language: 'python',
              code: `class Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)  # O(1) amortized\n\n    def pop(self):\n        if not self._items:\n            raise IndexError("Stack Underflow")\n        return self._items.pop()   # O(1) end pop\n\n    def peek(self):\n        return self._items[-1] if self._items else None\n\ns = Stack()\ns.push("A")\ns.push("B")\ns.push("C")\nprint("Top item:", s.peek())\nprint("Popped:", s.pop())\nprint("New Top:", s.peek())`,
              explanation: 'Item C was pushed last, so it is popped first. Access is strictly constrained to the top.',
              output: 'Top item: C\nPopped: C\nNew Top: B'
            },
            complexity: {
              time: 'O(1) for push, pop, peek, and is_empty',
              space: 'O(N) to store N items',
              rationale: 'Operations only manipulate the top boundary, requiring no shifting or traversal.'
            },
            common_mistakes: [
              'Popping from an empty stack, causing a Stack Underflow error.',
              'Attempting to access middle elements in a stack, which violates the LIFO encapsulation contract.'
            ],
            key_takeaways: [
              'Stacks enforce Last-In, First-Out (LIFO) discipline.',
              'All primary operations run in guaranteed O(1) constant time.',
              'Underlying storage can be a dynamic array or singly linked list.'
            ],
            quick_check: {
              id: 'qc-sq-1',
              question: 'If you push elements 10, 20, 30, and 40 onto an initially empty stack, what is the result of calling pop() twice?',
              options: [
                '10 followed by 20',
                '40 followed by 30',
                '40 followed by 10',
                '30 followed by 40'
              ],
              correct_index: 1,
              explanation: 'In LIFO order, the most recently added item (40) is popped first, followed by the next top item (30).'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture on Stacks, Queues, and Sequence Data Structures.'
              },
              {
                name: 'GeeksforGeeks Stack Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/stack-data-structure/',
                description: 'Comprehensive stack tutorials, operations, and interview problems.'
              }
            ]
          },
          {
            id: 'sq-m1-l2',
            title: 'Applications: Balanced Parentheses & Call Stacks',
            learning_objectives: [
              'Apply stacks to syntax checking and balanced delimiter matching',
              'Understand how operating systems use the call stack for recursive functions',
              'Trace call frames and recognize Stack Overflow conditions'
            ],
            explanation: `Stacks naturally model nested, hierarchical lifecycles because a nested context must finish before its enclosing outer context can complete.\n\nTwo quintessential applications:\n1. Balanced Parentheses: When reading characters, opening brackets ('(', '{', '[') are pushed onto the stack. When a closing bracket is encountered, the stack top is checked: if it matches the closing bracket type, it is popped. If the stack is empty or holds a mismatch, the string is invalid. At string end, the stack must be empty.\n2. Program Call Stack: Every time a function is invoked, the OS pushes an activation record (call frame containing parameters and local variables). When the function returns, its frame is popped. Infinite recursion exhausts allocated memory, triggering a Stack Overflow.`,
            code_example: {
              language: 'python',
              code: `def is_valid_parentheses(s: str) -> bool:\n    mapping = {')': '(', '}': '{', ']': '['}\n    stack = []\n    for char in s:\n        if char in mapping.values():\n            stack.append(char)\n        elif char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n    return len(stack) == 0\n\nprint("Valid:", is_valid_parentheses("{[()]}"))\nprint("Invalid:", is_valid_parentheses("{[(])}"))`,
              explanation: 'Matches the most recently opened delimiter against incoming closing delimiters in O(N) time using O(N) stack space.',
              output: 'Valid: True\nInvalid: False'
            },
            complexity: {
              time: 'O(N)',
              space: 'O(N)',
              rationale: 'Every character is pushed and popped at most once. Auxiliary stack space is at most N characters.'
            },
            common_mistakes: [
              'Checking that counts of open and closed brackets are equal without verifying matching order.',
              'Forgetting to check if the stack is completely empty after scanning the entire string.'
            ],
            key_takeaways: [
              'Stacks are the foundation of parsers, compilers, and nested expression evaluators.',
              'Call stacks maintain function execution state in all modern programming language runtimes.',
              'Balanced delimiter parsing runs in linear O(N) time with stack discipline.'
            ],
            quick_check: {
              id: 'qc-sq-2',
              question: 'Why does the string "([)]" fail bracket validation even though it has one pair of parentheses and one pair of brackets?',
              options: [
                'Because the string has an even number of characters.',
                'Because the closing parenthesis encounters an unmatched bracket on the top of the stack.',
                'Because brackets cannot contain parentheses in Python.',
                'Because the stack runs out of memory.'
              ],
              correct_index: 1,
              explanation: 'When ")" is seen, the top of the stack is "[", which does not match "(". LIFO requires inner brackets to close before outer ones.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Balanced Parentheses',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/',
                description: 'Classic stack parsing problem walkthrough and variations.'
              }
            ]
          }
        ]
      },
      {
        id: 'sq-mod-2',
        title: 'Module 2: The Queue (FIFO) Abstraction & Deques',
        description: 'Examine First-In First-Out mechanics, circular queue ring buffers, and double-ended queues.',
        lessons: [
          {
            id: 'sq-m2-l1',
            title: 'FIFO Principle & The Array Dequeue Trap',
            learning_objectives: [
              'Define the First-In First-Out (FIFO) ordering principle',
              'Explain why using standard array pop(0) results in catastrophic O(N) time',
              'Implement a true O(1) queue using collections.deque or circular buffers'
            ],
            explanation: `A Queue enforces First-In, First-Out (FIFO) ordering: the earliest element inserted is the first element removed (like people waiting in a line).\n\nCore Operations:\n- enqueue(item): Appends item to the rear of the queue.\n- dequeue(): Removes and returns the item at the front of the queue.\n\nThe Array Dequeue Trap: In Python, beginners often write queue.pop(0) on a standard list. Because a list is a contiguous array, deleting index 0 forces the runtime to shift all remaining N-1 elements left! This turns an algorithm performing N dequeues into an accidental O(N^2) bottleneck.\n\nTo achieve true O(1) operations, use collections.deque (a doubly linked block buffer) or a circular ring buffer with head and tail pointers.`,
            code_example: {
              language: 'python',
              code: `from collections import deque\n\n# Correct O(1) FIFO Queue Implementation\nqueue = deque()\n\n# Enqueue operations\nqueue.append("PrintJob_1")\nqueue.append("PrintJob_2")\nqueue.append("PrintJob_3")\n\n# Dequeue operations in O(1) time\nfirst_out = queue.popleft()\nprint(f"Processed: {first_out}")\nprint(f"Next in queue: {queue[0]}")`,
              explanation: 'collections.deque.popleft() runs in O(1) constant time without shifting array elements.',
              output: 'Processed: PrintJob_1\nNext in queue: PrintJob_2'
            },
            complexity: {
              time: 'O(1) for enqueue and dequeue when using deque or circular buffer',
              space: 'O(N) to hold N queue elements',
              rationale: 'Deque and circular buffers rewire boundary pointers or increment head indices modulo capacity without copying elements.'
            },
            common_mistakes: [
              'Using list.pop(0) in Python, creating an unintentional O(N) shifting cost per dequeue.',
              'Confusing LIFO (Stack) and FIFO (Queue) in graph search algorithms.'
            ],
            key_takeaways: [
              'Queues enforce First-In, First-Out (FIFO) processing order.',
              'Standard array pop(0) is an O(N) anti-pattern in high-throughput pipelines.',
              'Use collections.deque or circular arrays for genuine O(1) queue performance.'
            ],
            quick_check: {
              id: 'qc-sq-3',
              question: 'What is the time complexity of dequeuing N items sequentially from a Python standard list using list.pop(0)?',
              options: ['O(N)', 'O(N^2)', 'O(1)', 'O(log N)'],
              correct_index: 1,
              explanation: 'Each pop(0) on a standard list shifts the remaining elements, taking O(N) time. Doing this N times yields O(N^2) total time.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Queue Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/queue-data-structure/',
                description: 'Queue architecture, ring buffers, and deque implementations.'
              }
            ]
          }
        ]
      }
    ]
  },

  TREES: {
    concept_code: 'TREES',
    concept_title: 'Binary Search Trees & Trees',
    overview: 'Trees are non-linear, hierarchical data structures organized into nodes with parent-child relationships. Binary Search Trees (BST) maintain sorted order invariants, enabling logarithmic average-case search and insertion.',
    has_practice: true,
    modules: [
      {
        id: 'trees-mod-1',
        title: 'Module 1: Tree Terminology & The BST Invariant',
        description: 'Understand root, parent, child, height, and depth, and master the Binary Search Tree ordering invariant.',
        lessons: [
          {
            id: 'trees-m1-l1',
            title: 'Tree Terminology & Structural Anatomy',
            learning_objectives: [
              'Define root, edge, parent, child, leaf, height, and depth',
              'Differentiate general trees from binary trees',
              'Calculate maximum node capacity as a function of tree height'
            ],
            explanation: `A Tree is an acyclic, connected hierarchical graph with N nodes and exactly N-1 edges. Terminology:\n- Root: The unique top-level node with no parent.\n- Parent / Child: Directed relationship where a node references subordinate nodes.\n- Leaf: A terminal node with no children.\n- Depth of a node: The number of edges from the root to that node (root depth = 0).\n- Height of a tree: The length of the longest downward path from root to any leaf.\n\nA Binary Tree restricts every node to having at most two children: designated Left and Right. A full binary tree of height H contains at most 2^(H+1) - 1 nodes.`,
            code_example: {
              language: 'python',
              code: `class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n# Constructing a simple 3-node binary tree:\n#       10\n#      /  \\\n#     5    15\nroot = TreeNode(10)\nroot.left = TreeNode(5)\nroot.right = TreeNode(15)\n\nprint(f"Root: {root.val}, Left Child: {root.left.val}, Right Child: {root.right.val}")`,
              explanation: 'A TreeNode maintains values and references to left and right subtrees.',
              output: 'Root: 10, Left Child: 5, Right Child: 15'
            },
            complexity: {
              time: 'O(1) per node creation',
              space: 'O(N) for N total tree nodes',
              rationale: 'Nodes store data plus two child pointers.'
            },
            common_mistakes: [
              'Confusing tree height (distance from node down to deepest leaf) with node depth (distance from root down to node).',
              'Assuming all binary trees are automatically balanced.'
            ],
            key_takeaways: [
              'A tree with N nodes always contains exactly N-1 edges without cycles.',
              'Binary trees restrict each node to at most two children.',
              'Tree height dictates search efficiency in hierarchical data structures.'
            ],
            quick_check: {
              id: 'qc-tree-1',
              question: 'What is the maximum number of nodes in a binary tree of height 3 (where root depth is 0)?',
              options: ['7', '8', '15', '31'],
              correct_index: 2,
              explanation: '2^(3+1) - 1 = 2^4 - 1 = 15 nodes (levels 0, 1, 2, 3 hold 1 + 2 + 4 + 8 = 15).'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Lecture 5',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture 5: Binary Trees and Binary Search Trees.'
              },
              {
                name: 'GeeksforGeeks Tree Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/binary-tree-data-structure/',
                description: 'Comprehensive tutorials on binary trees and tree traversal algorithms.'
              }
            ]
          },
          {
            id: 'trees-m1-l2',
            title: 'The Binary Search Tree (BST) Ordering Invariant',
            learning_objectives: [
              'Formally state the BST ordering property',
              'Implement search and insertion in a BST',
              'Analyze the O(log N) average vs O(N) worst-case (skewed) complexity'
            ],
            explanation: `A Binary Search Tree (BST) is a binary tree satisfying the BST Invariant for every node X:\n- Every node in X's left subtree has a value strictly less than X.val.\n- Every node in X's right subtree has a value strictly greater than X.val.\n\nBecause of this invariant, searching for a key mirrors binary search: at each node, we compare key with curr.val. If key < curr.val, we go left; if key > curr.val, we go right. Each step discards an entire subtree!\n\nComplexity:\n- Balanced BST: Height is H = O(log N). Search, insert, and delete run in O(log N) time.\n- Degenerate (Skewed) BST: Inserting sorted numbers ([1, 2, 3, 4, 5]) degenerates the tree into a linked list with H = O(N). Search degrades to O(N) linear time. This motivates self-balancing trees (AVL, Red-Black).`,
            code_example: {
              language: 'python',
              code: `class BSTNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef bst_insert(root, val):\n    if not root:\n        return BSTNode(val)\n    if val < root.val:\n        root.left = bst_insert(root.left, val)\n    elif val > root.val:\n        root.right = bst_insert(root.right, val)\n    return root\n\ndef bst_search(root, target):\n    if not root or root.val == target:\n        return root\n    if target < root.val:\n        return bst_search(root.left, target)\n    return bst_search(root.right, target)\n\nroot = None\nfor x in [50, 30, 70, 20, 40, 60, 80]:\n    root = bst_insert(root, x)\n\nfound = bst_search(root, 40)\nprint("Search 40 found node with value:", found.val if found else "Not Found")`,
              explanation: 'bst_search discards half the remaining nodes at each level, achieving logarithmic average time.',
              output: 'Search 40 found node with value: 40'
            },
            complexity: {
              time: 'Average: O(log N); Worst-case (skewed): O(N)',
              space: 'O(H) recursion stack space where H is tree height',
              rationale: 'Search path length equals the height of the tree. A balanced tree has height log2(N); a completely skewed tree has height N.'
            },
            common_mistakes: [
              'Assuming checking that left < root and right > root for immediately adjacent children validates a BST (all descendants in the left subtree must be less than root).',
              'Inserting pre-sorted data into an unbalancing BST without shuffling or rebalancing.'
            ],
            key_takeaways: [
              'BST invariant: Left Subtree < Node < Right Subtree.',
              'Balanced BST operations run in O(log N) time; skewed BST degrades to O(N).',
              'Inorder traversal of a valid BST always produces keys in strictly sorted ascending order.'
            ],
            quick_check: {
              id: 'qc-tree-2',
              question: 'If you insert elements [10, 20, 30, 40, 50] in that exact order into an empty BST, what is the shape of the resulting tree and search complexity?',
              options: [
                'Perfect balanced tree with O(log N) search.',
                'Completely right-skewed tree equivalent to a linked list with O(N) search.',
                'Circular graph with O(1) search.',
                'Complete binary tree with O(1) search.'
              ],
              correct_index: 1,
              explanation: 'Each inserted element is greater than the previous root, creating a single right-branching chain of length 5 (O(N) search time).'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Binary Search Tree',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/binary-search-tree-data-structure/',
                description: 'Detailed tutorial on BST insertion, deletion, and search algorithms.'
              }
            ]
          }
        ]
      },
      {
        id: 'trees-mod-2',
        title: 'Module 2: Depth-First Traversals & BST Deletion',
        description: 'Master Inorder, Preorder, and Postorder tree traversals and the three cases of BST node deletion.',
        lessons: [
          {
            id: 'trees-m2-l1',
            title: 'Tree Traversals: Inorder, Preorder, Postorder',
            learning_objectives: [
              'Trace Inorder traversal (Left, Root, Right) and prove it yields sorted order on BSTs',
              'Trace Preorder (Root, Left, Right) for tree serialization and cloning',
              'Trace Postorder (Left, Right, Root) for bottom-up computation and memory deallocation'
            ],
            explanation: `Unlike linear structures, trees can be traversed in several depth-first recursive orders:\n\n1. Inorder (Left -> Root -> Right): Recursively visits left subtree, inspects current node, then recursively visits right subtree. On any valid BST, Inorder traversal visits keys in strictly sorted ascending order!\n2. Preorder (Root -> Left -> Right): Inspects current node before recursing on children. Ideal for copying/serializing a tree because children can be reconstructed under their parents.\n3. Postorder (Left -> Right -> Root): Recurses on both children before processing current node. Ideal for bottom-up tasks like calculating directory disk size or freeing memory.\n\nAll three traversals visit every node exactly once: O(N) time and O(H) auxiliary call stack space.`,
            code_example: {
              language: 'python',
              code: `def inorder_traversal(root):\n    res = []\n    def dfs(node):\n        if not node: return\n        dfs(node.left)       # 1. Left\n        res.append(node.val) # 2. Root\n        dfs(node.right)      # 3. Right\n    dfs(root)\n    return res\n\n# BST with values 50, 30, 70, 20, 40\n# Inorder yields sorted order: [20, 30, 40, 50, 70]`,
              explanation: 'Recursive Inorder traversal produces sorted output on any valid Binary Search Tree.',
              output: 'Sorted keys: [20, 30, 40, 50, 70]'
            },
            complexity: {
              time: 'O(N)',
              space: 'O(H) recursion stack where H is tree height',
              rationale: 'Every node is visited a constant number of times. Recursion stack depth equals the height of the tree.'
            },
            common_mistakes: [
              'Confusing the traversal order of Preorder (Root first) with Postorder (Root last).',
              'Failing to specify base case if not node: return, causing infinite recursion on leaf nodes.'
            ],
            key_takeaways: [
              'Inorder traversal of a BST produces sorted output.',
              'Preorder traversal is used for prefix serialization and cloning.',
              'Postorder traversal is used for bottom-up subtree metric evaluation.'
            ],
            quick_check: {
              id: 'qc-tree-3',
              question: 'Which tree traversal order visits a node only after both its left and right subtrees have been fully processed?',
              options: ['Preorder', 'Inorder', 'Postorder', 'Breadth-First Search'],
              correct_index: 2,
              explanation: 'Postorder follows Left -> Right -> Root, meaning the parent node is evaluated last.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Tree Traversals',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/',
                description: 'Visual animations and code for tree traversals.'
              }
            ]
          }
        ]
      }
    ]
  },

  GRAPHS: {
    concept_code: 'GRAPHS',
    concept_title: 'Graph Representations & Search',
    overview: 'Graphs are general network structures consisting of vertices connected by edges. They model complex relationships ranging from computer networks and GPS navigation to dependency DAGs and social media connections.',
    has_practice: true,
    modules: [
      {
        id: 'graphs-mod-1',
        title: 'Module 1: Graph Representations (Matrix vs. List)',
        description: 'Understand vertices, edges, directed vs undirected graphs, and contrast Adjacency Matrices with Adjacency Lists.',
        lessons: [
          {
            id: 'graphs-m1-l1',
            title: 'Graph Fundamentals & Storage Tradeoffs',
            learning_objectives: [
              'Define vertices (V), edges (E), directed/undirected, and weighted graphs',
              'Implement an Adjacency Matrix and evaluate its O(V^2) memory footprint',
              'Implement an Adjacency List and prove its O(V + E) memory optimality'
            ],
            explanation: `A Graph G = (V, E) consists of a set of vertices V (nodes) and edges E (connections between pairs of vertices).\n- Directed Graph (Digraph): Edges have direction (u -> v does not imply v -> u).\n- Undirected Graph: Edges are bidirectional.\n- Weighted Graph: Edges carry numerical costs/distances.\n\nTwo fundamental representations:\n1. Adjacency Matrix: A 2D array of size V x V where matrix[u][v] = 1 (or weight) if an edge exists. Edge lookup is instant O(1), but memory is strictly O(V^2), which is excessively wasteful for sparse graphs where E << V^2.\n2. Adjacency List: An array or hashmap mapping each vertex u to a list of its neighbors. Memory is optimal O(V + E). Finding all neighbors of vertex u takes O(degree(u)) time rather than scanning V columns. Most practical systems use Adjacency Lists.`,
            code_example: {
              language: 'python',
              code: `# Adjacency List representation in Python using dict of lists\ngraph = {\n    "A": ["B", "C"],\n    "B": ["A", "D", "E"],\n    "C": ["A", "F"],\n    "D": ["B"],\n    "E": ["B", "F"],\n    "F": ["C", "E"]\n}\n\n# Query neighbors of vertex 'B'\nprint("Neighbors of B:", graph["B"])`,
              explanation: 'Adjacency list uses O(V + E) space. Iterating neighbors of B requires only examining its 3 adjacent nodes.',
              output: "Neighbors of B: ['A', 'D', 'E']"
            },
            complexity: {
              time: 'Adjacency List: O(degree(u)) neighbor iteration; Matrix: O(1) edge check',
              space: 'Adjacency List: O(V + E); Adjacency Matrix: O(V^2)',
              rationale: 'Matrix allocates V^2 cells regardless of edge count. Adjacency list stores only vertices and existing edges.'
            },
            common_mistakes: [
              'Using an Adjacency Matrix for sparse graphs (e.g. 100,000 vertices with 200,000 edges would require 10 billion matrix entries: Out of Memory!).',
              'Forgetting to insert both directions (u -> v and v -> u) when building an undirected graph.'
            ],
            key_takeaways: [
              'Graphs generalize trees by permitting arbitrary cycles and multiple connections.',
              'Adjacency List is optimal for sparse graphs: O(V + E) space.',
              'Adjacency Matrix provides O(1) edge lookup at the expense of O(V^2) memory.'
            ],
            quick_check: {
              id: 'qc-graph-1',
              question: 'If a social network has 1,000,000 users and each user has an average of 100 friends, why is an Adjacency List far superior to an Adjacency Matrix?',
              options: [
                'Because an adjacency matrix cannot store strings.',
                'Because the matrix requires 1,000,000^2 = 1 trillion cells (terabytes of RAM), whereas the list stores only 1M vertices and 100M edges.',
                'Because BFS cannot run on an adjacency matrix.',
                'Because adjacency lists automatically delete unfriended connections.'
              ],
              correct_index: 1,
              explanation: 'A matrix requires V^2 space (10^12 entries). An adjacency list requires only V + 2E entries, fitting easily in standard RAM.'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Lecture 9',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture 9: Breadth-First Search and Graph Representations.'
              },
              {
                name: 'GeeksforGeeks Graph Data Structure',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/',
                description: 'Complete tutorials on graph representations, BFS, and DFS.'
              }
            ]
          }
        ]
      },
      {
        id: 'graphs-mod-2',
        title: 'Module 2: Graph Traversals: BFS and DFS',
        description: 'Master Breadth-First Search (shortest path in unweighted graphs) and Depth-First Search (cycle detection and topological sort).',
        lessons: [
          {
            id: 'graphs-m2-l1',
            title: 'Breadth-First Search (BFS) & Shortest Path',
            learning_objectives: [
              'Implement BFS using a queue and visited set',
              'Prove that BFS finds the shortest path in unweighted graphs',
              'Analyze the O(V + E) time and O(V) space complexity'
            ],
            explanation: `Breadth-First Search (BFS) explores a graph level by level outward from a start vertex. It systematically visits all distance-1 neighbors, then all distance-2 neighbors, and so on.\n\nMechanics:\n1. Initialize a FIFO Queue and enqueue the start vertex.\n2. Mark start vertex as visited in a set or boolean array.\n3. While queue is not empty: dequeue current vertex u; for each unvisited neighbor v of u, mark v as visited and enqueue v.\n\nCrucial Property: The first time BFS reaches any vertex in an unweighted graph, the path taken is guaranteed to be the shortest path (minimum edge count) from the start vertex!\n\nCrucial Guard: Graphs can contain cycles. If you do not track visited vertices, the algorithm will cycle endlessly in an infinite loop!`,
            code_example: {
              language: 'python',
              code: `from collections import deque\n\ndef bfs_shortest_path(graph, start, target):\n    queue = deque([(start, [start])])\n    visited = {start}\n    \n    while queue:\n        curr, path = queue.popleft()\n        if curr == target:\n            return path\n        for neighbor in graph.get(curr, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append((neighbor, path + [neighbor]))\n    return None\n\ng = {\n    "A": ["B", "C"],\n    "B": ["A", "D", "E"],\n    "C": ["A", "F"],\n    "D": ["B"],\n    "E": ["B", "F"],\n    "F": ["C", "E"]\n}\n\nprint("Shortest path A -> F:", bfs_shortest_path(g, "A", "F"))`,
              explanation: 'BFS discovers F via path [A, C, F] (2 edges), ignoring the longer path [A, B, E, F].',
              output: "Shortest path A -> F: ['A', 'C', 'F']"
            },
            complexity: {
              time: 'O(V + E)',
              space: 'O(V)',
              rationale: 'Every vertex is enqueued at most once (V) and every edge incident to that vertex is scanned once (E). The queue and visited set store at most V elements.'
            },
            common_mistakes: [
              'Forgetting the visited set, causing infinite recursion / loops on cyclic graphs.',
              'Marking a vertex as visited when popping from the queue instead of when pushing, leading to duplicate enqueues.'
            ],
            key_takeaways: [
              'BFS uses a FIFO queue and visits vertices in order of increasing distance from start.',
              'BFS guarantees the shortest path in unweighted graphs.',
              'Always mark vertices visited at the moment they are enqueued.'
            ],
            quick_check: {
              id: 'qc-graph-2',
              question: 'Why does BFS guarantee finding the shortest path between two nodes in an unweighted graph?',
              options: [
                'Because it sorts the graph edges by weight using quicksort.',
                'Because it explores vertices in order of increasing distance from the starting node (level by level).',
                'Because it uses recursion to evaluate all possible paths simultaneously.',
                'Because it avoids visiting leaf nodes.'
              ],
              correct_index: 1,
              explanation: 'By using a FIFO queue, BFS inspects all paths of length k before inspecting any path of length k+1.'
            },
            external_references: [
              {
                name: 'GeeksforGeeks Breadth First Search',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/',
                description: 'BFS walkthrough with step-by-step queue visualizer.'
              }
            ]
          },
          {
            id: 'graphs-m2-l2',
            title: 'Depth-First Search (DFS) & Cycle Detection',
            learning_objectives: [
              'Implement DFS using recursion or an explicit stack',
              'Apply DFS to cycle detection and connected components',
              'Trace the DFS backtracking mechanism'
            ],
            explanation: `Depth-First Search (DFS) explores as deep as possible along each branch before backtracking. When visiting vertex u, it selects an unvisited neighbor v and immediately recurses on v, only returning when no further unvisited neighbors exist.\n\nMechanics:\n- Uses an implicit recursion call stack or an explicit LIFO Stack.\n- Maintains a visited set to avoid infinite cycles.\n- In directed graphs, uses a 3-state coloring (Unvisited, Visiting/In-Stack, Visited) to detect back-edges, which directly indicate cycles.\n\nApplications: Topological Sorting (scheduling dependent build tasks), cycle detection in compilers, finding strongly connected components, solving maze puzzles.`,
            code_example: {
              language: 'python',
              code: `def dfs_traverse(graph, start):\n    visited = set()\n    traversal_order = []\n    \n    def dfs(node):\n        visited.add(node)\n        traversal_order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                dfs(neighbor)\n                \n    dfs(start)\n    return traversal_order\n\ng = {\n    "A": ["B", "C"],\n    "B": ["D"],\n    "C": ["E"],\n    "D": [],\n    "E": []\n}\n\nprint("DFS Traversal:", dfs_traverse(g, "A"))`,
              explanation: 'DFS dives down branch A -> B -> D before backtracking to explore branch A -> C -> E.',
              output: "DFS Traversal: ['A', 'B', 'D', 'C', 'E']"
            },
            complexity: {
              time: 'O(V + E)',
              space: 'O(V) for the call stack and visited set',
              rationale: 'Every vertex is visited once and every edge is explored. In the worst case (a single linear chain), the recursion stack reaches depth V.'
            },
            common_mistakes: [
              'Exceeding maximum recursion depth on large graphs (overcome using sys.setrecursionlimit or an explicit iterative stack).',
              'Confusing undirected cycle detection (which requires passing the parent node) with directed cycle detection (which requires tracking the current recursion stack).'
            ],
            key_takeaways: [
              'DFS explores deeply before backtracking, using LIFO stack discipline.',
              'DFS runs in O(V + E) time and O(V) space.',
              'DFS is the foundation of Topological Sort, Cycle Detection, and Connected Component analysis.'
            ],
            quick_check: {
              id: 'qc-graph-3',
              question: 'In a directed graph, how does DFS detect the presence of a cycle?',
              options: [
                'When it encounters a node with zero outgoing edges.',
                'When it visits a neighbor that is already in the current recursion call stack (a back-edge).',
                'When the number of visited nodes exceeds the number of edges.',
                'When the call stack becomes empty.'
              ],
              correct_index: 1,
              explanation: 'A cycle in a directed graph exists if and only if DFS encounters an edge pointing to an ancestor currently active on the recursion stack.'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Lecture 10',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
                description: 'Lecture 10: Depth-First Search and Topological Sort.'
              },
              {
                name: 'GeeksforGeeks Depth First Search',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/',
                description: 'DFS implementation and applications.'
              }
            ]
          }
        ]
      }
    ]
  },

  ALG_THINK: {
    concept_code: 'ALG_THINK',
    concept_title: 'Algorithmic Thinking',
    overview: 'Algorithmic thinking is the disciplined cognitive methodology of decomposing ambiguous real-world problems into unambiguous, step-by-step computational procedures. It balances input constraints, pattern recognition, and asymptotic efficiency.',
    has_practice: false,
    practice_notice: 'Practice questions for this foundational topic are not currently available. Please focus on mastering the conceptual modules below.',
    modules: [
      {
        id: 'alg-mod-1',
        title: 'Module 1: Problem Decomposition & Computational Mindset',
        description: 'Learn to deconstruct complex requirements, identify inputs/outputs, and formulate unambiguous procedures.',
        lessons: [
          {
            id: 'alg-m1-l1',
            title: 'Decomposition, Inputs & Constraints',
            learning_objectives: [
              'Deconstruct complex domain challenges into modular sub-problems',
              'Identify explicit inputs, expected outputs, and implicit boundary constraints',
              'Formulate deterministic, step-by-step solution outlines before writing code'
            ],
            explanation: `Computers cannot interpret intent; they strictly execute instructions. Algorithmic thinking begins not with typing syntax, but with disciplined deconstruction:\n\n1. Input Identification: What data is provided? What are the data types, ranges, and order guarantees? Can inputs be empty, negative, or contain duplicate values?\n2. Output Specification: Exactly what should be returned or modified? Should the operation be in-place, or produce a fresh data structure?\n3. Constraints & Scale: If N <= 10^3, an O(N^2) solution will easily execute within 1 second. If N = 10^6, only an O(N) or O(N log N) solution will terminate without a Time Limit Exceeded (TLE) error.\n4. Problem Decomposition: Break the grand objective into distinct sub-problems (e.g. Clean Input -> Sort -> Match Pairs -> Format Output).`,
            code_example: {
              language: 'python',
              code: `# Example: Structured problem solving framework\n# Problem: Find the first non-repeating character in a string.\n\ndef first_unique_char(s: str) -> int:\n    # Step 1: Sub-problem A - Build frequency distribution map\n    char_counts = {}\n    for char in s:\n        char_counts[char] = char_counts.get(char, 0) + 1\n        \n    # Step 2: Sub-problem B - Re-scan string in original order to find first count == 1\n    for idx, char in enumerate(s):\n        if char_counts[char] == 1:\n            return idx\n            \n    return -1  # Output: -1 if all characters repeat\n\nprint("Index of first unique:", first_unique_char("edupathedx"))`,
              explanation: 'Decomposing the problem into two sequential passes (counting frequencies O(N), then finding first unique O(N)) avoids quadratic O(N^2) nested loops.',
              output: 'Index of first unique: 0'
            },
            complexity: {
              time: 'O(N) linear time across two passes',
              space: 'O(1) auxiliary space (at most 26 lowercase English letters)',
              rationale: 'Decomposition transforms an O(N^2) pairwise search into an O(N) frequency lookup.'
            },
            common_mistakes: [
              'Immediately writing code before clarifying input constraints and edge cases.',
              'Assuming inputs will always be well-formed without testing empty, single-element, or extreme values.'
            ],
            key_takeaways: [
              'Always identify input types, ranges, and constraints before choosing an approach.',
              'Decompose large problems into independently verifiable sub-problems.',
              'Input scale (N) dictates the permissible asymptotic Big-O time complexity.'
            ],
            quick_check: {
              id: 'qc-alg-1',
              question: 'If a problem statement states that array length N can be up to 1,000,000 (10^6), which asymptotic time complexity will reliably pass within a standard 1.0-second CPU limit?',
              options: [
                'O(N^3) cubic time',
                'O(N^2) quadratic time',
                'O(N) linear or O(N log N) log-linear time',
                'O(2^N) exponential time'
              ],
              correct_index: 2,
              explanation: 'A modern CPU performs roughly 10^8 operations per second. For N = 10^6, O(N^2) would require 10^12 operations (hours), whereas O(N log N) requires ~2*10^7 operations (fraction of a second).'
            },
            external_references: [
              {
                name: 'MIT OpenCourseWare 6.006 Introduction',
                source_type: 'MIT OpenCourseWare',
                url: 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-1-introduction/',
                description: 'Lecture 1: Introduction to Algorithmic Thinking and Analysis.'
              },
              {
                name: 'GeeksforGeeks Fundamentals of Algorithms',
                source_type: 'GeeksforGeeks',
                url: 'https://www.geeksforgeeks.org/fundamentals-of-algorithms/',
                description: 'Core concepts in problem solving, invariants, and algorithmic thinking.'
              }
            ]
          }
        ]
      },
      {
        id: 'alg-mod-2',
        title: 'Module 2: Pattern Recognition & Optimization Strategy',
        description: 'Master the progression from brute-force baselines to optimized data structure selection.',
        lessons: [
          {
            id: 'alg-m2-l1',
            title: 'From Brute Force to Optimal Design: The Two-Sum Evolution',
            learning_objectives: [
              'Formulate a brute-force baseline to prove solution correctness',
              'Identify redundant computation and bottleneck operations',
              'Select appropriate data structures to achieve optimal asymptotic bounds'
            ],
            explanation: `A master algorithmist never struggles to find an optimal solution immediately. Instead, they follow the Systematic Optimization Strategy:\n\n1. Establish the Brute-Force Baseline: Find the most straightforward, obviously correct method. For example, in the Two-Sum problem (find two numbers that sum to target), check all N*(N-1)/2 pairs in nested loops: O(N^2) time.\n2. Identify the Bottleneck: In the brute force, for each number x, we perform a linear scan of the rest of the array to find target - x. The bottleneck is the repeated O(N) search!\n3. Choose the Optimal Data Structure: What data structure performs searches in O(1) time? A Hash Map! By storing visited numbers in a hash map as we iterate, looking up target - x takes O(1) time.\n4. Result: Total complexity collapses from O(N^2) to O(N) linear time, trading O(N) memory for dramatic speedups.`,
            code_example: {
              language: 'python',
              code: `# Evolution from O(N^2) Brute Force to O(N) Hash Table\ndef two_sum_optimal(nums, target):\n    seen = {}  # maps value -> index\n    for idx, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return (seen[complement], idx)\n        seen[num] = idx\n    return None\n\nprint("Found indices:", two_sum_optimal([3, 2, 4], 6))`,
              explanation: 'Hash map lookup takes O(1) average time, transforming the quadratic nested loop into a single linear pass.',
              output: 'Found indices: (1, 2)'
            },
            complexity: {
              time: 'O(N)',
              space: 'O(N)',
              rationale: 'A single linear pass through N elements with O(1) hash map operations.'
            },
            common_mistakes: [
              'Trying to optimize prematurely before having a verifiable, correct brute-force understanding.',
              'Ignoring space-time tradeoffs: refusing to use O(N) auxiliary space even when it yields an exponential time speedup.'
            ],
            key_takeaways: [
              'Start with a simple brute-force baseline to establish correctness.',
              'Identify the exact computational bottleneck (usually repeated searching or re-sorting).',
              'Substitute targeted data structures (e.g. hash maps, heaps, binary search trees) to eliminate the bottleneck.'
            ],
            quick_check: {
              id: 'qc-alg-2',
              question: 'In the Two-Sum evolution, what was the primary insight that enabled reducing time complexity from O(N^2) to O(N)?',
              options: [
                'Sorting the array using bubble sort.',
                'Recognizing that checking for the complement (target - x) can be performed in O(1) time using a hash map.',
                'Executing the nested loops in parallel threads.',
                'Converting all numbers into floating-point representation.'
              ],
              correct_index: 1,
              explanation: 'Replacing an O(N) linear search for the complement with an O(1) hash table lookup reduces the overall time from O(N^2) to O(N).'
            },
            external_references: [
              {
                name: 'OpenStax Algorithmic Problem Solving',
                source_type: 'OpenStax',
                url: 'https://openstax.org/details/books/computer-science',
                description: 'Open textbook chapter on computational complexity and problem-solving strategies.'
              }
            ]
          }
        ]
      }
    ]
  }
};

export const getConceptContent = (conceptCode: string): ConceptContent | undefined => {
  return LEARNING_CONTENT_REGISTRY[conceptCode.toUpperCase()];
};

export const getAllConceptContents = (): Record<string, ConceptContent> => {
  return LEARNING_CONTENT_REGISTRY;
};
