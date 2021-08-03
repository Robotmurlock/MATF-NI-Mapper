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

### Mapper

`TODO:` Topological background and motivation.

`Mapper` is TDA algorithm is used for generalized
notion of coordinatization for high dimensional
datasets. Coordinatization can refer to choice of
real valued coordinate functions or data or
other notions of geometric representation like
`reeb graph`. [4]

![iris](docs/images/reeb-graph.png)




## Toy Example - Iris

![iris](docs/images/iris.png)

## Literature

[\[1\] Intro to Applied Topological Data Analysis](https://towardsdatascience.com/intro-to-topological-data-analysis-and-application-to-nlp-training-data-for-financial-services-719495a111a4)

[\[2\] When is a coffee mug a donut? Topology explains it](https://phys.org/news/2016-10-coffee-donut-topology.html)

[\[3\] Introduction to Topology](https://www.math.colostate.edu/~renzo/teaching/Topology10/Notes.pdf)

[\[4\] Topological Methods for the Analysis of High Dimensional
Data Sets and 3D Object Recognition - Gurjeet Singh, Facundo Mémoli and Gunnar Carlsson](https://diglib.eg.org/bitstream/handle/10.2312/SPBG.SPBG07.091-100/091-100.pdf?sequence=1&isAllowed=y)