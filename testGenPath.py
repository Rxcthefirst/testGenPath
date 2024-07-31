from rdflib import Graph, URIRef

# Function to explore paths recursively
def find_paths(graph, start, end, path=None, visited=None, depth=0):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    path = path + [start]
    visited.add(start)

    if start == end:
        return [path]

    paths = []
    for _, p, o in graph.triples((start, None, None)):
        if (p == URIRef("http://example.org/friendOf") or p == URIRef("http://example.org/parentOf")) and o not in visited and len(path) < 5:
            print("visited", visited, _, p, o, depth, path)
            new_paths = find_paths(graph, o, end, path, visited, depth)
            for new_path in new_paths:
                paths.append(new_path)
                visited = set(path)

                # print("start", path)

    # Allow nodes to be revisited in different paths


    return paths

# Create RDF graph and load data (use rdflib Graph for local or remote access)
graph = Graph().parse(data='''
@prefix : <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Alice :friendOf :Bob .
:Bob :friendOf :Charlie .
:Charlie :friendOf :Bob .
:Charlie :friendOf :Dave .
:Alice :parentOf :Eve .
:Charlie :friendOf :John .
:John :parentOf :Dave .
:Alice :friendOf :Dave .
:Eve :friendOf :Charlie .

:Alice rdfs:label "Alice" .
:Bob rdfs:label "Bob" .
:Charlie rdfs:label "Charlie" .
:Dave rdfs:label "Dave" .
:Eve rdfs:label "Eve" .
''', format='n3')

# Define start and end nodes
start_node = URIRef("http://example.org/Alice")
end_node = URIRef("http://example.org/Dave")

# Find and print all paths
all_paths = find_paths(graph, start_node, end_node)
for path in all_paths:
    print(" -> ".join([str(node) for node in path]))



