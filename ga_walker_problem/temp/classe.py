class retangulo(object):
    def __init__(self,largura,altura):
        self.largura = largura
        self.altura = altura
    def area(self):
        return self.largura * self.altura
    def tipo(self):
        return "Sou retangulo"

class quadrado(retangulo):
    def __init__(self,lado):
        super(quadrado,self).__init__(lado,lado)
    def tipo(self):
        return "Sou quadrado"

