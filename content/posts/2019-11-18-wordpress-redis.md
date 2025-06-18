---
title: 同一服务器下多站点使用WordPress该如何设置Redis缓存
author: 梦随乡兮
type: post
date: 2019-11-18T08:00:04+00:00
featured_image: https://r2.imsxx.com/wp-content/uploads/2019/11/c4d79289f8430ab.jpg
fromname_value:
- 熊猫博客
fromurl_value:
- https://www.pandacui.com/231.html
views:
- 2407
categories:
- 笔记
tags:
- Redis
- wordpress
- 宝塔
- 建站
slug: "wordpress-redis"
---
<nav>
</nav>
### Redis是什么
* * *
WordPress采用的是动态数据库查询技术。通俗的说，就是用户访问每篇文章或页面，都会向数据库发送一条查询命令，数据库根据命令查询之后，反送查询结果（这个结果不考虑任何缓存技术）。显然，如果访问量大的时候，会出现频繁的查询。所以这会减慢网站速度。如果服务器性能不高，瞬间网站就崩溃了。
所以需要一种技术，来减少数据库查询次数。而数据库缓存技术就是其中之一。Redis技术是其中的佼佼者。Redis是key-value分布式存储系统。简单的说，就是根据关键词值进行查询，这在很大程度上弥补了Memcached的短板。通过Redis进行数据库缓存，查询速度会更快，并发数更多。
### 安装Redis
* * *
在宝塔软件管理搜索“Redis”点击安装，开启首页展示
### 安装PHP Redis扩展
* * *
找到你安装的PHP版本，选择安装扩展，安装Redis
### WordPress安装Redis插件
* * *
进入WordPress管理后台，搜索插件**Redis Object Cache**并安装，先别着急启用。
### 设置Redis多站点配置
* * *
如果你的服务器只有一个站点，这一步可有可无，但是为了保险起见，建议单站点也设置一下。
使用宝塔面板找到站点目录下的wp-config.php，点击编辑，在头部注释下方增加以下代码
`define( 'WP_CACHE_KEY_SALT', '你的网站域名' );`
`define( 'WP_REDIS_SELECTIVE_FLUSH', true );`
第一行是给Redis缓存一个独特的前缀，否则多站点时容易混乱，建议改成你的网站域名，不用http前缀，比如我的是pandacui
第二行意义在于刷新Redis缓存时是否只刷新当前站点，false代表刷新全部站点，设置为true即可。
### WordPress启用Redis缓存
* * *
经过以上步骤，就可以在WordPress插件管理页面启用Redis缓存，然后多刷新几次你的站点，在宝塔Redis的负载状态中看到命中率就代表配置成功了
<div class="entry-content">
<h3>
结束语
</h3>
<hr />
<p>
有的站点使用的是Memcached缓存，我觉得Redis比前者更强大一些，要注意的是，这两个缓存安装其一即可，否则可能引起问题。
: https://r2.imsxx.com/wp-content/uploads/2019/11/ed20bc3c79b871c.jpg
: https://r2.imsxx.com/wp-content/uploads/2019/11/c6b1a47a288a50d.jpg
: https://r2.imsxx.com/wp-content/uploads/2019/11/c4d79289f8430ab.jpg
: https://r2.imsxx.com/wp-content/uploads/2019/11/c431b5169b8d030.jpg
: https://r2.imsxx.com/wp-content/uploads/2019/11/d30ce47d8a550ac.jpg
