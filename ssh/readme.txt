这是我用python开源库paramiko进行ssh扫描爆破，前期弃用它，主要是因为安装有问题，具体原因不清楚，之前我是用python2.7编写代码，所以使用pip install paramiko 安装，但是出现很多报错，之后我再使用源码安装 python setup.py build && python setup.py install 但还是报错。接着我尝试用pip3安装，最后成功了，所以这个代码我是用python3编写的。
1、环境部署：
			我用的系统是Ubuntu14.04
			apt-get install python3-pip
			pip3 install --upgrade setuptools
			pip3 install paramiko
2、代码运行：
			更改读取、保存文件的目录即可
			python3 py文件路径
功能：
	这里我采用多线程处理，扫描爆破速度非常快！
	与telnet编写不同的是，这里我是直接利用nmap扫描开放22端口的主机ip集尝试爆破，后面也可以将namp模块直接添加进去