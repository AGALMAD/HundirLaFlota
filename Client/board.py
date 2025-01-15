matriz = [["" for _ in range(10)] for _ in range(10)]


def print_board():
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(" %s |" % matriz[i][j], end="")
        print()

def shot(x,y, good_shot):
    if matriz[x][y] == "" and good_shot:
        matriz[x][y] = "B"
    else:
        matriz[x][y] = "A"
            