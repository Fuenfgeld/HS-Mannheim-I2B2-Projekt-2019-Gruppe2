from unittest import TestCase
import psycopg2 as psy
import Querystack as qs
import pandas as pd
import Verarbeitungsschicht as bl
import KnotenListe as kl
import Abfragen as ab
import Kohortenabfrage as kab
import pandas as pd
import Verarbeitungsschicht as bl

con = bl.connection_zu_datenbank_aufbauen()

s = qs.Querystack()
def test_stack_init():
    s.size()==0

def test_push1_size():
        item = 5
        s.push(item)
        s.size == 5

def test_push2_size():
            s.push(5)
            s.push(6)
            s.size() == 2

def test_push2_pop1_size():
            s.push(5)
            s.push(6)
            s.pop()
            s.size == 1

def test_push2_pop1_value():
            s.push(8)
            s.push(9)
            s.pop() == 9

def test_push2_pop2_size():
        s.push("Glob")
        s.push("Blob")
        s.pop()
        s.pop()
        s.size == 0

def test_push2_pop2_value():
        s.push("Glob")
        s.push("Blob")
        s.pop()
        s.pop == "Glob"

def test_peek_push1():
        s.push(88)
        s.peek == 88

def test_peek_push3_pop1():
        s.push(7)
        s.push(889)
        s.push(3)
        s.pop()
        s.peek == 889

def test_pop_empty():
        s.pop() == None

def test_peek_empty():
        s.peek() == None

connection = bl.connection_zu_datenbank_aufbauen()

dfsichereHauptdiagnoseAndOR = pd.read_sql_query(
    "select distinct i2b2demodata.patient_dimension.patient_num,i2b2demodata.patient_dimension.sex_cd,i2b2demodata.patient_dimension.age_in_years_num,i2b2demodata.patient_dimension.language_cd,i2b2demodata.patient_dimension.race_cd from (select concept.concept_path, concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape'')) concept join i2b2demodata.observation_fact       on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path, concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '')) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",
    con=connection)
dfsichereNebendiagnoseAndOR = pd.read_sql_query(
    "select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/46 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') OR (i2b2demodata.concept_dimension.concept_path like   '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) AND (nebendia.concept_cd != k1.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",
    con=connection)
SichereGrößeAndOR = len(dfsichereHauptdiagnoseAndOR)
SicheresAlterAndOR = dfsichereHauptdiagnoseAndOR['age_in_years_num']
SicheresGeschlechtAndOR = dfsichereHauptdiagnoseAndOR['sex_cd']
SichereSpracheAndOR = dfsichereHauptdiagnoseAndOR['language_cd']
SichereRasseAndOR = dfsichereHauptdiagnoseAndOR['race_cd']

dfsichereHauptdiagnoseAndAnd = pd.read_sql_query(
    "select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k2 on k1.patient_num = k2.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",
    con=connection)
dfSichereNebendiagnoseAndAnd = pd.read_sql_query(
    "select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/4 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k2 on k1.patient_num = k2.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) AND (nebendia.concept_cd != k1.concept_cd) AND (nebendia.concept_cd != k2.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",
    con=connection)
SichereGrößeAndAnd = len(dfsichereHauptdiagnoseAndAnd)
SicheresAlterAndAnd = dfsichereHauptdiagnoseAndAnd['age_in_years_num']
SicheresGeschlechtAndAnd = dfsichereHauptdiagnoseAndAnd['sex_cd']
SichereSpracheAndAnd = dfsichereHauptdiagnoseAndAnd['language_cd']
SichereRasseAndAnd = dfsichereHauptdiagnoseAndAnd['race_cd']

dfsichereHauptdiagnoseOrAnd = pd.read_sql_query(
    "select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like  '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",
    con=connection)
dfSichereNebendiagnoseOrAnd = pd.read_sql_query(
    "select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/20 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) AND (nebendia.concept_cd != k1.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",
    con=connection)
SichereGrößeOrAnd = len(dfsichereHauptdiagnoseOrAnd)
SicheresAlterOrAnd = dfsichereHauptdiagnoseOrAnd['age_in_years_num']
SicheresGeschlechtOrAnd = dfsichereHauptdiagnoseOrAnd['sex_cd']
SichereSpracheOrAnd = dfsichereHauptdiagnoseOrAnd['language_cd']
SichereRasseOrAnd = dfsichereHauptdiagnoseOrAnd['race_cd']

dfsichereHauptdiagnoseOrOr = pd.read_sql_query(
    "select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like  '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') OR (i2b2demodata.concept_dimension.concept_path like  '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num ",
    con=connection)
dfSichereNebendiagnoseOrOr = pd.read_sql_query(
    "select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/122 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like   '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(Q00-Q99) Cong~t96i%' escape '') ) concept join i2b2demodata.observation_fact  on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",
    con=connection)
SichereGrößeOrOr = len(dfsichereHauptdiagnoseOrOr)
SicheresAlterOrOr = dfsichereHauptdiagnoseOrOr['age_in_years_num']
SicheresGeschlechtOrOr = dfsichereHauptdiagnoseOrOr['sex_cd']
SichereSpracheOrOr = dfsichereHauptdiagnoseOrOr['language_cd']
SichereRasseOrOr = dfsichereHauptdiagnoseOrOr['race_cd']

dfsichereHauptdiagnoseAnd=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",con=connection)
dfSichereNebendiagnoseAnd=pd.read_sql_query("select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/34 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from(select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k1 on k0.patient_num = k1.patient_num join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) AND (nebendia.concept_cd != k1.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",con=connection)
SichereGrößeAnd = len(dfsichereHauptdiagnoseAnd)
SicheresAlterAnd = dfsichereHauptdiagnoseAnd['age_in_years_num']
SicheresGeschlechtAnd = dfsichereHauptdiagnoseAnd['sex_cd']
SichereSpracheAnd = dfsichereHauptdiagnoseAnd['language_cd']
SichereRasseAnd = dfsichereHauptdiagnoseAnd['race_cd']

dfsichereHauptdiagnoseOr=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd, i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension  on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num",con=connection)
dfSichereNebendiagnoseOr=pd.read_sql_query("select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl, TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/117 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') OR (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(I00-I99) Dise~3w8h%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",con=connection)
SichereGrößeOr = len(dfsichereHauptdiagnoseOr)
SicheresAlterOr = dfsichereHauptdiagnoseOr['age_in_years_num']
SicheresGeschlechtOr = dfsichereHauptdiagnoseOr['sex_cd']
SichereSpracheOr = dfsichereHauptdiagnoseOr['language_cd']
SichereRasseOr = dfsichereHauptdiagnoseOr['race_cd']

dfsichereHauptdiagnose=pd.read_sql_query("select distinct i2b2demodata.patient_dimension.patient_num, i2b2demodata.patient_dimension.sex_cd,i2b2demodata.patient_dimension.age_in_years_num, i2b2demodata.patient_dimension.language_cd, i2b2demodata.patient_dimension.race_cd from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num ",con=connection)
dfSichereNebendiagnose=pd.read_sql_query("select nebendia.name_char as diagnose, count(distinct i2b2demodata.patient_dimension.patient_num) as anzahl,TRUNC((count(distinct i2b2demodata.patient_dimension.patient_num)*1.0)/83 * 100 , 2) as prozent from (select concept.concept_path,concept.concept_cd, i2b2demodata.observation_fact.patient_num from (select i2b2demodata.concept_dimension.concept_path, i2b2demodata.concept_dimension.concept_cd from i2b2demodata.concept_dimension where (i2b2demodata.concept_dimension.concept_path like '%\Diagnoses\(A00-B99) Cert~ugmm%' escape '') ) concept join i2b2demodata.observation_fact on concept.concept_cd = i2b2demodata.observation_fact.concept_cd join i2b2demodata.patient_dimension on i2b2demodata.patient_dimension.patient_num = i2b2demodata.observation_fact.patient_num) k0 join i2b2demodata.patient_dimension on k0.patient_num = i2b2demodata.patient_dimension.patient_num join (select i2b2demodata.observation_fact.patient_num, i2b2demodata.concept_dimension.concept_cd,i2b2demodata.concept_dimension.name_char from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd) nebendia on (nebendia.patient_num =k0.patient_num) where (nebendia.concept_cd like 'ICD%') AND (nebendia.concept_cd != k0.concept_cd) group by nebendia.name_char order by Anzahl desc limit 10",con=connection)
SichereGröße = len(dfsichereHauptdiagnose)
SicheresAlter = dfsichereHauptdiagnose['age_in_years_num']
SicheresGeschlecht = dfsichereHauptdiagnose['sex_cd']
SichereSprache = dfsichereHauptdiagnose['language_cd']
SichereRasse = dfsichereHauptdiagnose['race_cd']
def testKohortenabfrageDreiKriterienAndOR():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h",
                                                       "\Diagnoses\(Q00-Q99) Cong~t96i"],
                                            verknüpfungen=['AND', 'or']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
    SichereGrößeAndOR == KlasseKohortengröße
    SichereRasseAndOR == KlasseRasseDF
    SichereSpracheAndOR == KlasseSpracheDF
    SicheresGeschlechtAndOR == KlasseGeschlechtDF
    SicheresAlterAndOR == KlasseAlterDF
    dfsichereNebendiagnoseAndOR == KlasseNebendiaDF


def testKohortenabfrageDreiKritierenAndAnd():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h",
                                                       "\Diagnoses\(Q00-Q99) Cong~t96i"],
                                            verknüpfungen=['AND', 'AND']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    SichereGrößeAndAnd == KlasseKohortengröße
    SichereRasseAndAnd == KlasseRasseDF
    SichereSpracheAndAnd == KlasseSpracheDF
    SicheresGeschlechtAndAnd == KlasseGeschlechtDF
    SicheresAlterAndAnd == KlasseAlterDF
    dfSichereNebendiagnoseAndAnd == zutestendeAbfrage.df_nebendia


def testKohortenabfrageDreiKritierenOrAnd():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h",
                                                       "\Diagnoses\(Q00-Q99) Cong~t96i"],
                                            verknüpfungen=['OR', 'AND']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    SichereGrößeOrAnd == KlasseKohortengröße
    SichereRasseOrAnd == KlasseRasseDF
    SichereSpracheOrAnd == KlasseSpracheDF
    SicheresGeschlechtOrAnd == KlasseGeschlechtDF
    SicheresAlterOrAnd == KlasseAlterDF
    dfSichereNebendiagnoseOrAnd == zutestendeAbfrage.df_nebendia


def testKohortenabfrageDreiKritierenOrOr():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h",
                                                       "\Diagnoses\(Q00-Q99) Cong~t96i"],
                                            verknüpfungen=['OR', 'or']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
    SichereGrößeOrOr == KlasseKohortengröße
    SichereRasseOrOr == KlasseRasseDF
    SichereSpracheOrOr == KlasseSpracheDF
    SicheresGeschlechtOrOr == KlasseGeschlechtDF
    SicheresAlterOrOr == KlasseAlterDF
    dfSichereNebendiagnoseOrOr == KlasseNebendiaDF


def testKohortenabfrageZweiKritierenAnd():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h"],
                                            verknüpfungen=['and']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
    SichereGrößeAnd == KlasseKohortengröße
    SichereRasseAnd == KlasseRasseDF
    SichereSpracheAnd == KlasseSpracheDF
    SicheresGeschlechtAnd == KlasseGeschlechtDF
    SicheresAlterAnd == KlasseAlterDF
    dfSichereNebendiagnoseAnd == KlasseNebendiaDF


def testKohortenabfrageZweiKritierenAnd():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm",
                                                       "\Diagnoses\(I00-I99) Dise~3w8h"],
                                            verknüpfungen=['or']
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    SichereGrößeOr == KlasseKohortengröße
    SichereRasseOr == KlasseRasseDF
    SichereSpracheOr == KlasseSpracheDF
    SicheresGeschlechtOr == KlasseGeschlechtDF
    SicheresAlterOr == KlasseAlterDF
    dfSichereNebendiagnoseOr == zutestendeAbfrage.df_nebendia

def testKohortenabfrageEinKritieren():
    zutestendeAbfrage = kab.Kohortenabfrage(kriterien=["\Diagnoses\(A00-B99) Cert~ugmm"],
                                            verknüpfungen=[]
                                            )
    KlasseKohortengröße = zutestendeAbfrage.kohortengröße
    KlasseAlterDF = zutestendeAbfrage.df_alter
    KlasseGeschlechtDF = zutestendeAbfrage.df_geschlecht
    KlasseSpracheDF = zutestendeAbfrage.df_sprache
    KlasseRasseDF = zutestendeAbfrage.df_rasse
    KlasseNebendiaDF = zutestendeAbfrage.df_nebendia
    SichereGröße == KlasseKohortengröße
    SichereRasse == KlasseRasseDF
    SichereSprache == KlasseSpracheDF
    SicheresGeschlecht == KlasseGeschlechtDF
    SicheresAlter == KlasseAlterDF
    dfSichereNebendiagnose == KlasseNebendiaDF


# Abfragen
class TestDataframe_ebene_finden(TestCase):

    def test_dataframe_ebene_finden0(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=0", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(0,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden1(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=1", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(1,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden2(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=2", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(2,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden3(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=3", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(3,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden4(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=4", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(4,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden5(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=5", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(5,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden6(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=6", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(6,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden7(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=7", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(7,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden8(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=8", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(8,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden9(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=9", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(9,con)
    df.equals(df_2)

    def test_dataframe_ebene_finden10(self):

        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen

    df = pd.read_sql_query("SELECT c_symbol, c_fullname, c_path, c_name  from i2b2metadata.icd10_icd9 where c_tablename='concept_dimension' and c_hlevel=10", con=con)
    from Abfragen import dataframe_ebene_finden
    df_2 = dataframe_ebene_finden(10,con)
    df.equals(df_2)

class TestDataframe_knoten_mit_größe_in_einer_ebene_finden(TestCase):

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden0(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=0",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(0, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden1(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=1", con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(1, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden2(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=2",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(2, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden3(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=3",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(3, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden4(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=4",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden5(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=5",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(5, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden6(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=6",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(6, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden7(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=7",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(7, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden8(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=8",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(8, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden9(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=9",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(9, con)
        df.equals(df_2)

    def test_dataframe_knoten_mit_größe_in_einer_ebene_finden10(self):
        df = pd.read_sql_query(
            "SELECT c_symbol, c_fullname, c_path, c_name, coalesce(demo.Anzahl,0) from i2b2metadata.icd10_icd9 LEFT JOIN (Select count(distinct i2b2demodata.observation_fact.patient_num) as Anzahl,i2b2demodata.observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path from i2b2demodata.observation_fact join i2b2demodata.concept_dimension on i2b2demodata.observation_fact.concept_cd=i2b2demodata.concept_dimension.concept_cd group by observation_fact.concept_cd, i2b2demodata.concept_dimension.concept_path) demo on i2b2metadata.icd10_icd9.c_fullname=demo.concept_path where c_tablename='concept_dimension' and c_hlevel=10",
            con=con)

        df_2 = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(10, con)
        df.equals(df_2)

# Verarbeitungsschicht
class TestConnection_zu_datenbank_aufbauen(TestCase):
    def test_connection_zu_datenbank_aufbauen(self):
        connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
        return connection
        self.assertEqual(connection_zu_datenbank_aufbauen(), connection)


class TestAbfrage_grundgesamtheit(TestCase):
    def test_abfrage_grundgesamtheit(self):
        from Verarbeitungsschicht import abfrage_grundgesamtheit
        from Verarbeitungsschicht import connection_zu_datenbank_aufbauen
        pd.testing.assert_frame_equal(abfrage_grundgesamtheit(db_connection=connection_zu_datenbank_aufbauen()),
                                      pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension',
                                                        con=psy.connect(database="i2b2", user="i2b2",
                                                                        password="demouser", host="129.206.7.75",
                                                                        port="5432")))


class TestAbfrage_durchführen(TestCase):
    def test_abfrage_durchführen(self):
        from Verarbeitungsschicht import abfrage_durchführen
        df=pd.read_sql_query('SELECT * from i2b2demodata.patient_dimension', con=con)
        abfrage='SELECT * from i2b2demodata.patient_dimension'
        df_2= abfrage_durchführen(abfrage,con)
        print(df.equals(df_2))



class TestUmwandeln_zu_sql_statement(TestCase):
    def test_umwandeln_zu_sql_statement(self):
        elementliste=['a','b','c']
        sql_statement='SELECT * FROM i2b2demodata.patient_dimension WHERE a b c'
        print(sql_statement)

        from Verarbeitungsschicht import umwandeln_zu_sql_statement
        print(umwandeln_zu_sql_statement(elementliste))

        self.assertEqual(umwandeln_zu_sql_statement(elementliste), sql_statement)



class TestQuery_umwandeln_in_ergebniss_dataframes(TestCase):
    def test_query_umwandeln_in_ergebniss_dataframes(self):
         df=pd.read_sql_query("SELECT patient_num, sex_cd, age_in_years_num from i2b2demodata.patient_dimension where age_in_years_num =19", con=con)
         df_geschlecht= df['sex_cd']
         df_alter=df['age_in_years_num']
         df_patient_Anzahl=df['patient_num'].count()
         from Verarbeitungsschicht import query_umwandeln_in_ergebniss_dataframes
         alles=query_umwandeln_in_ergebniss_dataframes(con,[])
         allesAnzahl=alles[0]
         allesAlter=alles[2]
         allesGeschlecht=alles[1]
         allesAnzahl==df_patient_Anzahl
         allesAlter.equals(df_alter)
         allesGeschlecht.equals(df_geschlecht)


# Knotenliste
def Hilfe_Knotenliste():
    con = bl.connection_zu_datenbank_aufbauen()

    knotenliste_gesamt = []

    df_ebene = ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(4, con)

    knotenliste_gesamt.append(kl.knotenliste_für_eine_ebene_erstellen(df_ebene))

    return knotenliste_gesamt


def test_knotenliste():
    liste = Hilfe_Knotenliste()

    erwarteteliste = Hilfe_Knotenliste()

    assert type(liste) == list


class TestAus_knotenliste_baum_erstellen(TestCase):
    def  test_aus_knotenliste_baum_erstellen(self):
        from KnotenListe import knotenliste_gesamt_erstellen, aus_knotenliste_baum_erstellen
        knoten=knotenliste_gesamt_erstellen()
        baum=aus_knotenliste_baum_erstellen(knoten)
        baum==knotenliste_gesamt_erstellen()
    def knotenlistegesamterstellen(self):
        from KnotenListe import knotenliste_für_eine_ebene_erstellen
        con=bl.connection_zu_datenbank_aufbauen()
        knotenliste_gesamt=[]

        for i in range(0,11,1):
            df_ebene=ab.dataframe_knoten_mit_größe_in_einer_ebene_finden(i,con)
            knotenliste_gesamt.append(knotenliste_für_eine_ebene_erstellen(df_ebene))
        return knotenliste_gesamt


class TestKnotenliste_für_eine_ebene_erstellen(TestCase):
    def test_knotenliste_für_eine_ebene_erstellen(self):
        dict_ebene = {'name': ['Knoten1', 'Knoten2'], 'fullname': ['Fullname1', 'Fullname2'],
                      'Pfad': ['Pfad1', 'Pfad2'],
                      'Symbol': ['Symbol1', 'Symbol2'], 'Size': [0, 1]}
        df_ebene = pd.DataFrame(data=dict_ebene)
        print(df_ebene)
        from KnotenMitWert import node_with_value
        knotenliste = [
            node_with_value(name='Knoten1', fullname='Fullname1', pfad='Pfad1', size=0),
            node_with_value(name='Knoten2', fullname='Fullname2', pfad='Pfad2', size=1)]
        from KnotenListe import knotenliste_für_eine_ebene_erstellen
        knotenliste_für_eine_ebene_erstellen(df_ebene)==knotenliste


class TestKnotenliste_gesamt_erstellen(TestCase):
    def test_knotenliste_gesamt_erstellen(self):

        from KnotenListe import knotenliste_gesamt_erstellen
        from tree_dictionary_import_export import treedictionary_aus_pickle_importieren
        baum=treedictionary_aus_pickle_importieren('baum_mit_var_text')
        baum_Methode=knotenliste_gesamt_erstellen()
        baum==baum_Methode

class TestQueryStackSingleton(TestCase):

    def testQueryStackerstInstanzDannKonstruktor(self):
        import Querystack
        import pytest
        with pytest.raises(Exception):
            qIK = Querystack.instance()
            print(qIK)
            qIK2 = Querystack()
            print(qIK2)

    def testQueryStackerstInstanzDannKonstruktor(self):
        import Querystack
        import pytest
        with pytest.raises(Exception):
            q1K = Querystack()
            print(q1K)
            q2K = Querystack()
            print(q2K)

    def testQueryStackerstInstanzDannKonstruktor(self):
        import Querystack
        q1 = Querystack.Querystack.instance()
        print(q1)
        q2 = Querystack.Querystack.instance()
        print(q2)
        q1 == q2


con.close
