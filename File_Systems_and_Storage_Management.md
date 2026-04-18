# FILE SYSTEMS AND STORAGE MANAGEMENT

## A Comprehensive Guide to Operating System Storage

---

## TABLE OF CONTENTS

1. Introduction to File Systems
2. File System Structures and Operations
3. Directory Structures and Access Methods
4. Disk Scheduling Algorithms
5. Conclusion
6. References

---

## 1. INTRODUCTION TO FILE SYSTEMS

### 1.1 What is a File System?

A file system represents a fundamental component of operating systems that provides structured methods for organizing, storing, retrieving, and managing data on storage devices. According to research, file systems serve as the backbone of data storage, offering mechanisms that abstract hardware complexities while presenting user-friendly interfaces for applications and users ([Source: Fiveable.me](https://library.fiveable.me/operating-systems/unit-4)).

Content was rephrased for compliance with licensing restrictions.

Without file systems, data would exist as unorganized information, making it practically unusable. The file system acts as an intermediary between the physical storage hardware and the logical view that users and applications interact with.

### 1.2 Purpose and Importance

File systems serve several critical functions in modern computing:

- **Organization**: Arranging files in logical hierarchies for easy navigation
- **Storage Management**: Efficiently allocating disk space to files
- **Access Control**: Managing permissions and security for files
- **Data Retrieval**: Providing fast access to stored information
- **Metadata Management**: Tracking file attributes like size, creation date, and ownership

### 1.3 Evolution of File Systems

The development of file systems has evolved significantly over decades. Early systems used paper tape and punch cards, progressing to magnetic tape drives. As disk storage became affordable in the 1970s and 1980s, file systems focused on hierarchical directories, basic metadata, and sequential access patterns for performance optimization ([Source: GuruSoftware.com](https://www.gurusoftware.com/file-systems-in-operating-systems-an-in-depth-guide/)).

Content was rephrased for compliance with licensing restrictions.

---

## 2. FILE SYSTEM STRUCTURES AND OPERATIONS

### 2.1 File System Structure Components


The file system structure defines how files are arranged, how directories are organized, and how the operating system locates and stores data. Key structural components include:

#### 2.1.1 Boot Control Block

The boot control block contains information needed to boot the operating system from that volume. It is typically the first block of the volume and includes boot loader code.

#### 2.1.2 Volume Control Block

This component contains volume details such as:
- Number of blocks in the partition
- Block size
- Free block count and pointers
- Free file control block count and pointers

#### 2.1.3 Directory Structure

The directory structure organizes files within the file system. It maintains information about file names, locations, and attributes.

#### 2.1.4 File Control Block (FCB)

The FCB stores detailed information about individual files, including:
- File permissions and ownership
- File size and location on disk
- Creation, modification, and access timestamps
- Pointers to data blocks

### 2.2 File Allocation Methods

File allocation methods determine how files are physically stored on disk and how space is allocated. Three primary methods exist:

#### 2.2.1 Contiguous Allocation

In contiguous allocation, each file occupies a continuous set of blocks on the disk. If a file requires n blocks starting at block b, the assigned blocks are b, b+1, b+2, ..., b+n-1 ([Source: GeeksforGeeks](https://www.geeksforgeeks.org/operating-systems/file-allocation-methods/)).

**Advantages:**
- Minimal disk head movement during sequential access
- Fast access time due to sequential storage
- Simple implementation requiring only starting address and length

**Disadvantages:**
- External fragmentation as files are deleted
- Difficulty in file growth (requires relocation)
- Requires knowing file size in advance

#### 2.2.2 Linked Allocation

Linked allocation stores files as linked lists of disk blocks. Each block contains a pointer to the next block in the file sequence.

**Advantages:**
- No external fragmentation
- Files can grow dynamically
- No need to declare file size initially

**Disadvantages:**
- Slower random access (must traverse links)
- Space overhead for storing pointers
- Reliability issues if pointers are corrupted


#### 2.2.3 Indexed Allocation

Indexed allocation brings all pointers together into an index block. Each file has its own index block containing pointers to all blocks allocated to that file.

**Advantages:**
- Supports direct access without external fragmentation
- Dynamic file growth without relocation
- No chaining overhead

**Disadvantages:**
- Overhead of index block space
- Multiple disk accesses for large files
- Complexity in managing index blocks

### 2.3 File System Operations

File systems support various operations that applications use to interact with stored data:

#### 2.3.1 File Creation

File creation involves allocating disk space and creating a directory entry. The system must find available space, create the file control block, and update the directory structure.

#### 2.3.2 File Reading

Reading requires specifying the file name and providing a memory buffer address to store the content. The system locates the file, reads the requested data blocks, and transfers data to the buffer.

#### 2.3.3 File Writing

Writing operations require the file name and data to write. The system locates the file, allocates additional space if needed, and writes data to the appropriate blocks.

#### 2.3.4 File Deletion

Deletion involves removing the directory entry and releasing the allocated disk space back to the free space pool. The system updates metadata to reflect the freed blocks.

#### 2.3.5 File Positioning

Positioning operations set the read/write pointer within the file, allowing applications to access specific locations without reading from the beginning.

#### 2.3.6 File Truncation

Truncation reduces file size by releasing blocks beyond a specified point while maintaining file attributes and directory entry.

### 2.4 File Attributes and Metadata

File systems maintain extensive metadata about each file:

- **Name**: Human-readable identifier
- **Type**: File extension or format indicator
- **Location**: Physical address on storage device
- **Size**: Current file size in bytes
- **Protection**: Access permissions and ownership
- **Time stamps**: Creation, modification, and last access times
- **User identification**: Owner and group information

---

## 3. DIRECTORY STRUCTURES AND ACCESS METHODS

### 3.1 Understanding Directory Structures

A directory structure represents a hierarchical organization system used to arrange files on storage devices. Similar to a tree with branches, directories can contain both files and other directories, creating structured data organization ([Source: CompileNRun](https://www.compilenrun.com/docs/fundamental/os/file-systems/directory-structure/)).

Content was rephrased for compliance with licensing restrictions.


### 3.2 Types of Directory Structures

#### 3.2.1 Single-Level Directory

The simplest directory structure where all files exist in a single directory.

**Characteristics:**
- All files in one location
- Simple to implement and understand
- Easy file naming and searching

**Limitations:**
- Name collision issues with multiple users
- No file grouping capability
- Difficult to organize large numbers of files
- Poor scalability

**Use Cases:**
- Early operating systems
- Simple embedded systems
- Single-user environments with few files

#### 3.2.2 Two-Level Directory

This structure provides a separate directory for each user, with a master file directory containing user directories.

**Characteristics:**
- Each user has a private directory
- Reduces name collision problems
- Provides basic isolation between users
- Master directory tracks user directories

**Advantages:**
- Better organization than single-level
- User isolation and privacy
- Reduced naming conflicts

**Limitations:**
- No grouping within user directories
- Limited hierarchy depth
- Difficult to share files between users

#### 3.2.3 Tree-Structured Directory

The tree structure creates a hierarchical arrangement with a root directory at the top and subdirectories branching downward. This enables logical file grouping, such as organizing image files into an "Images" folder, improving usability and search efficiency ([Source: TutorialsArena](https://www.tutorialsarena.com/fundamentals/os/os-tree-structured-directory)).

Content was rephrased for compliance with licensing restrictions.

**Characteristics:**
- Root directory at the top level
- Each user typically has their own directory under root
- Unlimited subdirectory depth
- Path names specify file locations

**Advantages:**
- Efficient file organization
- Logical grouping of related files
- Scalable to large file systems
- Supports complex organizational structures

**Path Notation:**
- **Absolute Path**: Complete path from root (e.g., /home/user/documents/file.txt)
- **Relative Path**: Path from current directory (e.g., ../documents/file.txt)


#### 3.2.4 Acyclic Graph Directory

An acyclic graph structure allows files and subdirectories to be shared between directories without creating cycles.

**Characteristics:**
- Supports file and directory sharing
- Multiple paths to the same file
- Uses links or pointers for sharing
- No circular references allowed

**Implementation Methods:**
- **Hard Links**: Direct pointers to file data
- **Soft Links (Symbolic Links)**: Pointers to file names

**Advantages:**
- Efficient file sharing
- Reduced storage duplication
- Flexible organization

**Challenges:**
- Complexity in deletion (reference counting)
- Potential for dangling pointers
- More complex traversal algorithms

#### 3.2.5 General Graph Directory

The most flexible structure allowing cycles in the directory graph.

**Characteristics:**
- Permits circular references
- Maximum flexibility in organization
- Complex management requirements

**Challenges:**
- Risk of infinite loops during traversal
- Complicated garbage collection
- Difficult to determine when files can be deleted
- Requires sophisticated algorithms to prevent issues

### 3.3 Directory Operations

File systems provide various operations for directory management:

#### 3.3.1 Search

Locating files within the directory structure by name or attributes. Efficient search algorithms are essential for large file systems.

#### 3.3.2 Create File

Adding a new file entry to the directory, allocating space, and initializing metadata.

#### 3.3.3 Delete File

Removing file entries from the directory and releasing associated storage space.

#### 3.3.4 List Directory

Displaying all files and subdirectories within a specified directory, often with filtering and sorting options.

#### 3.3.5 Rename File

Changing the file name within the directory structure while maintaining file data and attributes.

#### 3.3.6 Traverse File System

Systematically accessing every file and directory in the structure, used for backup, search, and maintenance operations.


### 3.4 File Access Methods

Access methods define how programs read and write file data:

#### 3.4.1 Sequential Access

Sequential access processes file records in order from beginning to end.

**Characteristics:**
- Records read/written in sequence
- Simple implementation
- Efficient for processing entire files
- Common in tape-based systems

**Operations:**
- Read next record
- Write next record
- Reset to beginning
- Skip forward n records

**Use Cases:**
- Log files
- Batch processing
- Streaming data
- Backup operations

#### 3.4.2 Direct Access (Random Access)

Direct access allows reading or writing records in any order without processing preceding records.

**Characteristics:**
- Records accessed by position or key
- Requires fixed-length records or index
- Fast access to specific data
- Essential for databases

**Operations:**
- Read record n
- Write record n
- Position to record n
- Read next/previous record

**Use Cases:**
- Database systems
- Random access files
- Index-based retrieval
- Interactive applications

#### 3.4.3 Indexed Sequential Access

Combines sequential and direct access using an index structure.

**Characteristics:**
- Index provides fast lookup
- Sequential processing still possible
- Efficient for both access patterns
- Requires index maintenance

**Components:**
- Primary data file (sequential)
- Index file (direct access)
- Overflow area for insertions

**Advantages:**
- Fast search via index
- Efficient sequential processing
- Supports both access patterns

---

## 4. DISK SCHEDULING ALGORITHMS

### 4.1 Introduction to Disk Scheduling

Disk scheduling algorithms represent fundamental components of operating systems that determine the order in which disk input/output requests are processed. These algorithms significantly impact system performance by minimizing seek time and optimizing data access patterns ([Source: CodeLucky](https://codelucky.com/disk-scheduling-algorithms/)).

Content was rephrased for compliance with licensing restrictions.


### 4.2 Disk Performance Metrics

Understanding disk scheduling requires knowledge of key performance metrics:

#### 4.2.1 Seek Time

The time required for the disk head to move to the desired track. This is typically the most significant component of disk access time.

#### 4.2.2 Rotational Latency

The time for the desired sector to rotate under the disk head after the head reaches the correct track.

#### 4.2.3 Transfer Time

The time to actually read or write data once the head is positioned correctly.

#### 4.2.4 Disk Bandwidth

The total number of bytes transferred divided by the total time from request initiation to transfer completion.

### 4.3 First-Come, First-Served (FCFS)

#### 4.3.1 Algorithm Description

FCFS represents a primitive algorithm that processes requests in the order they arrive. The disk head serves requests sequentially without considering their physical locations on the disk.

**Algorithm Steps:**
1. Maintain a queue of disk requests
2. Process requests in arrival order
3. Move disk head to each requested track sequentially
4. Complete current request before starting next

#### 4.3.2 Advantages

- **Simplicity**: Easiest algorithm to implement
- **Fairness**: No request starvation; every request eventually gets served
- **Predictability**: Request order is deterministic
- **Low Overhead**: Minimal computational requirements

#### 4.3.3 Disadvantages

- **Poor Performance**: May result in excessive head movement
- **No Optimization**: Ignores physical disk layout
- **High Seek Time**: Can cause long waits for distant requests
- **Inefficient**: Not suitable for systems with heavy I/O loads

#### 4.3.4 Example

Consider a disk with 200 tracks (0-199) and the following request queue:
98, 183, 37, 122, 14, 124, 65, 67

Starting position: Track 53

**FCFS Movement:**
53 → 98 (45 tracks)
98 → 183 (85 tracks)
183 → 37 (146 tracks)
37 → 122 (85 tracks)
122 → 14 (108 tracks)
14 → 124 (110 tracks)
124 → 65 (59 tracks)
65 → 67 (2 tracks)

**Total Head Movement:** 640 tracks


### 4.4 Shortest Seek Time First (SSTF)

#### 4.4.1 Algorithm Description

SSTF selects the request closest to the current disk head position, thereby reducing seek time. This algorithm prioritizes minimizing head movement distance.

**Algorithm Steps:**
1. From current position, identify all pending requests
2. Select the request with minimum seek distance
3. Move head to selected request location
4. Repeat until all requests are served

#### 4.4.2 Advantages

- **Reduced Seek Time**: Minimizes total head movement
- **Better Performance**: Significantly faster than FCFS
- **Efficient**: Good throughput for moderate loads
- **Simple Logic**: Relatively easy to implement

#### 4.4.3 Disadvantages

- **Starvation Risk**: Distant requests may wait indefinitely
- **Unfairness**: Requests in middle tracks get priority
- **Unpredictable**: Response time varies significantly
- **Not Optimal**: Doesn't guarantee minimum total seek time

#### 4.4.4 Example

Using the same request queue: 98, 183, 37, 122, 14, 124, 65, 67
Starting position: Track 53

**SSTF Movement:**
53 → 65 (12 tracks) - closest
65 → 67 (2 tracks) - closest
67 → 37 (30 tracks) - closest
37 → 14 (23 tracks) - closest
14 → 98 (84 tracks) - closest
98 → 122 (24 tracks) - closest
122 → 124 (2 tracks) - closest
124 → 183 (59 tracks) - closest

**Total Head Movement:** 236 tracks (63% improvement over FCFS)

### 4.5 SCAN Algorithm (Elevator Algorithm)

#### 4.5.1 Algorithm Description

SCAN moves the disk head in one direction, servicing all requests along the way until reaching the end of the disk, then reverses direction. This behavior resembles an elevator, hence the nickname "Elevator Algorithm."

**Algorithm Steps:**
1. Start moving in a chosen direction (toward 0 or toward max)
2. Service all requests encountered in that direction
3. Continue until reaching the disk end
4. Reverse direction
5. Service requests in the opposite direction
6. Repeat the process

#### 4.5.2 Advantages

- **No Starvation**: All requests eventually get served
- **Uniform Wait Time**: More predictable response times
- **Good Throughput**: Efficient for heavy loads
- **Fair Distribution**: Balanced service across all tracks


#### 4.5.3 Disadvantages

- **End Track Bias**: Requests at disk ends wait longer
- **Unnecessary Movement**: Head travels to disk end even without requests
- **Moderate Complexity**: More complex than FCFS or SSTF
- **Direction Dependency**: Performance varies with initial direction

#### 4.5.4 Example

Using the same request queue: 98, 183, 37, 122, 14, 124, 65, 67
Starting position: Track 53, moving toward track 0

**SCAN Movement:**
53 → 37 (16 tracks) - moving toward 0
37 → 14 (23 tracks) - moving toward 0
14 → 0 (14 tracks) - reach end
0 → 65 (65 tracks) - reverse direction
65 → 67 (2 tracks) - moving toward 199
67 → 98 (31 tracks) - moving toward 199
98 → 122 (24 tracks) - moving toward 199
122 → 124 (2 tracks) - moving toward 199
124 → 183 (59 tracks) - moving toward 199

**Total Head Movement:** 236 tracks

### 4.6 C-SCAN Algorithm (Circular SCAN)

#### 4.6.1 Algorithm Description

C-SCAN provides more uniform wait time than SCAN by treating the disk as circular. The head moves in one direction, servicing requests, then quickly returns to the beginning without servicing requests on the return trip.

**Algorithm Steps:**
1. Start moving in one direction (typically toward higher tracks)
2. Service all requests encountered
3. Upon reaching the disk end, jump to the beginning
4. Resume servicing in the same direction
5. Repeat the circular pattern

#### 4.6.2 Advantages

- **Uniform Wait Time**: More consistent response times
- **Fair Service**: Eliminates bias toward middle tracks
- **No Starvation**: Guaranteed service for all requests
- **Predictable**: Easier to estimate wait times
- **Better for Heavy Loads**: Efficient under high I/O demand

#### 4.6.3 Disadvantages

- **Return Overhead**: Time wasted during head return
- **Complexity**: More complex implementation than SCAN
- **Longer Average Wait**: Some requests wait for full cycle
- **Resource Usage**: Return trip uses disk bandwidth


#### 4.6.4 Example

Using the same request queue: 98, 183, 37, 122, 14, 124, 65, 67
Starting position: Track 53, moving toward track 199

**C-SCAN Movement:**
53 → 65 (12 tracks) - moving toward 199
65 → 67 (2 tracks) - moving toward 199
67 → 98 (31 tracks) - moving toward 199
98 → 122 (24 tracks) - moving toward 199
122 → 124 (2 tracks) - moving toward 199
124 → 183 (59 tracks) - moving toward 199
183 → 199 (16 tracks) - reach end
199 → 0 (199 tracks) - return to beginning
0 → 14 (14 tracks) - resume servicing
14 → 37 (23 tracks) - moving toward 199

**Total Head Movement:** 382 tracks

### 4.7 Comparison of Disk Scheduling Algorithms

#### 4.7.1 Performance Comparison Table

| Algorithm | Avg Seek Time | Fairness | Starvation Risk | Complexity | Best Use Case |
|-----------|---------------|----------|-----------------|------------|---------------|
| FCFS | High | Excellent | None | Very Low | Light loads, simple systems |
| SSTF | Low | Poor | High | Low | Moderate loads, performance priority |
| SCAN | Moderate | Good | None | Moderate | Heavy loads, balanced needs |
| C-SCAN | Moderate | Excellent | None | Moderate | Heavy loads, uniform service |

#### 4.7.2 Selection Criteria

**Choose FCFS when:**
- System has light I/O load
- Simplicity is paramount
- Fairness is critical
- Implementation resources are limited

**Choose SSTF when:**
- Performance is the primary concern
- I/O load is moderate
- Starvation is acceptable
- Quick response for nearby requests is needed

**Choose SCAN when:**
- System has heavy I/O load
- Balance between performance and fairness is needed
- Starvation must be avoided
- Predictable service is important

**Choose C-SCAN when:**
- Uniform wait time is critical
- System has very heavy I/O load
- Fair service across all tracks is required
- Predictability is more important than raw performance

### 4.8 Modern Considerations

#### 4.8.1 Solid State Drives (SSDs)

Traditional disk scheduling algorithms are less relevant for SSDs because:
- No mechanical seek time
- Random access is nearly as fast as sequential
- Wear leveling considerations
- Different optimization strategies needed


#### 4.8.2 Hybrid Approaches

Modern systems often combine multiple algorithms:
- **Deadline Scheduling**: Ensures requests don't wait too long
- **Anticipatory Scheduling**: Predicts future requests
- **CFQ (Completely Fair Queuing)**: Balances fairness and performance
- **NOOP**: Simple FIFO for SSDs

---

## 5. CONCLUSION

### 5.1 Summary of Key Concepts

File systems and storage management represent critical components of modern operating systems. This document has explored three fundamental areas:

**File System Structures and Operations:**
File systems provide organized methods for storing and retrieving data through various allocation methods (contiguous, linked, and indexed). Each method offers distinct advantages and trade-offs regarding performance, fragmentation, and flexibility. File operations including creation, reading, writing, and deletion form the foundation of data management.

**Directory Structures and Access Methods:**
Directory structures have evolved from simple single-level systems to complex hierarchical and graph-based organizations. The tree-structured directory has become the standard, offering logical organization and scalability. Access methods (sequential, direct, and indexed sequential) provide different approaches to data retrieval based on application requirements.

**Disk Scheduling Algorithms:**
Disk scheduling algorithms optimize the order of I/O request processing. FCFS offers simplicity and fairness but poor performance. SSTF improves performance but risks starvation. SCAN and C-SCAN provide balanced solutions with no starvation, making them suitable for systems with heavy I/O loads.

### 5.2 Importance in Modern Computing

Understanding file systems and storage management remains crucial despite technological advances:

1. **Performance Optimization**: Proper algorithm selection significantly impacts system responsiveness
2. **Resource Management**: Efficient storage utilization reduces costs and improves scalability
3. **Data Integrity**: Well-designed file systems protect against data loss and corruption
4. **User Experience**: Organized directory structures enhance usability and productivity

### 5.3 Future Trends

Storage management continues to evolve with emerging technologies:

- **Cloud Storage Integration**: Distributed file systems spanning multiple locations
- **AI-Driven Optimization**: Machine learning predicting access patterns
- **Non-Volatile Memory**: New storage technologies requiring adapted algorithms
- **Blockchain-Based Systems**: Decentralized storage with enhanced security
- **Quantum Storage**: Future possibilities with quantum computing

### 5.4 Practical Applications

The concepts covered in this document apply across various domains:

- **Database Systems**: Rely heavily on efficient file allocation and access methods
- **Operating Systems**: Implement these algorithms for system-wide storage management
- **Cloud Services**: Use distributed versions of these concepts
- **Embedded Systems**: Adapt these principles for resource-constrained environments
- **Mobile Devices**: Optimize for battery life and limited storage


### 5.5 Final Thoughts

File systems and storage management form the invisible infrastructure supporting all computing activities. From simple file creation to complex database operations, these systems work continuously to ensure data remains accessible, secure, and efficiently organized. As storage technologies evolve, the fundamental principles discussed in this document continue to guide the development of new solutions.

Understanding these concepts enables computer scientists, system administrators, and software developers to make informed decisions about storage architecture, optimize application performance, and troubleshoot system issues effectively.

---

## 6. REFERENCES

### Academic and Educational Sources

1. Fiveable.me. (n.d.). *Operating Systems Class Notes - File Systems*. Retrieved from [https://library.fiveable.me/operating-systems/unit-4](https://library.fiveable.me/operating-systems/unit-4)

2. GeeksforGeeks. (2024). *File Allocation Methods*. Retrieved from [https://www.geeksforgeeks.org/operating-systems/file-allocation-methods/](https://www.geeksforgeeks.org/operating-systems/file-allocation-methods/)

3. GeeksforGeeks. (2024). *Structures of Directory in Operating System*. Retrieved from [https://www.geeksforgeeks.org/structures-of-directory-in-operating-system/](https://www.geeksforgeeks.org/structures-of-directory-in-operating-system/)

4. GeeksforGeeks. (2024). *Disk Scheduling Algorithms*. Retrieved from [https://www.geeksforgeeks.org/disk-scheduling-algorithms/](https://www.geeksforgeeks.org/disk-scheduling-algorithms/)

### Technical Documentation

5. CodeLucky. (2026). *File System in Operating System: Complete Guide to Structure and Organization*. Retrieved from [https://codelucky.com/file-system-operating-system/](https://codelucky.com/file-system-operating-system/)

6. CodeLucky. (2026). *Directory Structure: Single-level, Two-level, and Tree Structure in Operating Systems*. Retrieved from [https://codelucky.com/directory-structure-operating-systems/](https://codelucky.com/directory-structure-operating-systems/)

7. CodeLucky. (2026). *File Allocation Methods: Contiguous, Linked and Indexed Storage Techniques*. Retrieved from [https://codelucky.com/file-allocation-methods/](https://codelucky.com/file-allocation-methods/)

8. CodeLucky. (2026). *Disk Scheduling Algorithms: FCFS, SSTF, SCAN, C-SCAN*. Retrieved from [https://codelucky.com/disk-scheduling-algorithms/](https://codelucky.com/disk-scheduling-algorithms/)

### Online Learning Resources

9. CompileNRun. (n.d.). *File System Implementation*. Retrieved from [https://www.compilenrun.com/docs/fundamental/os/os-implementation/file-system-implementation/](https://www.compilenrun.com/docs/fundamental/os/os-implementation/file-system-implementation/)

10. CompileNRun. (n.d.). *Directory Structure*. Retrieved from [https://www.compilenrun.com/docs/fundamental/os/file-systems/directory-structure/](https://www.compilenrun.com/docs/fundamental/os/file-systems/directory-structure/)

11. TutorialsArena. (2024). *Tree-Structured Directory Systems*. Retrieved from [https://www.tutorialsarena.com/fundamentals/os/os-tree-structured-directory](https://www.tutorialsarena.com/fundamentals/os/os-tree-structured-directory)

12. Scaler. (2024). *Directory Structure in OS*. Retrieved from [https://www.scaler.com/topics/directory-structure-in-os/](https://www.scaler.com/topics/directory-structure-in-os/)


### Industry and Professional Sources

13. GuruSoftware. (2024). *File Systems in Operating Systems: An In-Depth Guide*. Retrieved from [https://www.gurusoftware.com/file-systems-in-operating-systems-an-in-depth-guide/](https://www.gurusoftware.com/file-systems-in-operating-systems-an-in-depth-guide/)

14. Student Notes. (2026). *Operating System File Management: Structure, Implementation, and Operations*. Retrieved from [https://www.student-notes.net/operating-system-file-management-structure-implementation-and-operations/](https://www.student-notes.net/operating-system-file-management-structure-implementation-and-operations/)

15. Medium. (2024). *Optimizing Disk Performance: A Deep Dive into FCFS, SSTF, SCAN, and C-SCAN Algorithms*. Retrieved from [https://medium.com/@sahil.deogade03/optimizing-disk-performance-a-deep-dive-into-fcfs-sstf-scan-and-c-scan-algorithms-27d23ca06dbd](https://medium.com/@sahil.deogade03/optimizing-disk-performance-a-deep-dive-into-fcfs-sstf-scan-and-c-scan-algorithms-27d23ca06dbd)

16. CCBP. (2026). *Disk Scheduling Algorithms in Operating Systems*. Retrieved from [https://www.ccbp.in/blog/articles/disk-scheduling-algorithms-in-operating-systems](https://www.ccbp.in/blog/articles/disk-scheduling-algorithms-in-operating-systems)

17. KindaTechnical. (2026). *A Guide to Operating Systems - Disk Scheduling*. Retrieved from [https://kindatechnical.com/operating-systems/lesson-37-disk-scheduling.html](https://kindatechnical.com/operating-systems/lesson-37-disk-scheduling.html)

### Additional Resources

18. Intellipaat. (2026). *Disk Scheduling Algorithms in OS*. Retrieved from [https://intellipaat.com/blog/disk-scheduling-algorithms-in-os/](https://intellipaat.com/blog/disk-scheduling-algorithms-in-os/)

19. ExploringBits. (2022). *File Allocation Methods in Operating System*. Retrieved from [https://exploringbits.com/file-allocation-methods-in-operating-system/](https://exploringbits.com/file-allocation-methods-in-operating-system/)

20. TheLinuxCode. (2026). *Contiguous, Linked, and Indexed (With Modern 2026 Guidance)*. Retrieved from [https://thelinuxcode.com/file-allocation-methods-contiguous-linked-and-indexed-with-modern-2026-guidance/](https://thelinuxcode.com/file-allocation-methods-contiguous-linked-and-indexed-with-modern-2026-guidance/)

---

## APPENDIX A: GLOSSARY OF TERMS

**Block**: Fixed-size unit of storage on a disk, typically 512 bytes or 4KB

**Cylinder**: Set of tracks at the same distance from the center on all disk platters

**Directory**: Container for organizing files and subdirectories

**FCB (File Control Block)**: Data structure containing file metadata

**Fragmentation**: Wasted space resulting from inefficient storage allocation

**Inode**: Data structure storing file metadata in Unix-like systems

**Metadata**: Data about data; information describing file attributes

**Partition**: Logical division of a physical disk

**Sector**: Smallest addressable unit on a disk

**Seek Time**: Time for disk head to move to the target track

**Track**: Circular path on a disk platter where data is stored

**Volume**: Logical storage unit that may span multiple physical devices

---

## APPENDIX B: ALGORITHM PSEUDOCODE

### FCFS Algorithm
```
FCFS_Disk_Scheduling(request_queue, initial_position):
    total_movement = 0
    current_position = initial_position
    
    for each request in request_queue:
        movement = abs(request - current_position)
        total_movement += movement
        current_position = request
        service_request(request)
    
    return total_movement
```


### SSTF Algorithm
```
SSTF_Disk_Scheduling(request_queue, initial_position):
    total_movement = 0
    current_position = initial_position
    remaining_requests = copy(request_queue)
    
    while remaining_requests is not empty:
        closest_request = find_closest(remaining_requests, current_position)
        movement = abs(closest_request - current_position)
        total_movement += movement
        current_position = closest_request
        service_request(closest_request)
        remove(remaining_requests, closest_request)
    
    return total_movement

find_closest(requests, position):
    min_distance = infinity
    closest = null
    
    for each request in requests:
        distance = abs(request - position)
        if distance < min_distance:
            min_distance = distance
            closest = request
    
    return closest
```

### SCAN Algorithm
```
SCAN_Disk_Scheduling(request_queue, initial_position, direction):
    total_movement = 0
    current_position = initial_position
    
    sort(request_queue)
    
    if direction == "toward_0":
        left_requests = requests <= current_position (sorted descending)
        right_requests = requests > current_position (sorted ascending)
        
        # Service left side
        for each request in left_requests:
            movement = abs(request - current_position)
            total_movement += movement
            current_position = request
            service_request(request)
        
        # Move to track 0 if needed
        if current_position != 0:
            total_movement += current_position
            current_position = 0
        
        # Service right side
        for each request in right_requests:
            movement = abs(request - current_position)
            total_movement += movement
            current_position = request
            service_request(request)
    
    else: # direction == "toward_max"
        # Similar logic in opposite direction
    
    return total_movement
```

### C-SCAN Algorithm
```
C_SCAN_Disk_Scheduling(request_queue, initial_position, max_track):
    total_movement = 0
    current_position = initial_position
    
    sort(request_queue)
    
    right_requests = requests >= current_position (sorted ascending)
    left_requests = requests < current_position (sorted ascending)
    
    # Service right side toward max
    for each request in right_requests:
        movement = abs(request - current_position)
        total_movement += movement
        current_position = request
        service_request(request)
    
    # Move to max track
    if current_position != max_track:
        total_movement += (max_track - current_position)
        current_position = max_track
    
    # Jump to track 0
    total_movement += max_track
    current_position = 0
    
    # Service left side
    for each request in left_requests:
        movement = abs(request - current_position)
        total_movement += movement
        current_position = request
        service_request(request)
    
    return total_movement
```

---

## APPENDIX C: PRACTICAL EXAMPLES

### Example 1: File Allocation Comparison

**Scenario**: Store a 10KB file on a disk with 1KB blocks

**Contiguous Allocation:**
- Allocate blocks 100-109 (10 consecutive blocks)
- Directory entry: Start=100, Length=10
- Access time: Fast (sequential)
- Growth: Difficult (requires relocation)

**Linked Allocation:**
- Block 100 → Block 245 → Block 67 → ... → Block 189
- Directory entry: Start=100
- Access time: Slower (follow pointers)
- Growth: Easy (add blocks anywhere)

**Indexed Allocation:**
- Index block 100 contains: [245, 67, 123, 456, 789, 234, 567, 890, 345, 189]
- Directory entry: Index=100
- Access time: Moderate (one extra access for index)
- Growth: Moderate (may need larger index)

### Example 2: Directory Structure Navigation

**Tree Structure Example:**
```
/                           (root)
├── home/
│   ├── user1/
│   │   ├── documents/
│   │   │   ├── report.txt
│   │   │   └── data.csv
│   │   └── pictures/
│   │       └── photo.jpg
│   └── user2/
│       └── projects/
│           └── code.py
├── etc/
│   └── config.txt
└── var/
    └── log/
        └── system.log
```

**Path Examples:**
- Absolute: /home/user1/documents/report.txt
- Relative (from /home/user1): documents/report.txt
- Relative (from /home/user1/pictures): ../documents/report.txt

---

**Document Information:**
- **Title**: File Systems and Storage Management
- **Topic**: Operating Systems - Storage Management
- **Sections**: File System Structures, Directory Structures, Disk Scheduling
- **Word Count**: Approximately 5,500 words
- **Format**: Markdown (convertible to Word)
- **Date**: February 2026
- **Sources**: 20+ academic and technical references

---

**END OF DOCUMENT**
