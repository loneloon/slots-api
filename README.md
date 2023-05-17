# Slots API

* Flask based API returning a randomly generated matrix with an array of symbol combinations found in that matrix.
* Default size of the matrix is set to 7x7. Default minimum number of symbols in a cluster to qualify for a combination is set to 5.
* Only vertical and horizontal-adjacent cells containing the same symbol qualify for a cluster.

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install the list of dependencies found in the root of the project
```
pip install -r requirements.txt
```

## Usage

Run main.py to start the API. By default it's listening on localhost:8000.

GET request on localhost:8000/ will return a json with a matrix map ( key=XYposition, value=symbol ) and an array of clusters with symbol coordinates.
