# MATF-NI-Mapper

## Topological data analysis (TDA)

`Topology` is the math concerning continuous objects. 
Not sizes and shapes, but continuity. It is how
things are connected and where the `gaps` are. 
It explains how a material's shape can be 
completely deformed into new one without losing its 
core properties. 

**Definition:** A `topology τ on a set X` consists of subsets of 
X satisfying the following properties:
- The empty set ∅ and the space X are both sets in the topology.
- The union of any collection of sets in τ is contained in τ
- The intersection of any finitely many sets in τ is also contained in τ.

**Definition:** A `topological space` is a pair (X, τ).

Famous example is the `mug and donut`
`homotopy`. Informally, two continous functions from
one topological space to another are called `homotopic`
if one can be `continuosly deformed` into another. Such
a deformation being called a `homotopy` between the 
two functions. [1, 2]

**Definition:** Let f, g : X → Y be maps. 
f is `homotopic` to g if there exists a map F : X×I → Y
such that F(x, 0) = f(x) and F(x, 1) = g(x) 
for all points x ∈ X. The map F is called a homotopy 
from f to g and we write it as f' F g.
More intuitvely, if we think of the second parameter 
of F as “time”, then F describes a
“continuous deformation” of f into g. At time 0 we 
have the function f, at time 1 we have the function g.

![iris](docs/images/mug-donut.gif)

`Topological data analysis (TDA)` is an approach to the analysis
of datasets using techiniques from `topology`. [1]

![iris](docs/images/iris.png)

## Literature

[\[1\] Intro to Applied Topological Data Analysis](https://towardsdatascience.com/intro-to-topological-data-analysis-and-application-to-nlp-training-data-for-financial-services-719495a111a4)

[\[2\] When is a coffee mug a donut? Topology explains it](https://phys.org/news/2016-10-coffee-donut-topology.html)

[\[3\] Introduction to Topology](https://www.math.colostate.edu/~renzo/teaching/Topology10/Notes.pdf)