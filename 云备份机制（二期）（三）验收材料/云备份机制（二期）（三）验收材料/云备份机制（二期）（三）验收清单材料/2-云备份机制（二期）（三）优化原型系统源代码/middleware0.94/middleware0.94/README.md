核高基国产操作系统，云存储与备份服务——复旦大学所承担开发部分.

一. 运行所需环境：

    Ubuntu 14.04
    python 2.7.6


二. 部署步骤

a. 启动方物服务器：参见云存储服务器root下firstStep中的readme.txt文件；

b. 安装中间件（第2步成功直接跳转第4步）：

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# chmod +x setup.sh

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# ./setup.sh install
  
    说明：
    系统需要已安装有apt-get、dpkg。
    本步骤可以安装中间件所必须的软件包，包括：
    数据传输组件所需的curl；
    数据加密功能所需的安装工具pip，支持库rsa，加密包libsecrypto.deb

c. 安装中间件：如果第2步安装中间件运行出错，请自行安装，安装过程如下：

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# apt-get install curl

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# apt-get install python-pip

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# pip rsa

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# dpkg -P libcrypto

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# dpkg -i libsecrypto.deb

    安装完成后再执行下面命令以确认加密库已添加：

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# ls /usr/lib/libsecrypto.so

    /usr/lib/libsecrypto.so

d. 启动中间件：

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# ./setup start

e. 运行中间件：

    客户端与中间件、服务器的通信方式：客户端直接通过socket与中间件连接，发送请求给中间件，中间件与服务器通信后将结果返回给客户端，socket端口号为10000。

    客户端与中间件的通信协议和接口参数详见云存储与云备份中间件0.93版本使用说明.xlsx。

三．说明

    中间件以守护进程运行在客户端。

    关闭中间件：

    root@herh-VirtualBox:/home/herh/middleware0.93-1126# ./setup stop


	

-------2015.11.26



