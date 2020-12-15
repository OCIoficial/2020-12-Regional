import random
import sys
from enum import Enum
from functools import reduce

# TODO: Revisar que las piezas de relleno no puedan usarse para salir de jaque
# comiendose a la pieza atacante.

INTENTOS = 22

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

    def otro(self):
        return Color(0) if self.value == 1 else Color(1)

def encontrarReyBlanco(tablero):
    for i in range(8):
        for j in range(8):
            if tablero[i][j].tipo is Tipo.REY and tablero[i][j].color is Color.BLANCA:
                return (i, j)
    return None

def encontrarReyNegro(tablero):
    for i in range(8):
        for j in range(8):
            if tablero[i][j].tipo is Tipo.REY and tablero[i][j].color is \
            Color.NEGRA:
                return (i, j)
    return None

def todasVacias(tablero):
    opciones = []
    for i in range(8):
        for j in range(8):
            if tablero[i][j] is Tipo.VACIA:
                opciones.append((i, j))
    return opciones

"""
Revisa si la casilla está siendo atacada. returns True si hay un ataque en la
casilla
"""
def casillaAtacada(tablero, target, color=Color.NEGRA):
    piezas = [Torre, Alfil, Reina, Caballo, Peon, Rey]
    ataques = [pieza.casillaAtacada(tablero, target, pieza) for pieza in piezas]
    return reduce((lambda x, y: x or y), ataques)    

"""
Revisa si la pieza de tipo `pieza` y color `color` en la posicion `source`
amenaza a la pieza en posicion `target` o las casillas de al rededor
"""
def amenazaAlRey(pieza, tablero, source, target, color=Color.NEGRA):
    if target is None:
        return False
    ataca = False
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            newTarget = (target[0] + i, target[1] + j)
            ataca |= pieza.revisarAtaque(tablero, source, newTarget, color)
    return ataca

"""
    Elimina las casillas aledañas a target de las opciones. Esto es para que el
    rey blanco no tenga la opción de comerse a la ficha que está atacando.
"""
def eliminarAledanas(opciones, target):
    (y, x) = target
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if (y + i, x + j) in opciones:
                opciones.remove((y + i, x + j))
    return opciones



class Pieza:
    def __init__(self, tipo, color):
        self.tipo = tipo
        self.color = color

class Torre(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.TORRE, color)

    """
    Encuentra vertical y horizontalmente las posibles opciones para posicionar
    una torre atacando a la casilla target
    """
    def posiblesAtaques(tablero, target, color=None):
        (targetY, targetX) = target
        opciones = []
        # Hacia arriba
        for i in range(targetY - 1, -1, -1):
            if tablero[i][targetX].tipo is not Tipo.VACIA:
                break
            opciones.append((i, targetX))
        # Hacia abajo
        for i in range(targetY + 1, 8):
            if tablero[i][targetX].tipo is not Tipo.VACIA:
                break
            opciones.append((i, targetX))
        # Hacia la izquierda
        for i in range(targetX - 1, -1, -1):
            if tablero[targetY][i].tipo is not Tipo.VACIA:
                break
            opciones.append((targetY, i))
        # Hacia la derecha
        for i in range(targetX + 1, 8):
            if tablero[targetY][i].tipo is not Tipo.VACIA:
                break
            opciones.append((targetY, i))
        return opciones

    """
    Posicionar una torre negra atacando a la casilla target.
    """
    def posicionarAtaque(tablero, target, color=None):
        opciones = Torre.posiblesAtaques(tablero, target)
        opciones = eliminarAledanas(opciones, target)
        if not opciones:
            return False
        posicion = random.choice(opciones)
        tablero[posicion[0]][posicion[1]] = Torre(Color.NEGRA)
        return True

    """
    Returns True si `source` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color=None):
        (y, x) = target
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Torre.posiblesAtaques(tablero, target)
        return source in opciones

    """
    Posicionar una torre de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    """
    def posicionarExtra(tablero, color):
        if color is Color.BLANCA:
            rey = encontrarReyNegro(tablero)
        else:
            rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Torre, tablero, (y, x), rey):
                tablero[y][x] = Torre(color)
                break

    """
    Returns True si hay una torre atacando la casilla indicada.
    Tipo tiene que ser o Torre o Reina
    """
    def casillaAtacada(tablero, target, tipo=Tipo.TORRE, color=None):
        (y, x) = target
        # Hacia arriba
        for i in range(y - 1, -1, -1):
            if tablero[i][x].tipo is Tipo.VACIA:
                continue
            elif tablero[i][x].tipo is tipo:
                return True
            else:
                break
        # Hacia abajo
        for i in range(y + 1, 8):
            if tablero[i][x].tipo is Tipo.VACIA:
                continue
            elif tablero[i][x].tipo is tipo:
                return True
            else:
                break
        # Hacia la izquierda
        for i in range(x - 1, -1, -1):
            if tablero[i][x].tipo is Tipo.VACIA:
                continue
            elif tablero[i][x].tipo is tipo:
                return True
            else:
                break
        # Hacia la derecha
        for i in range(x + 1, 8):
            if tablero[i][x].tipo is Tipo.VACIA:
                continue
            elif tablero[i][x].tipo is tipo:
                return True
            else:
                break
        return False



class Alfil(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.ALFIL, color)

    """
    Encuentra los posibles ataques en las diagonales para la casilla target
    """
    def posiblesAtaques(tablero, target, color=None):
        (targetY, targetX) = target
        opciones = []
        valid = [True, True, True, True]
        for i in range(8):
            # Diagonal 1 -- arriba a la derecha
            if valid[0]:
                if 0 > targetY - i or 8 <= targetX + i:
                    valid[0] = False
                elif tablero[targetY - i][targetX + i].tipo is not Tipo.VACIA:
                    valid[0] = False
                else:
                    opciones.append((targetY - i, targetX + i))
            # Diagonal 2 -- arriba a la izquierda
            if valid[1]:
                if 0 > targetY - i or 0 > targetX - i:
                    valid[1] = False
                elif tablero[targetY - i][targetX - i].tipo is not Tipo.VACIA:
                    valid[1] = False
                else:
                    opciones.append((targetY - i, targetX - i))
            # Diagonal 3 -- abajo a la izquierda
            if valid[2]:
                if 8 <= targetY + i or 0 > targetX - i:
                    valid[2] = False
                elif tablero[targetY + i][targetX - i].tipo is not Tipo.VACIA:
                    valid[2] = False
                else:
                    opciones.append((targetY + i, targetX - i))
            # Diagonal 4 -- abajo a la derecha
            if valid[3]:
                if 8 <= targetY + i or 8 <= targetX + i:
                    valid[3] = False
                elif tablero[targetY + i][targetX + i].tipo is not Tipo.VACIA:
                    valid[3] = False
                else:
                    opciones.append((targetY + i, targetX + i))
        return opciones

    """
    Posicionar un alfil negro atacando a la posicion target
    """
    def posicionarAtaque(tablero, target, color=None):
        opciones = Alfil.posiblesAtaques(tablero, target)
        opciones = eliminarAledanas(opciones, target)
        if not opciones:
            return False
        (y, x) = random.choice(opciones)
        tablero[y][x] = Alfil(Color.NEGRA)
        return True

    """
    Returns True si `source` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color=None):
        (y, x) = target
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Alfil.posiblesAtaques(tablero, target)
        return source in opciones

    """
    Posicionar un alfil de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    """
    def posicionarExtra(tablero, color):
        if color is Color.BLANCA:
            rey = encontrarReyNegro(tablero)
        else:
            rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Alfil, tablero, (y, x), rey):
                tablero[y][x] = Alfil(color)
                break

    """
    Returns True si hay un alfil atacando la casilla indicada.
    Tipo tiene que ser o Alfil o Reina
    """
    def casillaAtacada(tablero, target, tipo=Tipo.ALFIL, color=None):
        (y, x) = target
        valid = [True, True, True, True]
        for i in range(8):
            # Diagonal 1 -- arriba a la derecha
            if valid[0]:
                if 0 > y - i or 8 <= x + i:
                    valid[0] = False
                elif tablero[y - i][x + i].tipo is Tipo.VACIA:
                    None # Do nothing
                elif tablero[y - i][x + i].tipo is tipo:
                    return True
                else:
                    valid[0] = False
            # Diagonal 2 -- arriba a la izquierda
            if valid[1]:
                if 0 > y - i or 0 > x - i:
                    valid[1] = False
                elif tablero[y - i][x - i].tipo is Tipo.VACIA:
                    None # Do nothing
                elif tablero[y - i][x - i].tipo is tipo:
                    return True
                else:
                    valid[1] = False
            # Diagonal 3 -- abajo a la izquierda
            if valid[2]:
                if 8 <= y + i or 0 > x - i:
                    valid[2] = False
                elif tablero[y + i][x - i].tipo is Tipo.VACIA:
                    None # Do nothing
                elif tablero[y + i][x - i].tipo is tipo:
                    return True
                else:
                    valid[2] = False
            # Diagonal 4 -- abajo a la derecha
            if valid[3]:
                if 8 <= y + i or 8 <= x + i:
                    valid[3] = False
                elif tablero[y + i][x + i].tipo is Tipo.VACIA:
                    None # Do nothing
                elif tablero[y + i][x + i].tipo is tipo:
                    return True
                else:
                    valid[3] = False
        return False

class Reina(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.REINA, color)

    def posiblesAtaques(tablero, target, color=None):
        return Torre.posiblesAtaques(tablero, target) + \
            Alfil.posiblesAtaques(tablero, target)

    """
    Posicionar una reina negra atacando a la posicion target
    Combina las opciones de la torre y el alfil y elige una posicion al azar
    dentro de esas opciones.
    """
    def posicionarAtaque(tablero, target, color=None):
        opciones = Reina.posiblesAtaques(tablero, target)
        opciones = eliminarAledanas(opciones, target)
        if not opciones:
            return False
        (y, x) = random.choice(opciones)
        tablero[y][x] = Reina(Color.NEGRA)
        return True

    """
    Returns True si `source` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color=None):
        (y, x) = target
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Reina.posiblesAtaques(tablero, target)
        return source in opciones

    """
    Posicionar una reina de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    """
    def posicionarExtra(tablero, color):
        if color is Color.BLANCA:
            rey = encontrarReyNegro(tablero)
        else:
            rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Reina, tablero, (y, x), rey):
                tablero[y][x] = Reina(color)
                break

    """
    Returns True si hay un alfil atacando la casilla indicada.
    """
    def casillaAtacada(tablero, target, tipo=Tipo.REINA, color=None):
        (y, x) = target
        return Torre.casillaAtacada(tablero, (y, x), tipo) or \
                Alfil.casillaAtacada(tablero, (y, x), tipo)

class Caballo(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.CABALLO, color)

    """
    Encuentra los posibles ataques para la casilla target
    """
    def posiblesAtaques(tablero, target, color=None):
        opciones = []
        (y, x) = target

        # revisar las 8 opciones manualmente :(
        if 0 <= y - 2:
            if 0 <= x - 1:
                if tablero[y - 2][x - 1].tipo is Tipo.VACIA:
                    opciones.append((y - 2, x - 1))
            if 8 > x + 1:
                if tablero[y - 2][x + 1].tipo is Tipo.VACIA:
                    opciones.append((y - 2, x + 1))

        if 8 > y + 2:
            if 0 <= x - 1:
                if tablero[y + 2][x - 1].tipo is Tipo.VACIA:
                    opciones.append((y + 2, x - 1))
            if 8 > x + 1:
                if tablero[y + 2][x + 1].tipo is Tipo.VACIA:
                    opciones.append((y + 2, x + 1))

        if 0 <= x - 2:
            if 0 <= y - 1:
                if tablero[y - 1][x - 2].tipo is Tipo.VACIA:
                    opciones.append((y - 1, x - 2))
            if 8 > y + 1:
                if tablero[y + 1][x - 2].tipo is Tipo.VACIA:
                    opciones.append((y + 1, x - 2))

        if 8 > x + 2:
            if 0 <= y - 1:
                if tablero[y - 1][x + 2].tipo is Tipo.VACIA:
                    opciones.append((y - 1, x + 2))
            if 8 > y + 1:
                if tablero[y + 1][x + 2].tipo is Tipo.VACIA:
                    opciones.append((y + 1, x + 2))

        return opciones


    def posicionarAtaque(tablero, target, color=None):
        opciones = Caballo.posiblesAtaques(tablero, target) 
        opciones = eliminarAledanas(opciones, target)
        if not opciones:
            return False
        (y, x) = random.choice(opciones)
        tablero[y][x] = Caballo(Color.NEGRA)
        return True

    """
    Returns True si `source` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color=None):
        (y, x) = target
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Caballo.posiblesAtaques(tablero, target)
        return source in opciones

    """
    Posicionar un caballo de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    """
    def posicionarExtra(tablero, color):
        if color is Color.BLANCA:
            rey = encontrarReyNegro(tablero)
        else:
            rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Caballo, tablero, (y, x), rey):
                tablero[y][x] = Caballo(color)
                break

    """
    Returns True si hay un Caballo atacando la casilla indicada.
    """
    def casillaAtacada(tablero, target, tipo=Tipo.CABALLO, color=None):
        (y, x) = target
        opciones = Caballo.posiblesAtaques(tablero, (y, x))
        for opcion in opciones:
            if tablero[opcion[0]][opcion[1]] is tipo:
                return True
        return False

class Peon(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.PEON, color)

    """
    Encuentra los posibles ataques para la casilla target.
    target es de color 'color', siendo atacada por una
    pieza de color `color.otro()`
    """
    def posiblesAtaques(tablero, target, color):
        opciones = []
        (y, x) = target
        if color is Color.BLANCA:
            if y - 1 >= 0:
                if x - 1 >= 0:
                    if tablero[y - 1][x - 1].tipo is Tipo.VACIA:
                        opciones.append((y - 1, x - 1))
                if x + 1 < 8:
                    if tablero[y - 1][x + 1].tipo is Tipo.VACIA:
                        opciones.append((y - 1, x + 1))
        else:
            if y + 1 < 8:
                if x - 1 >= 0:
                    if tablero[y + 1][x - 1].tipo is Tipo.VACIA:
                        opciones.append((y + 1, x - 1))
                if x + 1 < 8:
                    if tablero[y + 1][x + 1].tipo is Tipo.VACIA:
                        opciones.append((y + 1, x + 1))
        return opciones

    def posicionarAtaque(tablero, target, color):
        opciones = Peon.posiblesAtaques(tablero, target, color.otro()) 
        if not opciones:
            return False
        (y, x) = random.choice(opciones)
        tablero[y][x] = Peon(Color.NEGRA)
        return True

    """
    Returns True si `source` de color `color` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color):
        (y, x) = source
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Peon.posiblesAtaques(tablero, target, color.otro())
        return source in opciones

    """
    Posicionar un peon de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    """
    def posicionarExtra(tablero, color):
        if color is Color.BLANCA:
            rey = encontrarReyNegro(tablero)
        else:
            rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Peon, tablero, (y, x), rey, color):
                tablero[y][x] = Peon(color)
                break

    """
    Returns True si hay un Peon atacando la casilla indicada.
    """
    def casillaAtacada(tablero, target, tipo=Tipo.PEON, color=Color.NEGRA):
        (y, x) = target
        opciones = Peon.posiblesAtaques(tablero, (y, x), color)
        for opcion in opciones:
            if tablero[opcion[0]][opcion[1]].tipo is tipo:
                return True
        return False

class Rey(Pieza):
    def __init__(self, color):
        Pieza.__init__(self, Tipo.REY, color)

    def ponerRandom(tablero, color):
        for i in range(INTENTOS):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA:
                tablero[y][x] = Rey(color)
                break

    """
    Encuentra los posibles ataques para la casilla target
    """
    def posiblesAtaques(tablero, target, color=None):
        opciones = []
        (y, x) = target
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if y + i < 0 or 8 <= y + i or x + j < 0 or x + j >= 8:
                    continue
                # if tablero[y + i][x + j] is Tipo.VACIA:
                opciones.append((y + i, x + j))
        return opciones

    """
    Returns True si `source` puede atacar a `target`
    """
    def revisarAtaque(tablero, source, target, color=None):
        (y, x) = target
        if x < 0 or 8 <= x or y < 0 or 8 <= y:
            return False
        opciones = Rey.posiblesAtaques(tablero, target)
        return source in opciones

    """
    Posicionar un rey de color 'color' que no ataca al rey ni los espacios al
    rededor del rey oponente.
    SOLO DEBE SER USADA CON COLOR NEGRO
    """
    def posicionarExtra(tablero, color):
        assert(color is Color.NEGRA)
        rey = encontrarReyBlanco(tablero)

        for i in range(INTENTOS * 2):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if tablero[y][x].tipo is Tipo.VACIA and \
                    not amenazaAlRey(Rey, tablero, (y, x), rey):
                tablero[y][x] = Rey(color)
                break

    """
    Returns True si hay un Rey atacando la casilla indicada.
    """
    def casillaAtacada(tablero, target, tipo=Tipo.REY, color=None):
        (y, x) = target
        opciones = Rey.posiblesAtaques(tablero, (y, x))
        for opcion in opciones:
            if tablero[opcion[0]][opcion[1]].tipo is tipo:
                return True
        return False

def printInput(tablero):
    for i in range(8):
        for j in range(8):
            elem = tablero[i][j]
            if elem.tipo is not Tipo.VACIA:
                print("{} {} {} {}".format(elem.color.value, elem.tipo.value,
                    i, j))

def contarPiezas(tablero):
    c = 0
    for i in range(8):
        for j in range(8):
            elem = tablero[i][j]
            if elem.tipo is not Tipo.VACIA:
                c += 1
    return c



"""
    Inputs
    En este orden: caso de prueba
                   numero de piezas negras atacando al rey blanco
                   numero de piezas blancas extra
                   numero de piezas negras extra
                   jaque mate? 1 = si, 0 = no. Esto hace el mejor intento a que
                               sea jaque mate, pero no lo garantiza
"""


random.seed(str(sys.argv[1:]))

caso = int(sys.argv[2])
nPiezasAtk = int(sys.argv[3])
nPiezasExtraBlanca = int(sys.argv[4])
nPiezasExtraNegra = int(sys.argv[5])
mate = int(sys.argv[6])

"""
    Comunes a todos los casos
"""

tablero = [[Pieza(Tipo.VACIA, Color.NEGRA) for _ in range(8)] for _ in range(8)]
Rey.ponerRandom(tablero, Color.BLANCA)
reyBlanco = encontrarReyBlanco(tablero)

Rey.posicionarExtra(tablero, Color.NEGRA)
reyNegro = encontrarReyNegro(tablero)

opcionesBlanco = [Torre] * 2 +  [Alfil] * 2 + [Reina] + [Caballo] * 2 + \
        [Peon] * 8
opcionesNegro = [Torre] * 2 +  [Alfil] * 2 + [Reina] + [Caballo] * 2 + \
        [Peon] * 8
# El peon tiene mas probabilidad
opcionesFlat = [Torre, Alfil, Reina, Caballo] + [Peon] * 5

"""
    Casos de prueba: 1. Al menos dos piezas atacan al rey blanco.
                     2. Negro solo tiene rey, peones y caballos
                     3. Todo vale.
"""

if caso == 1:
    opcionesNegro = [Peon] * 8 + [Caballo] * 2
    opcionesFlatNegro = [Peon] * 4 + [Caballo] # Los peones son mas probables
    for _ in range(nPiezasExtraBlanca):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesBlanco:
                opcionesBlanco.remove(pieza)
                pieza.posicionarExtra(tablero, Color.BLANCA)
                break
    for _ in range(nPiezasExtraNegra):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlatNegro)
            if pieza in opcionesNegro:
                opcionesNegro.remove(pieza)
                pieza.posicionarExtra(tablero, Color.NEGRA)
                break
    # Ponemos las piezas importantes que atacan al rey al final para que las
    # otras no bloqueen la linea de ataque. 
    for _ in range(nPiezasAtk):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlatNegro)
            if pieza in opcionesNegro:
                if pieza.posicionarAtaque(tablero, reyBlanco, Color.NEGRA):
                    opcionesNegro.remove(pieza)
                    break

    # Cubrir toda el area al rededor del rey
    if mate == 1:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                (y, x) = reyBlanco
                target = (y + i, x + j)
                if target[0] < 0 or target[0] >= 8 or \
                        target[1] < 0 or target[1] >= 8:
                    continue
                if not casillaAtacada(tablero, target, Color.NEGRA):
                    # No esta siendo atacada, poner una pieza atacando
                    for _ in range(INTENTOS * 4):
                        pieza = random.choice(opcionesFlatNegro)
                        if pieza in opcionesNegro:
                            if pieza.posicionarAtaque(tablero, target, Color.NEGRA):
                                opcionesNegro.remove(pieza)
                                break

if caso == 2:
    # En este caso los ataques de peones o caballos no pueden ser bloqueados
    # por otras piezas
    assert(nPiezasAtk >= 2)
    for _ in range(nPiezasAtk):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesNegro:
                if pieza.posicionarAtaque(tablero, reyBlanco, Color.NEGRA):
                    opcionesNegro.remove(pieza)
                    break
    for _ in range(nPiezasExtraBlanca):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesBlanco:
                opcionesBlanco.remove(pieza)
                pieza.posicionarExtra(tablero, Color.BLANCA)
                break
    for _ in range(nPiezasExtraNegra):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesNegro:
                opcionesNegro.remove(pieza)
                pieza.posicionarExtra(tablero, Color.NEGRA)
                break

    # Cubrir toda el area al rededor del rey
    if mate == 1:
        for whites in [True, False]:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    (y, x) = reyBlanco
                    target = (y + i, x + j)
                    if target[0] < 0 or target[0] >= 8 or \
                            target[1] < 0 or target[1] >= 8:
                        continue
                    if not casillaAtacada(tablero, target, Color.NEGRA):
                        # No esta siendo atacada, poner una pieza atacando
                        if whites:
                            if tablero[target[0]][target[1]].tipo is Tipo.VACIA:
                                if random.choice([True, False, False]):
                                    # 50/50 de bloquear con una pieza blanca
                                    pieza = random.choice(opcionesBlanco)
                                    tablero[target[0]][target[1]] = pieza(Color.BLANCA)
                                    opcionesBlanco.remove(pieza)
                                    break
                        else:
                            if tablero[target[0]][target[1]].color is not Color.BLANCA:
                                # Si no esta bloqueada por una pieza blanca
                                for _ in range(INTENTOS * 4):
                                    # Poner una pieza negra atacando
                                    pieza = random.choice(opcionesNegro)
                                    if pieza.posicionarAtaque(tablero, target, Color.NEGRA):
                                        opcionesNegro.remove(pieza)
                                        break

if caso == 3:
    # En este caso los ataques de peones o caballos no pueden ser bloqueados
    # por otras piezas
    for _ in range(nPiezasAtk):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesNegro:
                if pieza.posicionarAtaque(tablero, reyBlanco, Color.NEGRA):
                    opcionesNegro.remove(pieza)
                    break
    for _ in range(nPiezasExtraBlanca):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesBlanco:
                opcionesBlanco.remove(pieza)
                pieza.posicionarExtra(tablero, Color.BLANCA)
                break
    for _ in range(nPiezasExtraNegra):
        for _ in range(INTENTOS):
            pieza = random.choice(opcionesFlat)
            if pieza in opcionesNegro:
                opcionesNegro.remove(pieza)
                pieza.posicionarExtra(tablero, Color.NEGRA)
                break

    # Cubrir toda el area al rededor del rey
    if mate == 1:
        for whites in [True, False]:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    (y, x) = reyBlanco
                    target = (y + i, x + j)
                    if target[0] < 0 or target[0] >= 8 or \
                            target[1] < 0 or target[1] >= 8:
                        continue
                    if not casillaAtacada(tablero, target, Color.NEGRA):
                        # No esta siendo atacada, poner una pieza atacando
                        if whites:
                            if tablero[target[0]][target[1]].tipo is Tipo.VACIA:
                                if random.choice([True, False, False]):
                                    # 50/50 de bloquear con una pieza blanca
                                    pieza = random.choice(opcionesBlanco)
                                    tablero[target[0]][target[1]] = pieza(Color.BLANCA)
                                    opcionesBlanco.remove(pieza)
                                    break
                        else:
                            if tablero[target[0]][target[1]].color is not Color.BLANCA:
                                # Si no esta bloqueada por una pieza blanca
                                for _ in range(INTENTOS * 4):
                                    # Poner una pieza negra atacando
                                    pieza = random.choice(opcionesNegro)
                                    if pieza.posicionarAtaque(tablero, target, Color.NEGRA):
                                        opcionesNegro.remove(pieza)
                                        break


print(contarPiezas(tablero))
printInput(tablero)
