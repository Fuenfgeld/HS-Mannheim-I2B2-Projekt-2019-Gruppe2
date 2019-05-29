import Kohortenabfrage as kab
import pandas as pd
import Verarbeitungsschicht as bl

connection = bl.connection_zu_datenbank_aufbauen()


dfsichereHauptdiagnose=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num,i2b2demodata.patient_dimension.sex_cd,i2b2demodata.patient_dimension.age_in_years_num,i2b2demodata.patient_dimension.language_cd,i2b2demodata.patient_dimension.race_cd from (select concept.concept_path, concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape'')) concept join i2b2demodata.observation_fact       on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path, concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '')) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",con=connection)
SichereGröße=len(dfsichereHauptdiagnose)
SicheresAlter=dfsichereHauptdiagnose['age_in_years_num']
SicheresGeschlecht=dfsichereHauptdiagnose['sex_cd']
SichereSprache=dfsichereHauptdiagnose['language_cd']
SichereRasse=dfsichereHauptdiagnose['race_cd']

def testKohortenabfrage():
    ausderKlasse=kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                "\Diagnoses\(I00-I99) Dise~3w8h",
                                                "\Diagnoses\(Q00-Q99) Cong~t96i"],
                                     verknüpfungen=['AND','or']
                                     )
    print('blub',ausderKlasse.kohortengröße)
    HilfeHauptdia=dfsichereHauptdiagnose
    KlasseHauptdiaDF= ausderKlasse.df_hauptdia
    #print(len(KlasseHauptdiaDF))
    print('miau',len(HilfeHauptdia))
    KlasseKohortengröße=ausderKlasse.kohortengröße
    KlasseAlterDF= ausderKlasse.df_alter
    KlasseGeschlechtDF= ausderKlasse.df_geschlecht
    KlasseSpracheDF= ausderKlasse.df_sprache
    KlasseRasseDF= ausderKlasse.df_rasse
    print(SichereGröße==KlasseKohortengröße)
    SichereRasse==KlasseRasseDF
    SichereSprache==KlasseSpracheDF
    SicheresGeschlecht==KlasseGeschlechtDF
    SicheresAlter==KlasseAlterDF