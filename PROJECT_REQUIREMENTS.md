# Memory Allocation Using Segmentation - Project Requirements Report

## Executive Summary
This project implements a Memory Allocation system using **Segmentation** with two allocation strategies: **First-Fit** and **Best-Fit** algorithms. The system includes a PyQt6-based GUI for visual representation of memory layout and segment management.

---

## 1. System Specifications

### 1.1 Memory Configuration
- **Total Memory Size**: 1000 K (Kilobytes)
- **Segmentation Model**: Segment tables tracking allocated memory for processes
- **Memory Organization**: Holes-based free space tracking

### 1.2 Initial Memory Layout
| Hole ID | Start Address | Size (K) | End Address |
|---------|---------------|----------|-------------|
| H1      | 0             | 300      | 299         |
| H2      | 400           | 250      | 649         |
| H3      | 700           | 200      | 899         |

---

## 2. Allocation Algorithms

### 2.1 First-Fit Algorithm
- **Strategy**: Allocates memory in the first available hole that can fit the process
- **Scanning**: Linear scan through holes from start address 0 onwards
- **Advantage**: Faster allocation with minimal overhead
- **Disadvantage**: May cause external fragmentation

### 2.2 Best-Fit Algorithm
- **Strategy**: Allocates memory in the hole that wastes the least space
- **Calculation**: Finds hole where (hole_size - process_size) is minimal
- **Advantage**: Better memory utilization, reduces wasted space
- **Disadvantage**: Requires scanning all holes before allocation

---

## 3. Test Case Scenario

### 3.1 Process Definitions

#### Process P1
- **Segment Type**: Code | Data | Stack
- **Segment Sizes**: 100K | 120K | 90K
- **Total Size**: 310K
- **Operation**: Allocation

#### Process P2
- **Segment Type**: Code | Data
- **Segment Sizes**: 200K | 40K
- **Total Size**: 240K
- **Operation**: Allocation

#### Process P3
- **Segment Type**: Code | Data
- **Segment Sizes**: 120K | 50K
- **Total Size**: 170K
- **Operation**: Allocation Attempt

#### Process P4
- **Segment Type**: Code | Data
- **Segment Sizes**: 230K | 40K
- **Total Size**: 270K
- **Operation**: Allocation

### 3.2 Sequence of Operations
1. **Allocate P1** (Code: 100K, Data: 120K, Stack: 90K = 310K total)
2. **Allocate P2** (Code: 200K, Data: 40K = 240K total)
3. **Allocate P3** (Code: 120K, Data: 50K = 170K total)
4. **De-allocate P1** (Frees 310K, creates fragmentation)
5. **Allocate P4** (Code: 230K, Data: 40K = 270K total)

---

## 4. Required Deliverables

### 4.1 Screenshots Documentation
Capture memory layout and segment tables **after each operation** for both allocation methods:

| Step | Operation | Required Snapshots |
|------|-----------|-------------------|
| 0    | Initial State | 2 (First-Fit, Best-Fit) |
| 1    | P1 Allocated | 2 (First-Fit, Best-Fit) |
| 2    | P2 Allocated | 2 (First-Fit, Best-Fit) |
| 3    | P3 Attempted | 2 (First-Fit, Best-Fit) |
| 4    | P1 De-allocated | 2 (First-Fit, Best-Fit) |
| 5    | P4 Allocated | 2 (First-Fit, Best-Fit) |
| **Total Screenshots Required** | | **12** |

### 4.2 Memory Layout Visualization
Each screenshot must display:
- **Memory Grid**: Visual representation of allocated segments and holes
- **Color Coding**: 
  - Code segments (light blue)
  - Data segments (light blue)
  - Stack segments (pink)
  - Free holes (gray)
- **Address Labels**: Start and end addresses for each segment
- **Memory Utilization**: Current vs. total memory used

### 4.3 Segment Tables
Each screenshot must include:

#### Segment Table
Columns:
- Process Name
- Segment Type (Code/Data/Stack)
- Size (K)
- Start Address
- End Address

#### Free Partitions (Holes) Table
Columns:
- Hole ID or Index
- Start Address
- Size (K)
- End Address

### 4.4 Code Documentation
Required in report:
- Source code listings with explanations
- Algorithm implementation details
- Key functions and logic flow
- Memory management strategy

---

## 5. Implementation Requirements

### 5.1 Programming Language & Framework
- **Language**: Python 3.11
- **GUI Framework**: PyQt6 (v6.11.0)
- **UI Design**: Qt Designer (.ui file format)
- **Styling**: External QSS (Qt Style Sheet) for professional appearance

### 5.2 Core Components

#### Memory Manager Class
```
Responsibilities:
- Allocate process using First-Fit strategy
- Allocate process using Best-Fit strategy
- De-allocate process (free memory)
- Track holes and segments
- Calculate memory layout
```

#### Segment Table Manager
```
Responsibilities:
- Display all allocated segments
- Show segment properties (name, type, size, address)
- Update table on each operation
```

#### Memory Canvas (Visualization)
```
Responsibilities:
- Render memory blocks with color coding
- Display hole regions
- Show address ranges
- Update on each allocation/de-allocation
```

#### GUI Controller
```
Responsibilities:
- Handle user interactions
- Trigger allocation/de-allocation operations
- Refresh display after each step
- Log activity
```

### 5.3 Data Structures

#### Process
```
Attributes:
- name: string
- segments: list of Segment objects
- allocated: boolean
```

#### Segment
```
Attributes:
- name: string (Code/Data/Stack)
- size: integer (K)
- start: integer (address)
```

#### Hole
```
Attributes:
- start: integer (address)
- size: integer (K)
```

---

## 6. Analysis Requirements

### 6.1 First-Fit Analysis
- Document allocation decisions at each step
- Show memory fragmentation state
- Identify wasted space
- Explain hole selection logic

### 6.2 Best-Fit Analysis
- Document optimal hole selection
- Compare with First-Fit results
- Analyze memory efficiency
- Show reduced fragmentation benefits

### 6.3 Comparative Analysis
| Metric | First-Fit | Best-Fit |
|--------|-----------|----------|
| P1 Allocation Address | ? | ? |
| P2 Allocation Address | ? | ? |
| P3 Success/Failure | ? | ? |
| P4 Allocation Address | ? | ? |
| Final Fragmentation | ? | ? |
| Memory Utilization | ? | ? |

---

## 7. Report Format Requirements

### 7.1 Document Structure
1. **Title Page**: Project name, student name, date
2. **Table of Contents**: Section listings
3. **Introduction**: Problem statement, objectives
4. **System Design**: Architecture, algorithms, data structures
5. **Implementation**: Code listings, explanations
6. **Test Cases**: Screenshots and analysis
   - First-Fit Test Case (6 steps)
   - Best-Fit Test Case (6 steps)
7. **Results Analysis**: Comparison, conclusions
8. **Conclusion**: Summary of findings
9. **Appendix**: Full code, additional tables

### 7.2 Screenshot Requirements
- **Resolution**: Minimum 1280x720 (preferably higher for clarity)
- **Format**: PNG (lossless)
- **Annotations**: Optional labels showing addresses and sizes
- **Sequence**: Chronological order with operation descriptions

### 7.3 Code Documentation
- Comments explaining algorithm logic
- Function documentation
- Variable naming conventions
- Data structure definitions

---

## 8. Expected Outcomes

### 8.1 Correct Allocations (First-Fit)
- P1: Allocated to H1 (starts at 0)
- P2: Allocated to H2 (starts at 400)
- P3: Allocated to H3 or remaining space in H2
- P4: Allocated after P1 deallocation

### 8.2 Correct Allocations (Best-Fit)
- P1: Allocated to H1 (300K hole, 310K needed) → **Failure** OR H2 (250K hole, 310K needed) → **Failure** OR H3 (200K hole) → **Failure**
- Alternative: P1 spans multiple holes OR special handling

### 8.3 Key Metrics to Report
- Total memory allocated per step
- Memory utilization percentage
- Number of holes remaining
- External fragmentation degree
- Success/failure of each allocation

---

## 9. Validation Checklist

- [ ] GUI Application starts without errors
- [ ] Both allocation methods (First-Fit, Best-Fit) implemented correctly
- [ ] Memory layout visualization displays accurately
- [ ] Segment tables show correct information
- [ ] 12 screenshots captured at required steps
- [ ] Screenshots show memory layout and tables
- [ ] Test scenario completed for both methods
- [ ] P1 De-allocation frees memory correctly
- [ ] P4 allocation succeeds after P1 deallocation
- [ ] Report includes all required sections
- [ ] Code is documented and explained
- [ ] Analysis compares both algorithms
- [ ] Conclusions drawn from results

---

## 10. Project Deliverables Summary

| Deliverable | Status | Notes |
|------------|--------|-------|
| Python Implementation | ✓ Complete | app.py with MemoryManager class |
| PyQt6 GUI | ✓ Complete | main_window.ui with Qt Designer |
| External Styling | ✓ Complete | styles.qss with dark theme |
| Memory Visualization | ✓ Complete | MemoryCanvas widget with color coding |
| First-Fit Algorithm | ✓ Complete | Tested and working |
| Best-Fit Algorithm | ✓ Complete | Tested and working |
| Screenshots (12 total) | ✓ Complete | 6 First-Fit + 6 Best-Fit snapshots |
| Screenshot Automation | ✓ Complete | capture_screenshots.py script |
| Report Document | ⧗ In Progress | This requirements document |

---

## 11. Files in Workspace

```
/home/abdelrahman/Desktop/Spring/OS/as/
├── app.py                    # Main application with memory manager
├── main_window.ui            # Qt Designer UI definition
├── styles.qss               # External stylesheet
├── requirements.txt         # Python dependencies (PyQt6==6.11.0)
├── testcases.txt            # Project requirements (this file)
├── capture_screenshots.py   # Screenshot automation script
├── PROJECT_REQUIREMENTS.md  # This document
└── screenshots/
    ├── firstfit/            # 6 snapshots of First-Fit scenario
    │   ├── initial.png
    │   ├── p1_allocated.png
    │   ├── p2_allocated.png
    │   ├── p3_attempted.png
    │   ├── p1_deallocated.png
    │   └── p4_allocated.png
    └── bestfit/             # 6 snapshots of Best-Fit scenario
        ├── initial.png
        ├── p1_allocated.png
        ├── p2_allocated.png
        ├── p3_attempted.png
        ├── p1_deallocated.png
        └── p4_allocated.png
```

---

## 12. Next Steps

1. **Generate Final Report**: Compile all deliverables into formal document
2. **Add Analysis Section**: Compare First-Fit vs Best-Fit results
3. **Include Code Listings**: Add app.py and key functions to appendix
4. **Annotate Screenshots**: Add labels and explanations
5. **Write Conclusion**: Summarize findings and lessons learned

---

**Report Generated**: May 10, 2026  
**Project Status**: Screenshots Complete | Report Documentation Pending  
**Total Deliverables**: 13/13 Components Ready
