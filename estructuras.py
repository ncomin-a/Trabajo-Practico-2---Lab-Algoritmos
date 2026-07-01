class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._len = 0

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self._len

    def append(self, dato):
        nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = self.cola = nodo
        else:
            self.cola.siguiente = nodo
            self.cola = nodo
        self._len += 1

    push_back = append

    def __repr__(self):
        return f"ListaEnlazada([{', '.join(repr(x) for x in self)}])"

    def _reconstruir_desde_lista(self, items):
        self.cabeza = self.cola = None
        self._len = 0
        for it in items:
            self.append(it)
