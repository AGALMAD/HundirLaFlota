# Clase barco, se debe pasar la longitud y un array de sus posiciones (x,y)
class Ship:
    def __init__(self, positions=None):
        if positions is None:
            positions = []
        self.positions = positions

    """ Método para disparar al barco
     TRUE si ha sido tocado
     FALSE si no ha sido tocado"""
    def shot(self, shot_position):
        if shot_position in self.positions:
            i = self.positions.index(shot_position)
            self.positions[i].touched = True
            return True

        return False

    """Método para saber si el barco ha sido hundido
     TRUE si todas las posiciones han sido tocadas
     FALSE si hay alguna posición no tocada"""
    def isSunken(self):
        for position in self.positions:
            if not position.touched:
                return False

        return True

