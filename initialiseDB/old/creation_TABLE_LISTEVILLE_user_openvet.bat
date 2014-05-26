## #!/bin/ksh

echo creation table tmp listeville

mysql -u user_openvet -p0000 -e  'use OpenVet10'
echo importation villes dans tmp listeville
mysql -u user_openvet -p0000 OpenVet10 < villes_de_france.sql 
echo copie listeville dans openvet
mysql -u user_openvet -p0000 OpenVet10 < copie_tabletmp_villedefrance_openvet.sql
