---
title: 'debian12提示-bash: curl: command not found解决办法'
author: 梦随乡兮
date: 2024-02-29 02:50:01+00:00
slug: bash-curl-command-not-found
categories: ["建站"]
tags:
- bash
- curl
- command
- debian
---
<img width="1280" height="672" src="https://r2.imsxx.com/wp-content/uploads/20240229024911370002.jpg" alt="" />
有些VPS的debian默认未安装sudo，导致我们在使用curl命令的时候提示`-bash: curl: command not found`，解决办法如下：
先安装sudo：
`apt-get install sudo`
再安装curl：
`sudo apt install curl`
然后再安装诸如1panel或宝塔面板时就可以正常使用curl命令了。
