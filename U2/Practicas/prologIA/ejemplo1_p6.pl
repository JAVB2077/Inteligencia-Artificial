% Hombres y mujeres
hombre(carlos).
hombre(martin).
hombre(peter).
mujer(carmen).
mujer(lenka).

%Relaciones directas
progenitor(carlos, martin).
progenitor(carmen, martin).
progenitor(martin, peter).
progenitor(lenka, peter).

%Regla 1 - X es padre de Y si X es progenitor de Y y X es hombre
padre(X,Y) :- progenitor(X,Y), hombre(X).

%Regla 2 - X es madre de Y si X es progenitor de Y y X es mujer
madre(X,Y) :- progenitor(X,Y), mujer(X).

%Regla 3 - X es abuelo de Y si X es padre de Z e Z es padre de Y
abuelo(X,Y) :- padre(X,Z), padre(Z,Y).

%consultas
%?- padre(X, peter).
%?- madre(X, peter).
%?- abuelo(X, peter).