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

    def push_front(self, dato):
        nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = self.cola = nodo
        else:
            nodo.siguiente = self.cabeza
            self.cabeza = nodo
        self._len += 1

    def pop_front(self):
        if self.cabeza is None:
            return None
        nodo = self.cabeza
        self.cabeza = nodo.siguiente
        if self.cabeza is None:
            self.cola = None
        self._len -= 1
        return nodo.dato

    def pop_back(self):
        if self.cabeza is None:
            return None
        if self.cabeza is self.cola:
            dato = self.cabeza.dato
            self.cabeza = self.cola = None
            self._len -= 1
            return dato
        actual = self.cabeza
        while actual.siguiente is not self.cola:
            actual = actual.siguiente
        dato = self.cola.dato
        actual.siguiente = None
        self.cola = actual
        self._len -= 1
        return dato

    def remove_dato(self, dato):
        anterior = None
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                if actual is self.cola:
                    self.cola = anterior
                self._len -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self):
        return f"ListaEnlazada([{', '.join(repr(x) for x in self)}])"

    def _reconstruir_desde_lista(self, items):
        self.cabeza = self.cola = None
        self._len = 0
        for it in items:
            self.append(it)

    def ordenar_por_poder(self):
        items = list(self)
        items.sort(key=lambda p: p.poder_combate, reverse=True)
        self._reconstruir_desde_lista(items)

    def ordenar_por_nombre(self):
        items = list(self)
        items.sort(key=lambda p: p.nombre.lower())
        self._reconstruir_desde_lista(items)

    def ordenar_por_nivel(self):
        items = list(self)
        items.sort(key=lambda p: p.nivel, reverse=True)
        self._reconstruir_desde_lista(items)


class Stack:
    def __init__(self):
        self.tope = None
        self._fondo = None
        self._len = 0

    def esta_vacia(self):
        return self.tope is None

    def __len__(self):
        return self._len

    def push(self, dato):
        nodo = Nodo(dato)
        nodo.siguiente = self.tope
        self.tope = nodo
        if self._fondo is None:
            self._fondo = nodo
        self._len += 1

    def pop(self):
        if self.tope is None:
            return None
        nodo = self.tope
        self.tope = nodo.siguiente
        if self.tope is None:
            self._fondo = None
        self._len -= 1
        return nodo.dato

    def peek(self):
        return self.tope.dato if self.tope is not None else None

    def quitar_fondo(self):
        if self.tope is None:
            return None
        if self.tope is self._fondo:
            return self.pop()
        actual = self.tope
        while actual.siguiente is not self._fondo:
            actual = actual.siguiente
        dato = self._fondo.dato
        actual.siguiente = None
        self._fondo = actual
        self._len -= 1
        return dato

    def __iter__(self):
        actual = self.tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self):
        return f"Stack([{', '.join(repr(x) for x in self)}])"