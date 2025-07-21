---
title: 解决服务器占用过高导致数据库进程被杀无法打开网站的问题
author: 梦随乡兮
date: 2019-05-27 17:19:14+00:00
slug: mysqllife
tags:
- mysqllife
- 服务器
- 进程
- 网站开发
---
最近网站访问一高就会挂掉，之前看了不少网上大佬的教程发现每一个能用的。估计不是同一病症。
> **Error establishing a database connection**
这里记录一下修改教程，方便之后查验结果。
我用的是宝塔面板，所以修改起来比较简单：
按照网上的说法是PHP-FPM进程过多，导致mysql被杀掉。那么就改PHP-FPM好了。
打开网站运行的php版本设置界面
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-07-09.jpg" alt="" width="636" height="397" />
将上图的4个数值全部调小，
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-08-57.jpg" alt="" width="697" height="291" />
设置虚拟内存，按照大佬的说法，无论配置多好，虚拟内存都是有必要设置一下的。
Swap 推荐值：2G 和 2G 以下内存的服务器，设置成和物理内存相同容量 SWAP；2G 以上的，设置为 2G。如果跑的程序特别耗费内存，2G 内存以上的 Swap 也可以设置与内存相同。
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-10-52.jpg" alt="" width="635" height="342" />
安装php缓存插件，在网站出现数据库链接问题之前我就已经安装了。
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-12-29.jpg" alt="" width="634" height="530" />
php 配置调整，同样在 php 管理的配置修改中，memory_limit 脚本内存限制修改成 256M，这样 wordpress 跑起来更顺畅了；upload_max_filesize 允许上传文件的最大尺寸，像 avada 模板可能会超过这个数值无法上传，需要修改为大于上传文件的数值。
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-13-43.jpg" alt="" width="634" height="554" />
在配置文件中 Ctrl+F 搜索 memory_limit，把默认值修改成 256M，保存。
<img src="https://r2.imsxx.com/wp-content/uploads/2019/05/Snipaste_2019-05-28_01-14-53.jpg" alt="" width="636" height="385" />
PHP 并发调整，宝塔在安装的时候就把推荐配置作为默认了，如果我们实际上不需要太多的并发，可以下调。调整并发也会连同调整下面的进程数，当然你也可以单独设置。
做完所有调整后保存并重启服务器，以便让设置完全生效。具体这次调整后还会不会出现数据库连接报错的问题还需要观察。先就这样。
参考文章：
<a rel="nofollow" href="https://www.vpsss.net/6600.html" target="_blank" rel="noopener noreferrer">如何设置宝塔面板优化 php 服务器性能</a>
<a rel="nofollow" href="https://www.centos.bz/2017/12/wordpress%E5%AE%9A%E6%9C%9F%E5%87%BA%E7%8E%B0%E5%BB%BA%E7%AB%8B%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%9E%E6%8E%A5%E6%97%B6%E5%87%BA%E9%94%99%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E5%86%B3/" target="_blank" rel="noopener noreferrer">WordPress定期出现“建立数据库连接时出错”问题的解决方案</a>
