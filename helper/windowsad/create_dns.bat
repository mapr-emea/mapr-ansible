@ECHO OFF
ECHO Start of Loop

FOR /L %%i IN (1,1,254) DO (
    dnscmd /RecordAdd ps.mapr.com ip-10-0-0-%%i A 10.0.0.%%i
)