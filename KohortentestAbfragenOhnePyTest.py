import Kohortenabfrage as kab

# kann man nur 1 Element auswählen
AbfrageMitEinElement = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm"],
                                           verknüpfungen=[])
print("kohortengröße:", AbfrageMitEinElement.kohortengröße)
print("Nebendiagnose:", AbfrageMitEinElement.df_nebendia)
print("Zeitpunkt:", AbfrageMitEinElement.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitEinElement.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitEinElement.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitEinElement.y_achse_altersverteilung)
# kann man 2 Elemente auswählen : or
print("_______")
print("kann man 2 Elemente auswählen : or")
AbfrageMitZweiElementOr = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                         "\Diagnoses\(K00-K94) Dise~rl1r"],
                                              verknüpfungen=['or'])
print("kohortengröße:", AbfrageMitZweiElementOr.kohortengröße)
print("Nebendiagnose:", AbfrageMitZweiElementOr.df_nebendia)
print("Zeitpunkt:", AbfrageMitZweiElementOr.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitZweiElementOr.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitZweiElementOr.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitZweiElementOr.y_achse_altersverteilung)
# kann man 2 Elemente auswählen : and
print("_______")
print("kann man 2 Elemente auswählen : and")
AbfrageMitZweiElementAnd = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                          "\Diagnoses\(K00-K94) Dise~rl1r"],
                                               verknüpfungen=['and'])
print("kohortengröße:", AbfrageMitZweiElementAnd.kohortengröße)
print("Nebendiagnose:", AbfrageMitZweiElementAnd.df_nebendia)
print("Zeitpunkt:", AbfrageMitZweiElementAnd.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitZweiElementAnd.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitZweiElementAnd.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitZweiElementAnd.y_achse_altersverteilung)
# kann man 2 Elemente auswählen : and not
print("_______")
print("kann man 2 Elemente auswählen :  not")
AbfrageMitZweiElementNot = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                          "\Diagnoses\(K00-K94) Dise~rl1r"],
                                               verknüpfungen=['not'])
print("kohortengröße:", AbfrageMitZweiElementNot.kohortengröße)
print("Nebendiagnose:", AbfrageMitZweiElementNot.df_nebendia)
print("Zeitpunkt:", AbfrageMitZweiElementNot.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitZweiElementNot.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitZweiElementNot.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitZweiElementNot.y_achse_altersverteilung)

# kann man 10 Elemente auswählen : and
# print("_______")
# print("kann man 10 Elemente auswählen : and")
# AbfrageMit10ElementAnd=kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
#                                                  "\Diagnoses\(K00-K94) Dise~rl1r",
#                                                   "\Diagnoses\(J00-J99) Dise~45pn",
#                                                   "\Diagnoses\(K00-K94) Dise~rl1r",
#                                                  "\Diagnoses\(S00-T88) Inju~yy6i",
#                                                  "\Diagnoses\(P00-P96) Cert~6976",
#                                                   "\Diagnoses\(F01-F99) Ment~44ly",
#                                                   "\Diagnoses\(R00-R99) Symp~mt2x",
#                                                   "\Diagnoses\(V00-Y99) Exte~2k58",
#                                                   "\Diagnoses\(Z00-Z99) Fact~rmj9"]
#                                         ,verknüpfungen=['and','and','and','and','and',
#                                                         'and','and','and','and'])
# print("kohortengröße:",AbfrageMit10ElementAnd.kohortengröße)
# print("Nebendiagnose:",AbfrageMit10ElementAnd.df_nebendia)
# print("Zeitpunkt:",AbfrageMit10ElementAnd.zeitpunkt)
# print("Geschlechterverteilung: \n",AbfrageMit10ElementAnd.geschlecht_value_counts)
# print("Altersverteilung -x Achse:",AbfrageMit10ElementAnd.x_achse_altersverteilung)
# print("Altersverteilung -y Achse:",AbfrageMit10ElementAnd.y_achse_altersverteilung)
# kann man 10 Elemente auswählen : or
# print("_______")
# print("kann man 10 Elemente auswählen : or")
# AbfrageMit10ElementOr=kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
#                                                    "\Diagnoses\(K00-K94) Dise~rl1r",
#                                                    "\Diagnoses\(J00-J99) Dise~45pn",
#                                                    "\Diagnoses\(K00-K94) Dise~rl1r",
#                                                    "\Diagnoses\(S00-T88) Inju~yy6i",
#                                                   "\Diagnoses\(P00-P96) Cert~6976",
#                                                    "\Diagnoses\(F01-F99) Ment~44ly",
#                                                    "\Diagnoses\(R00-R99) Symp~mt2x",
#                                                    "\Diagnoses\(V00-Y99) Exte~2k58",
#                                                   "\Diagnoses\(Z00-Z99) Fact~rmj9"]
#                                         ,verknüpfungen=['or','or','or','or','or',
#                                                         'or','or','or','or'])
# print("kohortengröße:",AbfrageMit10ElementOr.kohortengröße)
# print("Nebendiagnose:",AbfrageMit10ElementOr.df_nebendia)
# print("Zeitpunkt:",AbfrageMit10ElementOr.zeitpunkt)
# print("Geschlechterverteilung: \n",AbfrageMit10ElementOr.geschlecht_value_counts)
# print("Altersverteilung -x Achse:",AbfrageMit10ElementOr.x_achse_altersverteilung)
# print("Altersverteilung -y Achse:",AbfrageMit10ElementOr.y_achse_altersverteilung)
# kann man 2 Elemente auswählen : and not
#print("_______")
#print("kann man 2 Elemente auswählen :  eine Verknüpfung zu viel")
#AbfrageMitZweiElementZuViel = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       #   "\Diagnoses\(K00-K94) Dise~rl1r"],
                                             #  verknüpfungen=['and','and'])
#print("kohortengröße:", AbfrageMitZweiElementZuViel.kohortengröße)
#print("Nebendiagnose:", AbfrageMitZweiElementZuViel.df_nebendia)
#print("Zeitpunkt:", AbfrageMitZweiElementZuViel.zeitpunkt)
#print("Geschlechterverteilung: \n", AbfrageMitZweiElementZuViel.geschlecht_value_counts)
#print("Altersverteilung -x Achse:", AbfrageMitZweiElementZuViel.x_achse_altersverteilung)
#print("Altersverteilung -y Achse:", AbfrageMitZweiElementZuViel.y_achse_altersverteilung)

print("_______")
print("kann man 2 Elemente auswählen : eine Verknüfung zu wenig")
AbfrageMitZweiElementZuWenig = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                          "\Diagnoses\(K00-K94) Dise~rl1r"],
                                               verknüpfungen=[])
print("kohortengröße:", AbfrageMitZweiElementZuWenig.kohortengröße)
print("Nebendiagnose:", AbfrageMitZweiElementZuWenig.df_nebendia)
print("Zeitpunkt:", AbfrageMitZweiElementZuWenig.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitZweiElementZuWenig.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitZweiElementZuWenig.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitZweiElementZuWenig.y_achse_altersverteilung)


print("_______")
print("kann man 3 Elemente auswählen : eine Verknüfung zu wenig")
AbfrageMitDreiElementZuWenig = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                          "\Diagnoses\(K00-K94) Dise~rl1r",
                                                              "\Diagnoses\(I00-I99) Dise~3w8h",  ],
                                               verknüpfungen=['and'])
print("kohortengröße:", AbfrageMitDreiElementZuWenig.kohortengröße)
print("Nebendiagnose:", AbfrageMitDreiElementZuWenig.df_nebendia)
print("Zeitpunkt:", AbfrageMitDreiElementZuWenig.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageMitDreiElementZuWenig.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageMitDreiElementZuWenig.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageMitDreiElementZuWenig.y_achse_altersverteilung)

print("_______")
print("was passiert wenn Krankheit gar nicht in I2b2 drin ist?")
AbfrageKrankheitNichtInI2B2= kab.Kohortenabfrage(kriterien=["IchBinSicherNichtDrin",
                                                            ],
                                               verknüpfungen=[])
print("kohortengröße:", AbfrageKrankheitNichtInI2B2.kohortengröße)
print("Nebendiagnose:", AbfrageKrankheitNichtInI2B2.df_nebendia)
print("Zeitpunkt:", AbfrageKrankheitNichtInI2B2.zeitpunkt)
print("Geschlechterverteilung: \n", AbfrageKrankheitNichtInI2B2.geschlecht_value_counts)
print("Altersverteilung -x Achse:", AbfrageKrankheitNichtInI2B2.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", AbfrageKrankheitNichtInI2B2.y_achse_altersverteilung)

print("_______")
print("was wenn Krankheit leer?")
KrankheitLeer= kab.Kohortenabfrage(kriterien=["_Diagnoses%(U%",
                                                            ],
                                               verknüpfungen=[])
print("kohortengröße:", KrankheitLeer.kohortengröße)
print("Nebendiagnose:", KrankheitLeer.df_nebendia)
print("Zeitpunkt:", KrankheitLeer.zeitpunkt)
print("Geschlechterverteilung: \n", KrankheitLeer.geschlecht_value_counts)
print("Altersverteilung -x Achse:", KrankheitLeer.x_achse_altersverteilung)
print("Altersverteilung -y Achse:", KrankheitLeer.y_achse_altersverteilung)