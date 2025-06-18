---
title: 禁用笔记本自带键盘教程，百度出来没一个靠谱的。
author: 梦随乡兮
type: post
date: 2019-08-22T15:46:44+00:00
url: /bijibenjianpan.html
featured_image: https://imsxx.com/wp-content/uploads/2019/08/17e5e54d74ceb0.png
zrz_credit_add:
  - 1
views:
  - 1049
like:
  - 1
b2_post_reading_role:
  - none
b2_vote:
  - 'a:2:{s:2:"up";i:0;s:4:"down";i:0;}'
categories:
  - 笔记
tags:
  - win10
  - 禁用
  - 笔记本
  - 键盘

slug: "bijibenjianpan"
---
笔记本在上个月进了雨水，虽然抢救回来勉强能用了，但是自带键盘却坏了。由于是2014年的老本子，搜索了一圈也没找到键盘，索性只能外接一个将它禁用。

之所以禁用它是因为外键键盘会时不时的出现奇怪的输入严重影响打字体验。

首先，百度出来的第一个通过设备管理器换驱动的方法禁用键盘并不好用，至少在win10上这么做就直接导致了蓝屏。

## 下面直接上我亲测能用的方法：

首先以管理员权限运行cmd

*方法：点开开始菜单，直接输入cmd会出现命令提示符，右键它选择以管理员身份运行<figure id="117" class="content-img-box">

<img decoding="async" id="B8C5A2AA" class="po-img-big" src="https://imsxx.com/wp-content/uploads/2019/08/17e5e54d74ceb0.png" alt="禁用笔记本自带键盘教程，百度出来没一个靠谱的。" /> <figcaption class="addDesn"></figcaption></figure> 

接下来将下面这段代码粘贴进去后回车，会收到成功提示：

<pre class="ql-syntax" spellcheck="false"><span class="hljs-attribute">sc</span> config i8042prt start=disabled
</pre><figure id="118" class="content-img-box">

<img decoding="async" id="D14AD4C5" class="po-img-big" src="https://imsxx.com/wp-content/uploads/2019/08/198edb95853ae1.png" alt="禁用笔记本自带键盘教程，百度出来没一个靠谱的。" /> <figcaption class="addDesn"></figcaption></figure> 

然后重启电脑，就搞定了。

## 恢复自带键盘功能

优先尝试下面这段代码：

<pre class="ql-syntax" spellcheck="false">sc config i8042prt <span class="hljs-keyword">start</span>=<span class="hljs-keyword">auto</span>
</pre>

不可用再尝试下面的

<pre class="ql-syntax" spellcheck="false">sc config i8042prt <span class="hljs-keyword">start</span>=<span class="hljs-keyword">demand</span>
</pre>

完事重启后就恢复了。
