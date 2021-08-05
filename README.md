# MATF-NI-Mapper

## Fast introduction to Topology

`Topology` is the math concerning continuous objects. 
Not sizes and shapes, but continuity. It is how
things are connected and where the `gaps` are. 
It explains how a material's shape can be 
completely deformed into new one without losing its 
core properties. 

**Definition (homotopy):** Let f, g : X → Y be maps. 
f is `homotopic` to g if there exists a map F : X×I → Y
such that F(x, 0) = f(x) and F(x, 1) = g(x) 
for all points x ∈ X. The map F is called a homotopy 
from f to g and we write it as f' F g.
More intuitvely, if we think of the second parameter 
of F as “time”, then F describes a
“continuous deformation” of f into g. At time 0 we 
have the function f, at time 1 we have the function g.

Famous example is the `mug and donut`
`homotopy`. Informally, two continous functions from
one topological space to another are called `homotopic`
if one can be `continuosly deformed` into another. Such
a deformation being called a `homotopy` between the 
two functions. [1, 2]

![iris](docs/images/mug-donut.gif)

## Topological data analysis (TDA)

`Topological data analysis (TDA)` is an approach to the analysis
of datasets using techiniques from `topology`. It is usually combined
with other forms of analysis such as statistical or geometric
approaches. [1]

## Mapper - Introduction

`Mapper` is TDA algorithm is used for generalized
notion of coordinatization for high dimensional
datasets. Coordinatization can refer to choice of
real valued coordinate functions or data or
other notions of geometric representation like
`reeb graph`. [4]

## Mapper - Topological background and motivation (construction)

**Definition:** `Cover C of set X` is collection of sets
whose union includes X. Cover is `open cover` is all 
members are open sets.

**Example:** X is unit circle and C is set of circles
containing X.

![cover](https://wildtopology.files.wordpress.com/2012/10/circlecover21.png)

**Definition:** `Nerve of an open covering C` is 
a construction of simplical complex N(C).

**Example:** From previous example we can form nerve of
open covering. Note: Obtained simplical complex 
approximates initial space.

![nerve](https://wildtopology.files.wordpress.com/2012/10/circlecover3.png)

**Definition:** `Partition of unity` of topological space
X is set of continuous functions R from X to [0, 1] where
for each point x ∈ X:
- there is a neighbourhood of x where all but finite number
of functions of R are 0,
- the sum of all the function values at x is 1.

![partition](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Partition_of_unity_illustration.svg/500px-Partition_of_unity_illustration.svg.png)

Assume we have finite covering U = {Ua | a ∈ A} 
of space X (A is indexing set), 
we can define nerve of the covering U 
to be simplical complex N(U):
- Vertices of N(U) are named by index set A. 
- Family {a(0), ..., a(k)} forms k-simplex
in N(U) if and only if Ua(0) ∩ Ua(1) ∩ ... ∩ Ua(k) is 
non-empty set.

With defined partition of unity, we can obtain 
map from X to N(U). 


## Mapper - Implementation

![iris](docs/images/reeb-graph.png)




## Toy Example - Iris

![iris](docs/images/iris.png)

## Literature

[\[1\] Intro to Applied Topological Data Analysis](https://towardsdatascience.com/intro-to-topological-data-analysis-and-application-to-nlp-training-data-for-financial-services-719495a111a4)

[\[2\] When is a coffee mug a donut? Topology explains it](https://phys.org/news/2016-10-coffee-donut-topology.html)

[\[3\] Introduction to Topology](https://www.math.colostate.edu/~renzo/teaching/Topology10/Notes.pdf)

[\[4\] Topological Methods for the Analysis of High Dimensional
Data Sets and 3D Object Recognition - Gurjeet Singh, Facundo Mémoli and Gunnar Carlsson](https://diglib.eg.org/bitstream/handle/10.2312/SPBG.SPBG07.091-100/091-100.pdf?sequence=1&isAllowed=y)

[\[5\] S. Mardsic and J. Segal, Shape theory, North-Holland Publishing Company, 1982.]()