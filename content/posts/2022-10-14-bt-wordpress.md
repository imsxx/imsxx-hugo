---
title: 使用宝塔面板搭建WordPress的PHP、MySQL等全套优化
author: 梦随乡兮
type: post
date: 2022-10-14T13:57:31+00:00
featured_image: https://r2.imsxx.com/wp-content/uploads/314821.jpg
views:
- 1862
like:
- 1
categories:
- 笔记
tags:
- mysql
- php
- wordpress
- 宝塔面板
slug: "bt-wordpress"
---
本文并非“使用宝塔面板如何搭建WordPress”而是<strong>“用宝塔面板搭建WordPress后如何优化”</strong>。
<nav>
</li>
</ul></nav>
## 运行配置介绍
最新的WordPress6.0中，官方最低配置要求
* PHP 7.4+
* MySQL 5.0+
* CPU 1GHz+
* 内存 512MB+
* 支持HTTPS
至于带宽没有特别要求，能访问就行。
本文中我展示的配置是：
* PHP 7.4
* MySQL 5.7
* CPU 4核
* 内存 8G
* * *
安装WordPress完成后，在面板左侧栏→软件商店，选择“已安装”，如下图：
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014215645.png" alt="" width="740" height="741" />
## 挨个介绍
### Nginx
这是运行环境，相比Apache而言，Nginx效率更高，占用更少。
Nginx的版本没有特别要求，在首次安装宝塔时会推荐安装某个版本，直接默认的就行。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014220314.png" alt="" width="654" height="608" />
Nginx的优化项并不多，调整它对WordPress搭建的网站在性能上的提升并不大，保持默认设置就行。
* * *
### MySQL
这是数据库。在服务器内存小于4G时，没法安装类似5.7的高版本，不过由于WordPress支持5.0+版本，所以也并非必须装高版本。当然，更高的版本自然意味着更好的易用性，但同时也会占用更多内存。
在下面这张图中，我们可以看到“当前状态”，名词和各种缓存原理就不细写了。每一个命中率都对应在“性能调整”中有相应设置。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014221906.png" alt="" width="1308" height="611" />
**在‘性能调整’页的顶部有‘优化方案’，对应你的服务器内存大小进行选择即可。**
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014222108.png" alt="" width="377" height="154" />
当然，这个一键式的优化方案，可能并不适用你的的建站情况，所以在各项值上也可以进行一些手动微调。<strong>以下所有调整都需要保存后重启数据库进行观察，如果不满足继续加。</strong>
* <strong>活动峰值连接数</strong>：这个值不大于max_connections即可，非常接近或者满了，就加max_connections，每次加50。
* <strong>线程缓存命中率</strong>：这个百分比不要小于90%，小于就加thread_cache_size，每次加8。
* <strong>索引命中率</strong>：这是给MyISAM引擎用的，小于95%就加key_buffer_size，每次64。
* <strong>Innodb索引命中率</strong>：这是给Innodb引擎用的，小于95%就加innodb_buffer_pool_size，每次64。
* <strong>查询缓存命中率</strong>：如果服务器或WordPress使用了redis、memcached进行缓存，那这项对应的query_cache_size可以设置成0。反之就使用默认配置即可。PS：在MySQL后续版本中已经放弃了这条，所以它未来也变得没那么重要。
* **创建临时表到磁盘：**WordPress不用太注意这个，因为WP本身就优化过。该值在45%左右即可，控制它的是tmp_cache_size，适当增减32。维持在45%或50%都行。
**已打开的表、****没有使用索引的量、没有使用索引的JOIN量、排序后的合并次数、锁表次数，这几项都是大数据量查询读写才会出现涉及到，这里就略过吧。**
* * *
### PHP
在最新的WordPress6.0中，官方已经推荐大家使用7.4版本了，服务器配置还不错的话，咱们也就直接听官方的用7.4。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014223940.png" alt="" width="654" height="607" />
在设置里，<strong>“安装扩展”</strong>这块，只需要安装 <strong>opcache</strong> 和 <strong>Memcached</strong> ，其他的扩展都可以忽略掉。当然，安装redis扩展也行(后面会写原因)。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014224220.png" alt="" width="656" height="609" />
在<strong>“配置修改”</strong>中，绝大多数设置都保持默认即可。
* <strong>max_execution_time</strong>：页面执行时间，页面上的任何读写都属于执行，超过设置的时间就会被系统中断，它旨在最大程度地减少服务器滥用。这个值一般设置成60或90即可。太少，会导致用户的一些操作被系统中断。太长，一些插件线程会长期占用。另外，恶意攻击也会因为你设置的值过大而撑爆你的服务器性能，导致网站瘫痪。我这里为了演示设置成600秒，实际我个人在使用90。
* **max_input_time**：最大输入时间设置允许脚本解析输入数据（如 POST 和 GET）的最大时间（秒）。计时从 PHP 在服务器上调用的那一刻开始。这个设置影响我们上传大型文件，因为越大的文件上传时间就越长，超时就会被系统中断。如果你的网站没有视频等大文件上传，这个值可以设置60或更低。
* **memory_limit**：限制单个脚本能分配到的最大内存。不超过512M即可，比较主流的设置是256M。这个值太大，一些脚本就会因为高频滥用拖慢服务器。
* **post_max_size**：指通过表单POST给PHP的所能接收的最大值，包括表单里的所有值。设置成256就已经很够了。注意，此处的设置要比下方upload_max_filesize大。
* <strong>upload_max_filesize</strong>：允许上传的单个文件最大限制。如果你的网站不传视频、软件、游戏等大容量内容。那么可以将它设置为5M，如果要上传超清照片，可以设置为20M。
* <strong>default_socket_timeout</strong>：socket流的超时参数，即socket流从建立到传输再到关闭整个过程必须要在这个参数设置的时间以内完成，如果不能完成，那么PHP将自动结束这个socket并返回一个警告。类似的一个PHP配置是connection_timeout，不过connection_timeout是指保持连接的时间超时，不包括创建和销毁连接。设置为60够用了。
其他上面没写出的设置对WordPress整体影响不大，都保持默认状态即可。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014233532.png" alt="" width="656" height="608" />
在<strong>“性能调整”</strong>中，对应自己的服务器内存，来选择宝塔已经预设好的设置就行了。
关于运行模式中的「动态、静态、按需」，选动态就好了，千万不要乱改。
* * *
### liuux工具箱
主要用它来为服务器开启虚拟内存(Swap)。虚拟内存可以一定程度上提升服务器性能。Swap虚拟内存，在十几年服务器配置都比较拉胯的时代非常有用。
因为虚拟内存虽然在极端情况下能帮我缓解物理内存压力，但实际上当物理内存占用非常高时，这时候线程都已经自动拉满了，但同时虚拟内存也开始帮你‘分忧’了。
结果就是原本100线程花10秒处理完的东西，非得因为swap的加入分来一些线程，导致预期内能处理完的程序反而需要更长时间。
这其中还有一个问题，因为虚拟内存实际上的表现非常一般，它的性能肯定比不了物理内存。
但如今建站服务器内存最次也有1G~2G，因此虚拟内存可以设置帮我们在突发状况下应急，但不建议过大。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221014235502.png" alt="" width="704" height="288" />
* * *
### Nginx免费防火墙
免费版防火墙，功能上自然不丰富。主要是用来做一些简单的拦截。
<img src="https://r2.imsxx.com/wp-content/uploads/2022/10/QQ截图20221015000322.png" alt="" width="690" height="520" />
* * *
### 日志清理工具
站点没什么流量可以不用装，流量较大可以一个季度或半年清理一次，给服务器腾出空间。
* * *
### 宝塔SSH终端
这是宝塔默认安装的应用，没什么功能可言。
推荐使用Xshell客户端，在其官网可以获取免费版。
* * *
### Pure-Ftpd
这是以前古早时期用来给服务器传文件用的工具。宝塔面板会默认选择安装，如果你不知道是干什么的，可以不管它或者卸载它。
* * *
### phpMyAdmin
在线管理数据库的工具，留着以备不时之需。
* * *
### Memcached
高性能的分布式内存对象缓存系统。也就是上面PHP介绍里安装的Memcached扩展管理面板，所有设置都默认即可。
* * *
好了，差不多就介绍完了。
