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

    def __iter__(self):
        return iter(self.to_lista())

    def to_lista(self):
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    to_list = to_lista

    def pop_front(self):
        if self.cabeza is None:
            return None
        valor = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        self._len -= 1
        if self.cabeza is None:
            self.cola = None
        return valor

    def push_front(self, dato):
        nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = self.cola = nodo
        else:
            nodo.siguiente = self.cabeza
            self.cabeza = nodo
        self._len += 1

    def pop_back(self):
        if self.cabeza is None:
            return None
        if self.cabeza is self.cola:
            valor = self.cabeza.dato
            self.cabeza = self.cola = None
            self._len = 0
            return valor
        actual = self.cabeza
        while actual.siguiente is not self.cola:
            actual = actual.siguiente
        valor = self.cola.dato
        actual.siguiente = None
        self.cola = actual
        self._len -= 1
        return valor

    def remove_dato(self, dato):
        if self.cabeza is None:
            return False
        if self.cabeza.dato == dato:
            self.pop_front()
            return True
        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.dato != dato:
            actual = actual.siguiente
        if actual.siguiente is None:
            return False
        if actual.siguiente is self.cola:
            self.cola = actual
        actual.siguiente = actual.siguiente.siguiente
        self._len -= 1
        return True

    def __repr__(self):
        return f"ListaEnlazada([{', '.join(repr(x) for x in self)}])"

    def _reconstruir_desde_lista(self, items):
        self.cabeza = self.cola = None
        self._len = 0
        for it in items:
            self.append(it)
