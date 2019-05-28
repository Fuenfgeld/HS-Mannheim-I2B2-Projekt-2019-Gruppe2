from logik import db_abfragen as log
from datenhaltung import connection as connect

connection = connect.create_connection()
df = log.all_patients()

x_bis_9= ((df['age_in_years_num']).lt(9)).sum()
x_bis_17= (((df['age_in_years_num']).ge(10))&((df['age_in_years_num']).le(17))).sum()
x_bis_34=(((df['age_in_years_num']).ge(18))&((df['age_in_years_num']).le(34))).sum()
x_bis_44=(((df['age_in_years_num']).ge(35))&((df['age_in_years_num']).le(44))).sum()
x_bis_54=(((df['age_in_years_num']).ge(45))&((df['age_in_years_num']).le(54))).sum()
x_bis_64=(((df['age_in_years_num']).ge(55))&((df['age_in_years_num']).le(64))).sum()
x_bis_74=(((df['age_in_years_num']).ge(65))&((df['age_in_years_num']).le(74))).sum()
x_bis_84=(((df['age_in_years_num']).ge(75))&((df['age_in_years_num']).le(84))).sum()
x_gr_gl_65=((df['age_in_years_num']).ge(65)).sum()
x_gr_gl_85=((df['age_in_years_num']).ge(85)).sum()