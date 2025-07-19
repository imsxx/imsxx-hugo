---
title: （待填坑）搭建在海外的WordPress网站如何做好国内访问
author: 梦随乡兮

date: 2021-09-02T08:13:48+00:00

slug: "wordpress-cdn-cn"
---
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
文章背景
由于服务器带宽等成本原因，导致原本面向国内访客的网站，不得不搭建在国外服务器上。那么怎么优化访问速度呢？这篇文章就分享记录一下我这些踩过的坑，希望你能有所收货。
## 服务器的选择 {.wp-block-heading}
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
线路
网站搭建在海外，但访客绝大多数又在国内。那服务器的选择就变得非常重要。
这里与其说是选服务器，不如说是在选服务器的线路。目前公认比较可靠的裸连三网裸连线路是走CN2 GIA，考虑性价比的话，这里推荐一下搬瓦工。
CN2 GIA线路仅限于裸连哈，如果套了奇奇怪怪的CDN加速服务，CN2的优势就没了。
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
配置
目前我的多个跑着WordPress配置如下
<div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-9d6595d7 wp-block-columns-is-layout-flex">
<div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow">
<div class="wp-block-pandastudio-list color-error">
<div class="pf-panel-title">
决斗链接中文网
<div class="pf-panel-content">
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
CPU 4核
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
内存 8G
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
硬盘 160G SSD
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
流量 4T/月 (G口)
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
IDC vultr 美国洛杉矶 普通线路
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
系统 CentOS SELinux 8 x64
<div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow">
<div class="wp-block-pandastudio-list color-info">
<div class="pf-panel-title">
本站(博客)
<div class="pf-panel-content">
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
CPU 2核
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
内存 4G
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
硬盘 60G SSD
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
流量 1T/月 (6Mbps)
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
IDC 腾讯轻量云 成都地区
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
系统 CentOS 8 x64
如果只是挂个人博客，配置可以再往下降。但再往下降能节约钱的也很少，并且配置过低，用来跑如今的WordPress还是会比较吃力。所以建议上2h4g的配置，这是国内外做网站的服务器中热销配置。
另外带宽方面，国外服务器不用过多考虑。国内服务器的话，推荐我博客上面的配置，差不多够用了。(如果你正在访问我的网站，发现速度慢下来了，那就提升一个档的配置)
## WordPress {.wp-block-heading}
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
配置
WP对服务器的要求不是很高，甚至连虚拟机都可以搭建。但考虑到网站尽可能的流畅和拓展性，建议使用
<div class="wp-block-pandastudio-list color-success">
<div class="pf-panel-title">
WordPress推荐配置
<div class="pf-panel-content">
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
Nginx 1.17.10
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
MySQL 5.7.32
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
PHP 7.3
<div class="wp-block-pandastudio-list-item color-white">
<div class="list-content">
面板 宝塔(bt)
面板提供了一键编译安装上面的环境，编译完成后参考下面这篇文章做一些基础小优化。
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
主题推荐
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
本地缓存优化
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
本地图片优化
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
本地广告优化
## CDN {.wp-block-heading}
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
cloudflare
<div class="wp-block-pandastudio-title">
<div class="title_style_01">
<p>
自选IP
