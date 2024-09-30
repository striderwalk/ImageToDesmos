from PyDesmos import Graph


def plot_ploys(polys):
    with Graph("my graph") as G:
        for index, poly in enumerate(polys):
            print(len(poly))
            coeficientes, minx, maxx = poly

            x = G.x
            if len(coeficientes) == 2:
                G.define(f"f(x)", coeficientes[0] * x ** 2 + coeficientes[1])
            elif len(coeficientes) == 3:
                G.define(
                    f"f(x)",
                    coeficientes[0] * x ** 3
                    + coeficientes[1] * x ** 2
                    + coeficientes[2],
                )
            elif len(coeficientes) == 4:
                G.define(
                    f"f(x)",
                    coeficientes[0] * x ** 3
                    + coeficientes[1] * x ** 2
                    + coeficientes[2] * x ** 1
                    + coeficientes[3],
                )
            elif len(coeficientes) == 5:
                G.define(
                    f"f(x)",
                    coeficientes[0] * x ** 4
                    + coeficientes[1] * x ** 3
                    + coeficientes[2] * x ** 2
                    + coeficientes[3] * x ** 1
                    + coeficientes[4],
                )
            elif len(coeficientes) == 6:
                G.define(
                    f"f(x)",
                    coeficientes[0] * x ** 4
                    + coeficientes[1] * x ** 4
                    + coeficientes[2] * x ** 3
                    + coeficientes[3] * x ** 2
                    + coeficientes[4] * x ** 1
                    + coeficientes[5],
                )
