## #!/bin/ksh

echo creation table tmp listeville

mysql -u user_openvet -p0000 -e  'use OpenVet10b'
echo importation villes dans tmp listeville
mysql -u user_openvet -p0000 OpenVet10b < villes_de_france.sql 
echo copie listeville dans openvet
mysql -u user_openvet -p0000 OpenVet10b < copie_tabletmp_villedefrance_openvet10b.sql
