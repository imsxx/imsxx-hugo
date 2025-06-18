---
title: WordPress点击发布文章时“无限加载”解决办法
author: 梦随乡兮
type: post
date: 2022-12-16T17:02:37+00:00
url: /wordpress-post-loading.html
featured_image: https://r2.imsxx.com/wp-content/uploads/17d1bcd4325753d.jpg
views:
  - 670
suxing_ding:
  - 1
like:
  - 1
categories:
  - 笔记
tags:
  - post
  - wordpress
  - 邮件

slug: "wordpress-post-loading"
---
在服务器未做大调试的情况下，优先考虑插件和自写代码的问题。

在关闭所有插件后，按个重启插件，每重启一个插件就试试文章发布是否正常，直到重启Easy WP SMTP这个邮件插件时，重启后文章点击发布就开始无限加载，加载超时后会白屏报错。

F12看了一下post.php传了0，虽然显示无线加载，但实际上文章已经发布出去了。

于是搭了个新环境重测Easy WP SMTP插件，发现没异常，那应该是我自己添加的代码导致。

翻了很久找到之前有给邮件写过美化代码。

Ps：WordPress自带的邮件通知功能很简陋，为此才会做这个美化。

而这个美化代码是挂靠在邮件通知插件里，邮件通知插件又会在发布文章时被触发，由于代码写得渣导致每次调用都会拖垮post.php进程。

解决办法就是要么删掉代码，要么等空了优化。

不过总算找到问题所在了，还是有收获。

