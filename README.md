
---------------------------------------
🧠 GTA (Graph Topology Ablation) Challenge
---------------------------------------

This repository hosts the official evaluation system for the Graph Topology Ablation (GTA) challenge.
Participants submit predictions for ideal and perturbed topology settings.

All submissions are encrypted, automatically evaluated, and ranked on a public leaderboard.

Repository hosted on GitHub.

-------------------------------------------------------------------------------------------------------------
🏆 View Live Leaderboard: [Open leaderboard](https://idrees11.github.io/GTA-Graph-Topology-Ablation_-GTA-/)
--------------------------------------------------------------------------------------------------------------
---------------
🎯 Objective
---------------

Participants must generate predictions for two settings: 
```
✅ Ideal graph topology
✅ Perturbed graph topology
```
------------------------------
**⚙️ Perturbation Mechanism**
------------------------------
Two types of feature corruption are applied:
```
1️ Distribution Shift
    A constant offset is added to node features:
    x ← x + δ
    where δ = feature_shift (default 0.3)

    This simulates systematic measurement bias or domain shift.

2️ Gaussian Noise Injection
    Random noise is added to each feature:
    x ← x + ϵ,   ϵ ~ N(0, σ²)
    where σ = noise_std (default 0.05)

    This simulates noisy feature extraction.
```
--------------------------------
**Purpose of This Perturbation**
--------------------------------
```
This setup evaluates whether a GNN:

✔ relies on exact feature values
✔ generalizes under feature distribution shift
✔ remains stable under noisy topological descriptors

The model is trained on clean features and evaluated under corrupted features to measure robustness.
```

----------------------
📌Dataset Description
----------------------
```
We have used MUTAG Dataset: 

MUTAG is a classic benchmark dataset for graph classification originating from chemical informatics research.
It consists of molecular graphs representing small chemical compounds, with labels indicating whether each compound
exhibits mutagenic effects on a specific bacterium.

```

**🔗 Official Source**

The dataset is part of the TU Dortmund University graph kernel benchmark collection and can be downloaded from the official TU Dortmund repository:

📥 https://ls11-www.cs.tu-dortmund.de/people/morris/graphkerneldatasets/MUTAG.zip

**📊 Core Statistics**
```
Property                Value

Task                    Binary graph classification

Domain	                Chemical compounds (mutagenic vs non-mutagenic)

# of Graphs      	    188 graphs (benchmark size)

Avg. Nodes per Graph	~18 nodes
Avg. Edges per Graph	~40 edges
Node/Atom Features	    Categorical atom labels (interpreted as features)

# Classes	            2 (mutagenic / non-mutagenic)
```

Each graph represents a molecule:

Nodes correspond to atoms

Edges correspond to chemical bonds

Graph label indicates whether the molecule is mutagenic to Salmonella typhimurium or not.

-----------------------
**📊 Evaluation metrics:**
----------------------

In GTA (Graph Topology Ablation), model performance is evaluated using the F1 score rather than simple accuracy.

The F1 score is used because it balances:

correct predictions

false positives

false negatives

This provides a more reliable measure of classification performance than accuracy alone.

**Each submission is evaluated under two conditions:**

F1 Score (Ideal)     — performance on clean topological features

F1 Score (Perturbed) — performance on corrupted topological features

To measure stability, we compute:

Robustness Gap = |F1 Ideal − F1 Perturbed|

A smaller robustness gap indicates a more stable and reliable model.

🏁 Ranking Priority
```
1️⃣ Highest Perturbed F1 Score
2️⃣ Lowest Robustness Gap
3️⃣ Most recent submission
```
--------------------------
📂 Repository Structure
--------------------------
```
gnn-topology-ablation/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── scoring_script.py              # Computes F1 scores and robustness gap
├── leaderboard_system.py          # Leaderboard update engine
├── scores.json                    # Temporary scoring output (auto-generated)
│
├── submissions/                   # Participant encrypted submissions (.enc files)
│
├── starter_code/                  # Starter implementation for participants
│
├── data/                          # Evaluation dataset + references
│   ├── train.csv                  # Training reference file
│   ├── test.csv                   # Test reference file
│   └── TUDataset/
│       └── MUTAG/
│
├── leaderboard/                   # Public leaderboard outputs
│   ├── leaderboard.md
│   └── leaderboard_history.csv
│
├── keys/                          # Encryption keys
│   └── public_key.pem             # Organiser RSA public key
│
├── .github/
│   └── workflows/
│       └── score_submission.yml   # Automated scoring pipeline
│
└── readme                         # Additional documentation

```
--------------------
⚙️ Getting Started
--------------------

**Clone the repository:**

git clone https://github.com/idrees11/gnn-topology-ablation.git 

**cd gnn-topology-ablation**


**Install dependencies:**

pip install -r requirements.txt


**Generate prediction files:**

submissions/ideal_submission.csv

submissions/perturbed_submission.csv

**Format of these files should be**

```
graph_index,target

160,1
62,0
48,0
173,1
109,1
129,0
.....
```
---------------------------------------------------
🔐 Secure Submission Format (AES + RSA Encryption)
---------------------------------------------------

All prediction files must be encrypted before submission.

**Encryption design:**

```
✔ Prediction files encrypted using AES-256
✔ AES key encrypted using RSA public key
✔ Only organiser can decrypt submissions
```

**Public key provided in:**

keys/public_key.pem


Private key is securely stored by organiser and never shared.

----------------------
📦 Files to Submit
---------------------

Your Pull Request must contain ONLY:
```
submissions/ideal_submission.enc
submissions/perturbed_submission.enc
submissions/aes_key.enc
```
**❌ Do NOT upload**
```
Raw CSV files
AES key .hex files
```
Unencrypted predictions

-----------------------------------
🧩 Encryption Steps (Run Exactly)
-----------------------------------

**🔹 Step 1 — Generate AES key**

           openssl rand -hex 32 > submissions\aes_key1.hex

**🔹 Step 2 — Encrypt CSV files using AES key**

**Encrypt ideal predictions:**

           openssl enc -aes-256-cbc -pbkdf2 -in submissions\ideal_submission.csv -out submissions\ideal_submission.enc -pass  
           file:submissions\aes_key.hex


**Encrypt perturbed predictions:**

           openssl enc -aes-256-cbc -pbkdf2 -in submissions\perturbed_submission.csv -out submissions\perturbed_submission.enc -pass 
           file:submissions\aes_key.hex

**🔹 Step 3 — Encrypt AES key using organiser RSA public key**

           openssl pkeyutl -encrypt -pubin -inkey keys\public_key.pem -in submissions\aes_key.hex -out submissions\aes_key.enc


**If multiple AES keys are used:**

           openssl pkeyutl -encrypt -pubin -inkey keys\public_key.pem -in submissions\aes_key_perturbed.hex -out submissions\aes_key_perturbed.enc

-------------------------
🚀 Submission Procedure
-------------------------
```
1️⃣ Fork the repository
2️⃣ Place encrypted files inside submissions/
3️⃣ Create a new branch
4️⃣ Commit ONLY .enc files
5️⃣ Open a Pull Request
```
Submissions are evaluated automatically.

----------------------------------
🤖 Automated Evaluation Pipeline
----------------------------------

When a Pull Request is opened:
```
1️⃣ AES key is decrypted using organiser private RSA key
2️⃣ Prediction files are decrypted
3️⃣ Evaluation metrics are computed
4️⃣ Scores are written to scores.json
5️⃣ Leaderboard is updated automatically
```
Participants never see decrypted predictions.

-----------------------
🏆 Leaderboard System
-----------------------

Leaderboard is generated by:

leaderboard_system.py


It maintains:
```
✔ Full submission history
✔ Best score per participant
✔ Public ranking
```
Generated outputs:
```
leaderboard/leaderboard.md
leaderboard/leaderboard.json
leaderboard/leaderboard_history.csv
```
**📊 Leaderboard Ranking Logic**

For each submission the system records:
```
✔Participant name
✔F1 Ideal
✔F1 Perturbed
✔Robustness Gap
✔Timestamp
```
Best submission per participant is selected using:

Sort priority:
```
1) Highest perturbed score
2) Lowest robustness gap
3) Latest timestamp
```
**Track Live leaderboard:** [Leaderboard](leaderboard/leaderboard.md)
----------------------
🔒 Security Guarantee
---------------------
```
✔ Predictions encrypted locally
✔ AES key encrypted using RSA public key
✔ Only organiser can decrypt
✔ Files visible but unreadable
✔ Ensures blind evaluation
```
----------------
📜 License
----------------

Released under the MIT License.
-----------------------------------------------------------------------------------------------------------------------



This dataset comprises street network graphs for 120 diverse cities across continents including North America, South America, Europe, Asia, Africa, Australia & Oceania, and others like the Middle East and Central Asia. The graphs are extracted from OpenStreetMap using OSMnx, focusing on driveable roads within a 500-meter buffer around each city's central point.

The dataset includes a total of 120 cities with an unbalanced distribution of street network types reflecting real-world urban patterns: 37 grid cities (such as planned orthogonal layouts like Salt Lake City, USA), 31 organic cities (such as irregular, historic winding streets like Boston, USA), and 52 hybrid cities (such as mixed elements like Atlanta, USA).

Each city's data is stored as a serialized NetworkX graph in `.pkl` format within the `data` folder, including nodes (intersections with coordinates), edges (roads with lengths and geometries), and graph attributes for layout `type` (grid/organic/hybrid) and city `name`.

This dataset is ideal for urban planning analysis, graph theory, or machine learning tasks like layout classification. It was generated via a Python script using OSMnx and NetworkX.


The goal of Task 3 is to train a model to classify each city's street layout into one of three classes:

- `0` = **organic**
- `1` = **grid**
- `2` = **hybrid**

Participants will train on the **train set** and submit predictions for the **test set** as a `submission.csv`.

---

## Environment setup

Before training or submitting, set up a Python environment and install dependencies.

### 1. Create a virtual environment

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

From the **project root** (where `requirements.txt` is):

**Linux / macOS:**
```bash
pip install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

(If you use the starter-code baseline, also install its dependencies: `pip install -r starter_code/requirements.txt`.)

---

## Dataset Summary

- Class distribution in the full dataset:
  - **organic**: 31
  - **grid**: 37
  - **hybrid**: 52

Each city graph is stored as a serialized NetworkX graph (`.pkl`) and contains:
- **nodes**: intersections with coordinates (`x`, `y`)
- **edges**: road segments (may include attributes such as length/geometry depending on OSM)
- **graph attributes** (e.g., city name).  
For the **test set**, the label attribute is removed.

This dataset is useful for urban planning analysis, graph learning, and layout classification tasks.

---

## Data Split (Train/Test)
The dataset is split into **70/30** with **stratification by class**:

- `data/train/` : labeled graphs (70%)
- `data/test/`  : unlabeled graphs (30%)

Training labels are provided in:
- `data/train_labels.csv` with columns:
  - `filename`
  - `target`

---

## What You Need To Do (Participant)

### Step 1: Train
Train your model using:
- graphs in `data/train/`
- labels in `data/train_labels.csv`

### Step 2: Predict
Predict labels for every graph in:
- `data/test/`

### Step 3: Prepare your submission file
Create a CSV with columns `filename` and `prediction` (same format as `submissions/sample_submission.csv`):

```csv
filename,prediction
Boston_Massachusetts_USA.pkl,2
Delhi_India.pkl,0
Turin_Italy.pkl,1
...
```

Save it as a `.csv` file (e.g. `my_submission.csv`) in the **`submissions/`** folder.  
**Note:** `.csv` files in `submissions/` are git-ignored, so your raw submission will not be pushed. You will submit an **encrypted** version instead.

### Step 4: Encrypt your submission
From the project root, run the encryption script so it can find your CSV and the encryption key:

**Linux / macOS:**
```bash
cd submissions
python encrypt_submissions.py
cd ..
```

**Windows (Command Prompt):**
```cmd
cd submissions
python encrypt_submissions.py
cd ..
```

**Windows (PowerShell):**
```powershell
cd submissions
python encrypt_submissions.py
cd ..
```

This creates a `.enc` file next to each `.csv` in `submissions/` (e.g. `my_submission.csv.enc`). Only `.enc` files are tracked by git; your `.csv` stays local.

### Step 5: Push your encrypted submission
Commit and push the new `.enc` file(s) to the repository (e.g. open a Pull Request or push to the main branch, as per the challenge rules). The automated pipeline will decrypt and score the **latest** `.enc` file in `submissions/` and update the leaderboard.

---

## Project directory structure

Below is the layout of the repository (relevant to competitors). Run `tree -a -I '.git|.venv|__pycache__' --dirsfirst` from the project root to print it locally (if `tree` is installed).

```
.
├── .env.example          # Example env file; organisers use .env for secrets (e.g. test labels).
├── .github/
│   ├── scripts/
│   │   └── process_submission.py   # CI script: finds latest .enc, decrypts, updates leaderboard.
│   └── workflows/
│       └── process_submission.yml # Runs on push to main.
├── data/
│   ├── train/            # Training city graphs (.pkl).
│   ├── test/             # Test city graphs (.pkl), no labels.
│   └── train_labels.csv  # Labels for files in data/train/.
├── encryption/
│   ├── encrypt.py        # Used by encrypt_submissions.py (reads public_key.pem).
│   ├── decrypt.py        # Used by CI to decrypt .enc submissions.
│   ├── generate_keys.py  # For organisers; generates key pair.
│   └── public_key.pem    # Public key used to encrypt submissions.
├── leaderboard/          # Leaderboard logic and assets (scores, CSV, HTML).
├── starter_code/
│   ├── baseline.py       # Example GCN baseline (train + predict).
│   └── requirements.txt # Extra deps for baseline (e.g. PyTorch).
├── submissions/
│   ├── encrypt_submissions.py  # Run this (from submissions/) to turn .csv → .enc.
│   ├── sample_submission.csv  # Format reference (filename, prediction).
│   └── *.csv.enc         # Your encrypted submissions; push these.
├── leaderboard.md        # Auto-generated leaderboard markdown.
├── README.md             # This file.
├── requirements.txt      # Root Python dependencies (encryption, scoring, etc.).
├── scoring_script.py     # Local scoring helper (needs test labels).
└── index.html            # Project index / redirect if used.
```

---

## Baseline Model (GCN) — Details

The provided baseline is a **Graph Convolutional Network (GCN)** for **graph-level classification** (one label per city graph).

### Input
Each city is a graph `G` stored as a `.pkl` NetworkX file.

- Nodes: intersections with coordinate attributes `x` and `y`
- Edges: road connections between intersections

### Node Features Used (per node)
For each node, we build a 3D feature vector:

1. **Centered & scaled x-coordinate**
2. **Centered & scaled y-coordinate**
3. **Normalized node degree**

So the node feature matrix is:

- `X ∈ R^(N×3)` where `N` = number of nodes in the city graph.

### Adjacency (GCN Normalization)
The baseline builds a sparse adjacency matrix with self-loops and applies standard GCN normalization:

Normalized adjacency: D^{-1/2}(A+I)D^{-1/2}

This improves stability compared to using a raw adjacency matrix.

### Model Architecture
The baseline uses two GCN-style message passing layers (implemented with sparse matrix multiplication) and then a graph pooling step:

- Layer 1: `X -> hidden`
- Layer 2: `hidden -> hidden`
- Pooling: concatenate **mean pooling** + **max pooling** to get a graph embedding
- Classifier: linear layer to output 3 logits (organic/grid/hybrid)

Training uses:
- Adam optimizer
- Cross-entropy loss
- class weights (helps if classes are imbalanced)
- dropout + weight decay (regularization)

### Validation
To provide a baseline metric without touching the hidden test labels, the script splits the training set internally:

- 70% train
- 30% validation (stratified)

It prints:
- Validation Accuracy
- Validation Macro-F1 (main metric)

### Output
After training, the baseline predicts on the unlabeled test graphs. Save your predictions in the required format and place the CSV in `submissions/`, then encrypt with `submissions/encrypt_submissions.py` and push the resulting `.enc` file(s).

Format of the submission CSV:
```csv
filename,prediction
City1.pkl,2
City2.pkl,0
...
```
<<<<<<< HEAD



---------

To ensure all participants use consistent inputs, we provide a helper script (`utils.py`) to load the **Adjacency Matrix ($A$)** and **Node Feature Matrix ($X$)** directly from the raw files.

### 1. Adjacency Matrix ($A$)
- **Format:** Sparse Matrix ($N \times N$)
- **Description:** Represents the street connectivity. $A_{ij} = 1$ if an intersection exists between node $i$ and node $j$.

### 2. Node Feature Matrix ($X$)
- **Format:** Continuous Matrix ($N \times 2$)
- **Description:** Represents the spatial geometry of the city.
  - **Column 0:** Centered X-coordinate (Longitude)
  - **Column 1:** Centered Y-coordinate (Latitude)
- *Note: While identity features are acceptable as a baseline, we explicitly provide spatial coordinates to enable geometric deep learning.*

### 3. How to Load
Use the provided `load_city_graph` function in your training script:

```python
from utils import load_city_graph

# Example: Load the first training graph
# Returns:
#   A: Scipy Sparse Adjacency Matrix
#   X: Numpy Feature Matrix (Geometric)
#   label: The target class (0, 1, or 2)
A, X, label = load_city_graph("gnn_challenge/data/train/Boston_Massachusetts_USA.pkl")

print(f"Adjacency Shape: {A.shape}") # (N, N)
print(f"Feature Shape:   {X.shape}") # (N, 2)
=======
>>>>>>> 1a0d3b2645b127c72b75e9723caae2a03d1e9f55
