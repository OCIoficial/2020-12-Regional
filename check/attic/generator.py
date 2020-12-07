import random
import sys
from enum import Enum

INTENTOS = 8

class Tipo(Enum):
    TORRE   = 0    
    ALFIL   = 1
    REINA   = 2
    REY     = 3
    CABALLO = 4
    PEON    = 5
    VACIA   = 6

class Color(Enum):
    BLANCA = 0
    NEGRA  = 1

def encontrarReyBlanco(tablero):
    for i in range(8):
        for j in range(8):
            if tablero[i][j].tipo is Tipo.REY and tablero[i][j].color is Color.BLANCA:
                return (i, j)

class Pieza:
    def __init__(self, tipo, color):
        self.tipo = tipo
        self.color = color

class Torre(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.TORRE, color)

    """
    Posicionar una torre negra atacando al rey blanco.
    La funcion intenta 8 veces poner a la torre en una posición de ataque. Esto
    no verifica si es que hay otras piezas entre medio. Lo intenta INTENTOS
    numero de veces en una posicion aleatoria atacando al rey, no hace nada si
    la posición siempre está ocupada.
    """
    def posicionarAtaque(tablero):
        reyY, reyX = encontrarReyBlanco(tablero)
        intentos = INTENTOS
        for _ in range(INTENTOS):
            if random.choice([True, False]):
                # La torre ataca al rey verticalmente
                y = random.randint(0, 7)
                if tablero[y][reyX].tipo is not Tipo.VACIA:
                    continue
                tablero[y][reyX] = Pieza(Tipo.TORRE, Color.NEGRA)
                return
            else:
                # La torre ataca al rey horizontalmente
                x = random.randint(0, 7)
                if tablero[reyY][x].tipo is Tipo.VACIA:
                    tablero[reyY][x] = Torre(Color.NEGRA)
                    return

class Alfil(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.ALFIL, color)

    """
    Posicionar un alfil negro atacando al rey blanco.
    La funcion intenta 8 veces poner al alfil en una posición de ataque. Esto
    no verifica si es que hay otras piezas entre medio. Lo intenta INTENTOS
    numero de veces en una posicion aleatoria atacando al rey, no hace nada si
    la posición siempre está ocupada.
    """
    def posicionarAtaque(tablero):
        reyY, reyX = encontrarReyBlanco(tablero)
        for _ in range(INTENTOS * 4):
            # No estoy muy seguro que tan probable es que pase esto, pero
            # podemos subirle el numero de intentos hasta que funcione.
            n = random.randint(0, 7)
            x = reyX + random.choice([n, -n])
            y = reyY + random.choice([n, -n])
            if x < 0 or 7 < x or y < 0 or 7 < y:
                continue;
            if tablero[y][x].tipo is Tipo.VACIA:
                tablero[y][x] = Alfil(Color.NEGRA)
                return


class Reina(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.REINA, color)

    """
    Posicionar una reina negra atacando al rey blanco.
    Primero decide si atacar en linea recta (vertical u horizontalmente) o en
    diagonal, y despues posiciona a la reina usando la misma estrategia que la
    torra y el alfil respectivamente.
    """
    def posicionarAtaque(tablero):
        reyY, reyX = encontrarReyBlanco(tablero)
        if random.choice([True, False]):
            # La Reina ataca en linea recta (copy-paste de la torre)
            for _ in range(INTENTOS):
                if random.choice([True, False]):
                    # La Reina ataca al rey verticalmente
                    y = random.randint(0, 7)
                    if tablero[y][reyX].tipo is not VACIA:
                        continue
                    tablero[y][reyX] = Pieza(Tipo.REINA, Color.NEGRA)
                    return
                else:
                    # La Reina ataca al rey horizontalmente
                    x = random.randint(0, 7)
                    if tablero[reyY][x].tipo is VACIA:
                        tablero[reyY][x] = Pieza(Tipo.REINA, Color.NEGRA)
                        return
        else:
            # La Reina ataca en diagonal (copy-paste del alfil)
            for _ in range(INTENTOS * 4):
                n = random.randint(0, 7)
                x = reyX + random.choice([n, -n])
                y = reyY + random.choice([n, -n])
                if x < 0 or 7 < x or y < 0 or 7 < y:
                    continue;
                if tablero[y][x].tipo is VACIA:
                    tablero[y][x] = Reina(Color.NEGRA)
                    return

class Caballo(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.CABALLO, color)

    def posicionarAtaque(tablero):
        reyY, reyX = encontrarReyBlanco(tablero)
        for _ in range(INTENTOS):
            # Separa las opciones en 2 grupos para hacerlo mas facil
            if random.choice([True, False]):
                x = reyX + random.choice([-1, 1])
                y = reyY + random.choice([-2, 2])
            else:
                x = reyX + random.choice([-2, 2])
                y = reyY + random.choice([-1, 1])
            if x < 0 or 7 < x or y < 0 or 7 < y:
                continue;
            if tablero[y][x].tipo is VACIA:
                tablero[y][x] = Caballo(Color.NEGRA)
                return

class Peon(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.PEON, color)

    def posicionarAtaque(tablero):
        reyY, reyX = encontrarReyBlanco(tablero)
        x = random.choice([-1, 1])
        if reyX + x < 0 or 7 < reyX + x:
            return
        if tablero[reyY][reyX + x].tipo is not Tipo.VACIA:
            x *= - 1
        if reyX + x < 0 or 7 < reyX + x:
            return
        if tablero[reyY][reyX + x].tipo is not Tipo.VACIA:
            # Los dos espacios de ataque estan bloqueados
            return 
        tablero[reyY][reyX + x] = Peon(Color.NEGRA)

class Rey(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.REY, color)

    def ponerRandom(tablero):
        # Asume que el tablero esta vacio
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        tablero[y][x] = Rey(Color.BLANCA)

def printInput(tablero):
    for i in range(8):
        for j in range(8):
            elem = tablero[i][j]
            if elem.tipo is not Tipo.VACIA:
                print("{} {} {} {}".format(elem.color.value, elem.tipo.value,
                    i, j))
random.seed(str(sys.argv))

caso = int(sys.argv[2])
nPiezas = int(sys.argv[3])

board = [[Pieza(Tipo.VACIA, Color.NEGRA) for _ in range(8)] for _ in range(8)]
Rey.ponerRandom(board)

opciones = [Torre, Alfil, Reina, Caballo, Peon]
if caso == 1:
    for _ in range(nPiezas):
       random.choice(opciones).posicionarAtaque(board)

print(nPiezas + 1)
printInput(board)
