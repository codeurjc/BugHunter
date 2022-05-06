# Regression Seeker

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6522906.svg)](https://doi.org/10.5281/zenodo.6522906)

Reproduction package for the paper "Hunting bugs: Towards an automated approach to identifying which change caused a bug through regression testing", presented to ASE 2022 (still under review). 

This repository contains the tool that allows, from a commit that fixes a bug and a test that reveals this bug, to find the commit that introduced the bug. 
It also includes a collection of Jupyter Notebooks to analyze in detail the results of the tool.

This package contains:

```
.
├── analysis        # Jupyter Notebooks for data  analysis
├── configFiles     # Config files for each project
├── dockerfiles     # Docker files for all necessary images to perform the experiment
├── projects        # Subjects of the experiment (git repositories)
├── py              # Python scripts to perform the experiment
├── results         # Results generate from the experiment
├── scripts         # Bash scripts to easy-perform the experiment
├── tmp             # Folder for temporary files
└── README.md 
```

## SetUp

### Requirements

- Git >= 2.25
- Docker >= 20.10 (used: build f0df350)

### Build images

In order to use the tool, the following docker images are required to use the tool:

- __Defects4J image__
```
docker build -f dockerfiles/defects4j/defects4j.Dockerfile -t defects4j:2.1.0 .
```

- __RegTestExecutor image__
```
docker build -f dockerfiles/regression-seeker.Dockerfile -t regression-seeker:0.2.2 .
```

> If in later steps the container generated from this image does not have permissions on Docker, you must build the image using the GID of the Docker socket as argument
```
DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
docker build --build-arg DOCKER_GID=$DOCKER_GID -f dockerfiles/regression-seeker.Dockerfile -t regression-seeker:0.2.2 .
```
- __Analysis image__
```
docker build -f dockerfiles/analysis.Dockerfile -t regression-seeker-analysis:0.1.1 .
```

## Conducting the experiment
The experiment was carried out in 3 phases/steps:

1. Extract bug information from the Defects4J dataset.
2. Execution of the regression test in the past (per bug)
3. Analysis of the results

## Step 1. Extract bug information from the Defects4J dataset

To carry out the experiment, we will use the [Defects4J](https://github.com/rjust/defects4j) dataset, which has a simple API to obtain the information of the bugs .
and is stored in the folder configFiles/.

This step generates a configuration file in JSON format with all the bug information (as shown below) and is stored in the folder `configFiles/`

```
{
    "id": "1",
    "project": "Closure",
    "git_url": "D4J",
    "docker_image": "defects4j:2.1.0",
    "bug_report": "https://storage.googleapis.com/google-code-archive/v2/code.google.com/closure-compiler/issues/issue-253.json",
    "fix_commit": "1dfad5043a207e032a78ef50c3cba50488bcd300",
    "build": "ant -Dd4j.project.id=Closure compile",
    "build_test": "ant -Dd4j.project.id=Closure compile.tests",
    "test_command": "ant -Dd4j.project.id=Closure -Dtest.entry.class=com.google.javascript.jscomp.CommandLineRunnerTest -Dtest.entry.method=testSimpleModeLeavesUnusedParams run.dev.tests",
    "folder": "test/com/google/javascript/jscomp/",
    "file": "CommandLineRunnerTest.java",
    "test_report": "target/surefire-reports/TEST-com.google.javascript.jscomp.CommandLineRunnerTest.xml"
}
```

In order to generate these files automatically, a file called `project-config.json` has been generated manually for each project to provide structure to the configuration files created.

### How to reproduce

To extract the information of each bug, we use the following command:
```
$ ./scripts/runExtractBugsD4J.sh <project_name>
```

## Step 2. Execution of the regression test in the past (per bug)

### Experiment process

From the configuration files generated in the previous step, we run the experiment. This experiment consists of:

1) Read the bug configuration file
2) Clone the repository (in the case of Defects4J, this is done through its tool).
3) Execute the test that reveals the bug in the bug fixing commit (BFC) and check that the test succeeds.
4) Execute the test that reveals the bug in the commit before the BFC and check that it fails
5) Execute the test that reveals the bug in all previous commits

In the steps that execute regression tests, the tool follows this procedure: 

1) Checkout the corresponding commit
2) Transplant (copy) the regression test
3) Compile the source code
4) Compile the regression test
5) Execute the regression test. 

### Experiment results

For each bug, the following information is obtained:

- The result of compiling the source code, compiling the test code and running the regression test in JSON format.
- The logs of each of these three phases
- The test report generated

The results of this step (which we will call raw results) can be found in Zenodo (https://zenodo.org/record/6522906) as `raw-results.tar.gz` (15GB).

### How to reproduce

To run the experiment on a bug, we use the following command:
```
$ ./scripts/runExperiment.sh <project> <bug_id>
```

## Step 3. Analysis of the results

For this step you will need to have started a Docker container using the image built in set up (`regression-seeker-analysis`)

```
$ ./scripts/runNotebook.sh
```

### 3.1 Analysis of raw results

The analysis of the results is easily visualized through a Jupyter Notebook.

- [Open notebooks in browser](http://localhost:9000/notebooks/analysis/Analysis.ipynb)
- [Open notebooks in Gitlab/GitHub](analysis/Analysis.ipynb)

This notebook:

- Performs a bug introducing change (BIC) search.
- Analyzes and displays results that answer `RQ0: "Can regression tests be transplanted to the past?"`
- Analyzes and displays results that answer `RQ1: "Can the BIC for a given bug be found using its regression test?"`

When running all notebook cells, processed results are generated in the `analysis/results/` folder.

The results of this step (which we will call processed results) can be found in Zenodo (https://zenodo.org/record/6522906) as `processed-results.tar.gz` (300MB).

### 3.2 Generare BIC dataset

From the results obtained in the previous step (processed results) a BIC dataset is generated through a JupyterNotebook.

- [Open notebooks in browser](http://localhost:9000/notebooks/analysis/GenerateDatasetOfBugs.ipynb)
- [Open notebooks in Gitlab/GitHub](analysis/GenerateDatasetOfBugs.ipynb)

The result of executing all the cells of this notebook is the CSV file `analysis/regressions.csv`, included in the Git repository.

### 3.3 Evaluation of SZZ derivatives

Once the dataset has been generated in the previous step, in this step we will use it to test the performance and evaluate different derivations of the SZZ algorithm. 

All SZZ derivations are part of this repository and are located in `py/szz/`. A suite of adapters has been generated to facilitate the use of these algorithms using Python code:

- OpenSZZ.py
- PySZZ.py
- SZZUnleashed.py

These algorithms will use the project's git repository and the configuration file generated in Step 1. The latter file must be adapted to include additional information required by these algorithms (date the fix was created, date the issue was opened and date the issue was closed). To adapt this configuration file, the following command is provided:

```
$ ./scripts/adaptAllIssues.sh
```

The execution of the SZZ algorithms on the detected regressions is automated through the scripts located in `scripts/szz/`. 

```
$ scripts/szz/run<SZZ_Algorithm>.sh
```

The results of the execution of these algorithms are part of the `raw results` mentioned above and are available at Zenodo (https://zenodo.org/record/6522906).

To visualize the results of these derivations of the SZZ and answer the `RQ2: How precise are SZZ derivatives in detecting the change that introduced a bug?`, we will use again a JupyterNotebook

- [Open notebooks in browser](http://localhost:9000/notebooks/analysis/EvaluationOfSZZDerivatives.ipynb)
- [Open notebooks in Gitlab/GitHub](analysis/EvaluationOfSZZDerivatives.ipynb)

### 3.4 Comparing our dataset

To validate our dataset, we checked our results with those of a popular BIC benchmark, [InduceBenchmark](https://github.com/justinwm/InduceBenchmark) which includes BICs for the Defects4J dataset.

The analysis of the common BICs (whether the identification matches or not) together with how the different algorithms behave (the derivations of the SZZ and our proposal) can be found in a Jupyter Notebook.

- [Open notebooks in browser](http://localhost:9000/notebooks/analysis/EvaluationOfSZZDerivatives.ipynb)
- [Open notebooks in Gitlab/GitHub](analysis/EvaluationOfSZZDerivatives.ipynb)
