---
title: 使用cloudflare对新老域名进行URL转发
author: 梦随乡兮
type: post
date: 2022-11-06T14:33:46+00:00
featured_image: https://r2.imsxx.com/wp-content/uploads/9d840e3d45a82a0.png
views:
- 1943
categories:
- 笔记
tags:
- cloudflare
- URL转发
slug: "cloudflare-url-zhuanfa"
---
之前写过《<a title="网站利用cloudflare SaaS实现分流加速国外访问-梦随乡兮" href="https://imsxx.com/cloudflare-saas.html" target="_blank" rel="noopener">网站利用cloudflare SaaS实现分流加速国外访问</a>》，里面我提到了老域名需要跳转到新域名去。
首先明确一下，国内域名即便是备案了也不能做URL转发，因为根据备案要求，这里就记录一下转发过程。
管局的要求是你域名打开后备案号要对得上，而URL转发的逻辑是访问域名A实际打开时域名B，域名B肯定不会对得上A的备案号。备案服务商抽查到就会要求整改。
简单的做法是给域名A做一个单页，让用户手动去单页上点击跳转，单页里你可以介绍“本站使用了新域名”之类的文字，要留下域名A的备案号。这样做服务商是认可的。
更简单的做法是把域名迁移到大陆外的域名服务商，在他们那进行URL转发。
> 为什么一定要迁出？
>
> 因为大陆服务商对域名解析的基础要求就是备案，不只是域名解析到大陆服务器需要备案，进行URL转发也需要备案。因此需要转出，而我境外业务主要使用的是cloudflare，就转进了cloudflare。
* * *
如何从国内转出域名就不写了，域名管理页面有步骤，这里从解析开始记录。
首先进入需要转发的域名页面。
<img src="https://r2.imsxx.com/wp-content/uploads/07ded96df5c4827.png" alt="" width="1827" height="847" />
打开左侧栏的规则→页面规则，点击“创建页面规则”：
<img src="https://r2.imsxx.com/wp-content/uploads/9d840e3d45a82a0.png" alt="" width="854" height="561" />
* 【URL】即你要用来转发的域名，你可以设置全域名转发*ygodl.com/*中间域名换成你自己的。也可以*ygodl.com/1.html*来指定某个路径特定页面来转发。
* 【选取设置】选择“转发URL”
* 【状态代码】这里主要是给搜索引擎用的。301表示永久，即搜索引擎收录了你的老域名被人打开后跳转到新域名，301状态就让搜索引擎知道你换域名了，它就会逐步把域名都替换成你最新的。而302临时状态，意味着你只是暂时换了域名，搜索引擎不会对已收录的URL进行调整替换。
* 【目标URL】你最终需要展示给用户的新网站or新地址。
设置好上面的内容后转发实际上就已经生效了，如果你到这步没生效，那么就再做下面的设置。
<img src="https://r2.imsxx.com/wp-content/uploads/d167a8b18ac5e7f.png" alt="" width="1050" height="319" />
来到域名解析处，添加A记录：记录值@、IP随便写都行，然后保存。
完成了。
