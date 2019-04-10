# Graph isomorphism equvialence classes and automorphism count

Given a list of graphs determines the isomorphism equvialence classes and the corresponding number of automorphisms.

## Usage

`-i | --iso`: Determine equvialence classes

`-a | --aut`: Calculate number of automorphisms

`-af | --autfirst`: If both `--iso` and `--aut` or none is set, calculate the automorphisms first and then compare only the ones with equal number

`-v | --verbose`: Enables logging

`[-g | --graph] 0 1 4`: Provide the indices of the graphs to be checked

## Examples

`./main.py graphs/bigtrees3.grl --iso --aut -g 0 1 3`

`./main.py graphs/cubes5.grl --autfirst`

`./main.py graphs/Isom1.grl graphs/cographs1.grl --iso -v`
