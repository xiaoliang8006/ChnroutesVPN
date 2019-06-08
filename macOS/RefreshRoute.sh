#!/bin/bash
#######config#######
ROOTPASSWD="123456"
####################
dir=$(cd "$(dirname "$0")";pwd)
cd $dir
xattr -c *.*
touch /tmp/temp.txt


while true
do
#历史路由
b=$(cat /tmp/temp.txt)
#当前路由
a=$(netstat -nr | grep '^default' | grep -v 'utun' | sed 's/default *\([0-9\.]*\) .*/\1/')
#刚开机时只有当前路由没有历史路由
if [[ -n "$a" && -z "$b" ]]; then
echo "First add...."
/usr/bin/expect  << EOF
set timeout 60
#首次添加路由表
spawn sudo ./addRoute.sh
expect "Password:"
send "$ROOTPASSWD\r"
EOF
echo "****"
echo "Added!"
sleep 60
#当前路由不等于历史路由，说明网络更换，需要刷新路由表
elif [[ -n "$a" && -n "$b" && "$a" != "$b" ]]; then
echo "Refreshing...."
/usr/bin/expect  << EOF
set timeout 60
#先删除旧表
spawn sudo ./deleteRoute.sh
expect "Password:"
send "$ROOTPASSWD\r"
EOF
echo "****"
sleep 60
/usr/bin/expect  << EOF
set timeout 60
#更新路由
spawn sudo ./addRoute.sh
expect "Password:"
send "$ROOTPASSWD\r"
EOF
echo "****"
echo "Please wait a moment...."
sleep 60
#其他情况均等待，循环检测
else
echo "Checking...."
sleep 60
fi
done
