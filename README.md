# chnroutes VPN 自动分流

利用来自[APNIC](http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest)的数据生成路由命令脚本，让VPN客户端在连接时自动执行。通过这些路由脚本，可以让用户在使用VPN作为默认网关时，不使用VPN访问中国国内IP，从而减轻VPN负担，并提高访问国内网站的速度。

## 基本约定

在使用这些脚本之前，请确保你在自己的电脑上已经成功配置好一个VPN（IPsec or Ikev2 均可），并且让之以默认网关的方式运行（通常是默认配置），即VPN连接之后所有网络流量都通过VPN。


## Mac OS X

1. 在终端中执行

		$ python chnroutes.py -p mac

	这将生成`addRoute.sh`和`deleteRoute.sh`两个文件；
	
2. 使用时只需执行`RefreshRoute.sh`即可
3. 稍等片刻可以`ping baidu.com`和`ping google.com`查看效果。
4. 可以把`RefreshRoute.sh`加入开机启动项，它具有自动检测网络环境是否变化的功能，如果变换wifi或者有线网，会自动更新路由表。


## Windows

1. 在命令提示符中执行

		$ python chnroutes.py -p win
	
	这将生成`Refresh.bat`可执行脚本；
	
2. 可以将`Refresh.bat`加入开机启动项，开机后会自动更新路由表。也可双击手动添加。


## 注意事项

* 环境：`python2.7`
* 因为这些IP数据不是固定不变的，建议每隔一段时间更新一次；
* 在macOS中后台初始化大概需要半分钟，而Windows初始化要一分钟左右。不要问我为什么，bat脚本真是醉了。。。
* macOS开机后会每隔一定时间检测，自动更新路由表；而Windows只会在开机时检测等待到联网时更新一次路由表，如果更换网络环境就要重启电脑。
* 在Windows上联网时，无线和WiFi只能选一种(要关闭另一种网络)，不能同时连接，否则添加路由失败。重启可解决！
* 注意Windows在联网一分钟左右再连VPN即可，不然程序可能添加部分节点失败，而macOS上不用担心这个问题。macOS再次体现出优越性。。。

## 信息反馈

本项目的脚本都是测试通过的，如果在其它拨号方式下，脚本不能运作，请添加新的Issue。

如果觉得有用的话，请Star一下吧！