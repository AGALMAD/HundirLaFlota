class Board:
    def __init__(self):
        self.ships = []
        self.not_touched_ships = []

    """Método para disparar a los barcos
    1 si lo toca
    2 si lo toca y lo hunde
    0 si no lo toca
    """
    def shot(self,shot_position):
        for ship in self.ships:
            if ship.shot(shot_position):
                if not ship.isSunken():
                    return 1
                else:
                    return 2


        self.not_touched_ships.append(shot_position)
        return 0

    #Método para saber si el jugador se ha quedado sin barcos
    def lose(self):
        for ship in self.ships:
            if not ship.isSunken():
                return False

        return True
