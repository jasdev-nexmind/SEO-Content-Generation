@echo off
set "CompanyName[0]=NexMind"
set "CompanyName[1]=Dynamic Brands"
set "CompanyName[2]=Time"
set "CompanyName[3]=Oreo"
set "CompanyName[4]=Taj"
set "CompanyName[5]=Hertz"
set "CompanyName[6]=Apple"
set "CompanyName[7]=Google"
set "CompanyName[8]=Microsoft"

set "Keyword[0]=Sofa Manufacturing Company in Malaysia"
set "Keyword[1]=Wifi Service Provider in Malaysia"
set "Keyword[2]=Best Biscuit Company in Malaysia"
set "Keyword[3]=Best Hotel in Malaysia"
set "Keyword[4]=Car Rental Company in Malaysia"
set "Keyword[5]=Best Ice Cream in Malaysia"
set "Keyword[6]=Top Tech Company in Malaysia"
set "Keyword[7]=Car Delership in Malaysia"
set "Keyword[8]=Online Florist in Malaysia"


:: Path to your Python script, modify if needed
set "ScriptPath=.\seo-temp.py"

set /A "index1=(%RANDOM% %% 9)"
set /A "index2=(%RANDOM% %% 9)"
:: These are the predefined inputs


call echo Company Name: %%CompanyName[%index1%]%%
call echo Keyword: %%Keyword[%index2%]%%


:: This is where you run the Python script with the inputs
call python %ScriptPath% "%%CompanyName[%index1%]%%" "%%Keyword[%index2%]%%"

exit
