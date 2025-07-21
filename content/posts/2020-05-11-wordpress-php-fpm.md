---
title: WordPress因php-fpm导致的服务器CPU占用爆满
author: 梦随乡兮
date: 2020-05-11 09:21:24+00:00
slug: wordpress-php-fpm
tags:
- wordpress
- php
- fpm
- CPU
---
上图是解决占用之后的进程，之前2核CPU是占满的。
这次主要是因为某个插件自带了文章标签内链功能，原理就不讲了反正我也不懂，从后台关闭这个插件后占用逐渐恢复正常水平。
进不去网站的时候，从服务器进去，到这个路径/www/wwwroot/imsxx.com/wp-content/plugins，把相关的插件文件夹重命名一下，WordPress就跑不通这个插件了，也就是变相停止了。等网站恢复正常后，要么把该插件不必要的功能关掉，要么就直接卸载掉该插件。
: https://r2.imsxx.com/wp-content/uploads/2020/05/52ab9ef9f1af91c.jpg
