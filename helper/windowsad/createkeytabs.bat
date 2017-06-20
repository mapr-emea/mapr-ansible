@ECHO OFF

set MAPR_HOSTS=hosts.txt
set MAPR_TEC_USER=TEC-MAPR
set REALM=PS.MAPR.COM

for /F "tokens=*" %%A in (%MAPR_HOSTS%) do (
  ktpass /princ mapr/%%A@%REALM% /mapuser %MAPR_TEC_USER% +rndPass /out out\mapr-%%A.keytab /crypto RC4-HMAC-NT /ptype KRB5_NT_PRINCIPAL
  echo mapr-%%A.keytab
  ktpass /princ cldb/%%A@%REALM% /mapuser %MAPR_TEC_USER% +rndPass /out out\cldb-%%A.keytab /crypto RC4-HMAC-NT /ptype KRB5_NT_PRINCIPAL
  echo mapr-%%A.keytab
  ktpass /princ HTTP/%%A@%REALM% /mapuser %MAPR_TEC_USER% +rndPass /out out\HTTP-%%A.keytab /crypto RC4-HMAC-NT /ptype KRB5_NT_PRINCIPAL
  echo mapr-%%A.keytab
)

PAUSE