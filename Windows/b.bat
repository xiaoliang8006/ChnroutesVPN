@echo off
:start

for /F %%i in ('ping www.baidu.com -n 1') do (set com=%%i)
echo %com%
if "%com%"=="Ping" (
echo hahaha
timeout /T 5
goto start
) else (
echo ya
timeout /T 10
)

for /F "tokens=3" %%* in ('route print ^| findstr "\<0.0.0.0\>"') do set "gw=%%*"
ipconfig /flushdns
route add 50.0.1.0 mask 255.255.255.0 %gw% metric 5
route add 51.0.2.0 mask 255.255.254.0 %gw% metric 5
timeout /T 10

