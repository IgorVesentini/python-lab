import os

print("=== Variabili speciali a livello modulo/script ===")
print(f"__file__     : {__file__}")
print(f"__name__     : {__name__}")
print(f"__doc__      : {__doc__}")
print(f"__package__  : {__package__}")
print(f"__loader__   : {__loader__}")
print(f"__spec__     : {__spec__}")
print(f"__cached__   : {__cached__}")
print(f"__builtins__ : {__builtins__}")

print("\n=== Attributi speciali in classe e oggetto ===")

class Esempio:
    """Classe di esempio per dimostrare attributi speciali"""

    def __init__(self, valore):
        self.valore = valore

    def __str__(self):
        return f"Esempio con valore={self.valore}"

    def __repr__(self):
        return f"Esempio(valore={self.valore!r})"

    def __call__(self):
        print("Chiamato come funzione")

    def __getitem__(self, key):
        return f"Accesso all'elemento {key}"

# Creo un'istanza
obj = Esempio(42)

print(f"obj.__class__     : {obj.__class__}")
print(f"obj.__dict__      : {obj.__dict__}")
print(f"str(obj)          : {str(obj)}")
print(f"repr(obj)         : {repr(obj)}")

print("Chiamo obj() (usa __call__):")
obj()

print(f"obj['chiave']     : {obj['chiave']}")

print(f"Nome della classe : {Esempio.__name__}")
print(f"Docstring classe : {Esempio.__doc__}")
