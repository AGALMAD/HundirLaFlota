class Board:
    def __init__(self):
        self.ships = []

    #Método para disparar a los barcos
    def shot(self,shot_position):
        for ship in self.ships:
            if ship.shot(shot_position):
                return True
        return False

    #Método para saber si el jugador se ha quedado sin barcos
    def lose(self):
        for ship in self.ships:
            if not ship.isSunken():
                return False

        return True
