---
title: 1panel开启WordPress的redis缓存流程 流程优化版
author: 梦随乡兮
date: 2024-04-17 04:39:26+00:00
slug: 1panel-wordpress-redis
tags:
- 1panel
- wordpress
- redis
---
之前在网上搜了一些教程，发现已经有人做过了，但中间有一些细节写错，这里自己写一版。
首先，开启redis需要现在1panel面板里搜索安装redis组件。
<img src="https://r2.imsxx.com/wp-content/uploads/078cd3e954e01e6.png" />
安装完成后打开运行环境，编辑当前wordpress在用的PHP版本，在扩展里添加redis，最后点确认。会自动重建应用。
<img src="https://r2.imsxx.com/wp-content/uploads/f38e3d966560daf.png" />
然后打开wordpress后台，在插件市场里搜索安装“Redis Object Cache”，启用后会看到已经检测到服务器支持redis写入，但redis不可访问。这时候回到1panel面板，打开网站的根目录->wp-config.php这个文件。添加如下代码：
<div>
<pre>define('WP_REDIS_HOST', 'redis');
define('WP_REDIS_PORT', '6379');
define('WP_REDIS_DATABASE', '0');
define('WP_REDIS_PASSWORD', '此处替换成你的redis密码');```
<img src="https://r2.imsxx.com/wp-content/uploads/e9f5b5730c3c17d.png" />
redis的密码在数据库-Redis-连接信息里查看。
<img src="https://r2.imsxx.com/wp-content/uploads/dcc5d6ee3ff29db.png" />
注意只需要改成你自己的密码就可以了，代码里的其他内容不要动。改完保存，然后回到wordpress后台刷新插件页面会发现已经redis已经可以访问了。
这时候开启对象缓存，大概率你会收到一个报错，这个报错是因为object-cache.php这个文件配置的问题。如果你没乱改存放，它应该是在根目录/wp-content/object-cache.php。
打开它，搜索“protected function build_parameters”可以找到下面这段代码：
<img src="https://r2.imsxx.com/wp-content/uploads/c5da63dc6f423e4.png" />
host里原本写的redis（也可能写的127.0.0.1），改成你Redis连接信息里的容器连接地址。
然后加一个密码的字段，字段填写Redis连接信息里的容器密码。
<div>
<pre>'password' => '填写你的redis密码',```
最后保存。
刷新wordpress后台发现报错已经没了，来到wordpress的redis插件，启用对象存储，大功告成。
<img src="https://r2.imsxx.com/wp-content/uploads/97c27bf1dd6fff5.png" />
