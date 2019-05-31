import Kohortenabfrage as kab
import pandas as pd
import Verarbeitungsschicht as bl

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