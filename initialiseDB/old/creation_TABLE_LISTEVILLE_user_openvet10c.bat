## #!/bin/ksh

echo creation table tmp listeville

mysql -u user_openvet -p0000 -e  'use OpenVet10c'
echo importation villes dans tmp listeville
mysql -u user_openvet -p0000 OpenVet10c < villes_de_france.sql 
echo copie listeville dans openvet
mysql -u user_openvet -p0000 OpenVet10c < copie_tabletmp_villedefrance_openvet10c.sql
