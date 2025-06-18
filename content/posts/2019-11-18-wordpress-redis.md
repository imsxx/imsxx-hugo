---
title: 同一服务器下多站点使用WordPress该如何设置Redis缓存
author: 梦随乡兮
type: post
date: 2019-11-18T08:00:04+00:00
url: /wordpress-redis.html
featured_image: https://imsxx.com/wp-content/uploads/2019/11/c4d79289f8430ab.jpg
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
<div id="ez-toc-container" class="ez-toc-v2_0_73 counter-hierarchy ez-toc-counter ez-toc-transparent ez-toc-container-direction">
  <div class="ez-toc-title-container">
    <p class="ez-toc-title" style="cursor:inherit">
      本文目录
    </p>
    
    <span class="ez-toc-title-toggle"><a href="#" class="ez-toc-pull-right ez-toc-btn ez-toc-btn-xs ez-toc-btn-default ez-toc-toggle" aria-label="Toggle Table of Content"><span class="ez-toc-js-icon-con"><span class=""><span class="eztoc-hide" style="display:none;">Toggle</span><span class="ez-toc-icon-toggle-span"><svg style="fill: #999;color:#999" xmlns="http://www.w3.org/2000/svg" class="list-377408" width="20px" height="20px" viewBox="0 0 24 24" fill="none"><path d="M6 6H4v2h2V6zm14 0H8v2h12V6zM4 11h2v2H4v-2zm16 0H8v2h12v-2zM4 16h2v2H4v-2zm16 0H8v2h12v-2z" fill="currentColor"></path></svg><svg style="fill: #999;color:#999" class="arrow-unsorted-368013" xmlns="http://www.w3.org/2000/svg" width="10px" height="10px" viewBox="0 0 24 24" version="1.2" baseProfile="tiny"><path d="M18.2 9.3l-6.2-6.3-6.2 6.3c-.2.2-.3.4-.3.7s.1.5.3.7c.2.2.4.3.7.3h11c.3 0 .5-.1.7-.3.2-.2.3-.5.3-.7s-.1-.5-.3-.7zM5.8 14.7l6.2 6.3 6.2-6.3c.2-.2.3-.5.3-.7s-.1-.5-.3-.7c-.2-.2-.4-.3-.7-.3h-11c-.3 0-.5.1-.7.3-.2.2-.3.5-.3.7s.1.5.3.7z"/></svg></span></span></span></a></span>
  </div><nav>
  
  <ul class='ez-toc-list ez-toc-list-level-1 ' >
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-1" href="https://imsxx.com/wordpress-redis.html/#Redis%E6%98%AF%E4%BB%80%E4%B9%88" title="Redis是什么">Redis是什么</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-2" href="https://imsxx.com/wordpress-redis.html/#%E5%AE%89%E8%A3%85Redis" title="安装Redis">安装Redis</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-3" href="https://imsxx.com/wordpress-redis.html/#%E5%AE%89%E8%A3%85PHP_Redis%E6%89%A9%E5%B1%95" title="安装PHP Redis扩展">安装PHP Redis扩展</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-4" href="https://imsxx.com/wordpress-redis.html/#WordPress%E5%AE%89%E8%A3%85Redis%E6%8F%92%E4%BB%B6" title="WordPress安装Redis插件">WordPress安装Redis插件</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-5" href="https://imsxx.com/wordpress-redis.html/#%E8%AE%BE%E7%BD%AERedis%E5%A4%9A%E7%AB%99%E7%82%B9%E9%85%8D%E7%BD%AE" title="设置Redis多站点配置">设置Redis多站点配置</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-6" href="https://imsxx.com/wordpress-redis.html/#WordPress%E5%90%AF%E7%94%A8Redis%E7%BC%93%E5%AD%98" title="WordPress启用Redis缓存">WordPress启用Redis缓存</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-3'>
      <a class="ez-toc-link ez-toc-heading-7" href="https://imsxx.com/wordpress-redis.html/#%E7%BB%93%E6%9D%9F%E8%AF%AD" title="结束语">结束语</a>
    </li>
  </ul></nav>
</div>

### <span class="ez-toc-section" id="Redis%E6%98%AF%E4%BB%80%E4%B9%88"></span>Redis是什么<span class="ez-toc-section-end"></span>

* * *

<span class="bjh-p">WordPress采用的是动态数据库查询技术。通俗的说，就是用户访问每篇文章或页面，都会向数据库发送一条查询命令，数据库根据命令查询之后，反送查询结果（这个结果不考虑任何缓存技术）。显然，如果访问量大的时候，会出现频繁的查询。所以这会减慢网站速度。如果服务器性能不高，瞬间网站就崩溃了。</span>

<span class="bjh-p">所以需要一种技术，来减少数据库查询次数。而数据库缓存技术就是其中之一。Redis技术是其中的佼佼者。Redis是key-value分布式存储系统。简单的说，就是根据关键词值进行查询，这在很大程度上弥补了Memcached的短板。通过Redis进行数据库缓存，查询速度会更快，并发数更多。</span>

### <span class="ez-toc-section" id="%E5%AE%89%E8%A3%85Redis"></span>安装Redis<span class="ez-toc-section-end"></span>

* * *

在宝塔软件管理搜索“Redis”点击安装，开启首页展示

[<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-213" src="https://imsxx.com/wp-content/uploads/2019/11/ed20bc3c79b871c.jpg" alt="" width="795" height="292" />][1]

### <span class="ez-toc-section" id="%E5%AE%89%E8%A3%85PHP_Redis%E6%89%A9%E5%B1%95"></span>安装PHP Redis扩展<span class="ez-toc-section-end"></span>

* * *

找到你安装的PHP版本，选择安装扩展，安装Redis

[<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-214" src="https://imsxx.com/wp-content/uploads/2019/11/c6b1a47a288a50d.jpg" alt="" width="633" height="561" />][2]

### <span class="ez-toc-section" id="WordPress%E5%AE%89%E8%A3%85Redis%E6%8F%92%E4%BB%B6"></span>WordPress安装Redis插件<span class="ez-toc-section-end"></span>

* * *

进入WordPress管理后台，搜索插件**Redis Object Cache**并安装，先别着急启用。

[<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-215" src="https://imsxx.com/wp-content/uploads/2019/11/c4d79289f8430ab.jpg" alt="" width="576" height="405" />][3]

### <span class="ez-toc-section" id="%E8%AE%BE%E7%BD%AERedis%E5%A4%9A%E7%AB%99%E7%82%B9%E9%85%8D%E7%BD%AE"></span>设置Redis多站点配置<span class="ez-toc-section-end"></span>

* * *

如果你的服务器只有一个站点，这一步可有可无，但是为了保险起见，建议单站点也设置一下。

使用宝塔面板找到站点目录下的wp-config.php，点击编辑，在头部注释下方增加以下代码

[<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-216" src="https://imsxx.com/wp-content/uploads/2019/11/c431b5169b8d030.jpg" alt="" width="558" height="405" />][4]

`<span class="me0">define</span><span class="br0">(</span> <span class="st1">'WP_CACHE_KEY_SALT'</span><span class="">, </span><span class="st1">'你的网站域名'</span> <span class="br0">)</span><span class="">;</span>`

`<span class="me0">define</span><span class="br0">(</span> <span class="st1">'WP_REDIS_SELECTIVE_FLUSH'</span><span class="">, </span><span class="kw4">true</span> <span class="br0">)</span><span class="">;</span>`

第一行是给Redis缓存一个独特的前缀，否则多站点时容易混乱，建议改成你的网站域名，不用http前缀，比如我的是pandacui

第二行意义在于刷新Redis缓存时是否只刷新当前站点，false代表刷新全部站点，设置为true即可。

### <span class="ez-toc-section" id="WordPress%E5%90%AF%E7%94%A8Redis%E7%BC%93%E5%AD%98"></span>WordPress启用Redis缓存<span class="ez-toc-section-end"></span>

* * *

经过以上步骤，就可以在WordPress插件管理页面启用Redis缓存，然后多刷新几次你的站点，在宝塔Redis的负载状态中看到命中率就代表配置成功了

[<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-217" src="https://imsxx.com/wp-content/uploads/2019/11/d30ce47d8a550ac.jpg" alt="" width="612" height="528" />][5]

<div class="entry-content">
  <h3>
    <span class="ez-toc-section" id="%E7%BB%93%E6%9D%9F%E8%AF%AD"></span>结束语<span class="ez-toc-section-end"></span>
  </h3>
  
  <hr />
  
  <p>
    有的站点使用的是Memcached缓存，我觉得Redis比前者更强大一些，要注意的是，这两个缓存安装其一即可，否则可能引起问题。
  </p>
</div>

 [1]: https://imsxx.com/wp-content/uploads/2019/11/ed20bc3c79b871c.jpg
 [2]: https://imsxx.com/wp-content/uploads/2019/11/c6b1a47a288a50d.jpg
 [3]: https://imsxx.com/wp-content/uploads/2019/11/c4d79289f8430ab.jpg
 [4]: https://imsxx.com/wp-content/uploads/2019/11/c431b5169b8d030.jpg
 [5]: https://imsxx.com/wp-content/uploads/2019/11/d30ce47d8a550ac.jpg

