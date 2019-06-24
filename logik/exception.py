class KriterienError(Exception):
    pass


class UngültigeEingabeError(KriterienError):
    '''Diese Exception wird geworfen wenn in der Eingabezeile keine passende Kriterien eingegeben werden'''

    def __init__(self, expression):
        self.expression = expression
        self.message = 'Ungültige Eingabe. Eventuell ist ein Kriterium falsch geschrieben'
