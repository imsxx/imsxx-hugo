
---
title: 小服务器生存法则（二）：MySQL与OpenResty的精准调校
date: 2025-07-27T16:00:00+08:00
draft: false
author: 梦随乡兮
slug: "vps-mysql-openresty-tuning"
tags: 
- 1Panel
- Docker
- MySQL
- OpenResty
- 性能优化
- VPS
categories: ["建站"]
---

大家好，我是梦随乡兮。在上一篇[《小服务器生存法则（一）：榨干性能，从PHP-FPM优化开始》](https://imsxx.com/vps-php-fpm/)中，我通过将PHP-FPM的运行模式调整为`ondemand`，成功为我的2核4G小服务器降低了闲时内存占用。在解决了PHP这个“内存大户”后，本次我们的目标将转向另外两个核心服务：**MySQL数据库**和作为Web服务网关的**OpenResty**。

本篇笔记将详细记录我如何借助专业分析工具，对这两个服务进行一次数据驱动的、精准的性能调优，完成我整个服务器优化之旅的最后一块拼图。

## 一、MySQL的“智能体检”与调优

盲目地修改MySQL配置是危险且低效的。为了做到“有的放矢”，我决定使用业界著名的开源脚本`MySQLTuner`来为我的数据库做一次全面的“智能体检”。

### 挑战：如何给容器里的MySQL“看病”？

我的第一个挑战不期而至。当我像往常一样，在服务器的主机终端里运行`perl mysqltuner.pl`时，脚本直接报错退出，提示找不到`mysqladmin`等命令行工具。

这正是我在第一篇[Docker探索笔记](https://imsxx.com/2025-07-22-1panel-docker-wordpress/)中学到的核心知识点——**容器隔离性**的体现。MySQLTuner脚本在主机环境（“门外”）运行，而它需要的所有工具都和MySQL服务本身一起，被封装在独立的容器环境（“屋里”）。

解决方案是：**把“医生”请进“屋里”**。

1.  **找到MySQL容器**：在主机终端执行`docker ps`命令，可以列出所有正在运行的容器。我从中找到了我的MySQL容器的名字，形如`1Panel-mysql-nA60`。
2.  **进入容器内部**：接着，通过`docker exec -it 1Panel-mysql-nA60 /bin/bash`命令，我成功地进入了MySQL容器内部的命令行。
3.  **在容器内安装依赖**：我发现这是一个极其精简的容器镜像，连`apt-get`或`yum`这些常见的包管理器都没有。经过几次尝试，我最终找到了它内置的轻量级包管理器`microdnf`。通过执行`microdnf install -y wget perl`，我成功地为这个“纯净”的容器环境安装了运行MySQLTuner所必需的两个工具。

### MySQLTuner的诊断报告与“药方”

在容器内部成功运行`perl mysqltuner.pl`后，我得到了一份详细的“体检报告”。报告的整体评价非常健康，这得益于MySQL 8.4.5版本自身已经相当智能。但在报告最末尾的`[Recommendations]`部分，它依然给出了两条极具价值的建议：

> Variables to adjust:
>
> *   `innodb_redo_log_capacity` should be (=32M) if possible, so InnoDB Redo log Capacity equals 25% of buffer pool size.
> *   `innodb_log_buffer_size` (> 64M)

这两条建议都指向了InnoDB存储引擎的日志系统，这是提升数据库写入性能和稳定性的关键。

*   **关于`innodb_redo_log_capacity`**：报告指出我的重做日志容量（100M）相对于缓冲池（128M）的比例过高，建议调整为缓冲池的25%，即32M。这有助于在保证数据安全的前提下，平衡恢复时间和写入性能。
*   **关于`innodb_log_buffer_size`**：报告建议增大日志缓冲区。这是一个在日志写入磁盘前的内存缓冲区，增大它可以有效减少磁盘I/O。考虑到我服务器内存有限，我没有直接采纳`>64M`的建议，而是选择了一个更为保守但已足够优化的值`16M`。

### “对症下药”：修改配置并重建

拿到了清晰的“药方”，我开始“对症下药”。

1.  在1Panel的文件管理器中，我找到了MySQL的配置文件：`/opt/1panel/apps/mysql/mysql/conf/my.cnf`。
2.  编辑该文件，在`[mysqld]`区块下，添加了以下两行配置：
    ```ini
    [mysqld]
    # ... 原有配置 ...
    
    # --- 新增的性能优化配置 ---
    innodb_redo_log_capacity = 32M
    innodb_log_buffer_size = 16M
    ```
3.  保存文件后，回到1Panel的应用列表，对**MySQL应用**执行了一次“**重建 (Rebuild)**”操作。当MySQL重建完成，针对数据库的优化便正式生效了。

## 二、OpenResty (Nginx)的“健康检查”

优化完数据库后，我将目光投向了Web服务的总入口——OpenResty。我需要确认它的全局配置是否与我这台小服务器的硬件规格相匹配。

在1Panel后台，我找到了OpenResty的全局配置，其对应的文件路径为`/opt/1panel/apps/openresty/openresty/conf/nginx.conf`。

经过检查，我发现1Panel的默认配置已经相当出色：
*   `worker_processes auto;`：这是最完美的设置，它会自动根据服务器的CPU核心数（我的机器是2核）来启动相应数量的工作进程。
*   `worker_connections 1024;`：每个工作进程能处理1024个连接，总并发处理能力达到2048，对于我的网站规模来说绰绰有余。

唯一可以“锦上添花”的地方，是`gzip_types`指令。默认配置已经包含了大部分文本文件，但我决定将其扩展，以支持JSON、RSS订阅源和尤其重要的SVG矢量图（其本质是XML文本，压缩效果显著）。

我将`gzip_types`这一行修改为：
```nginx
gzip_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss image/svg+xml;
```
修改并保存后，对**OpenResty应用**执行了一次“**重启**”，使Gzip压缩策略覆盖得更为全面。

## 总结

至此，我这台2核4G的小服务器，已经经历了一次从应用层到服务层的全链路优化。

1.  **PHP-FPM**的`ondemand`模式，极大地降低了闲时内存占用，为服务器“开源”。
2.  **MySQL**的日志系统调优，提升了数据库的写入效率和稳定性，为数据处理“节流”。
3.  **OpenResty**的配置检查与微调，确保了Web服务网关的高效运行。

整个过程不仅让服务器运行得更加健康、高效，更重要的是，它加深了我对现代化、容器化服务器架构的理解。从最初对Docker的一知半解，到现在能够熟练地通过`docker exec`进入容器内部解决问题，这本身就是比性能参数提升更有价值的收获。

希望我的这份系列笔记，能为同样在小服务器上探索的朋友们提供一些有用的参考。

---
*笔记由Gemini 2.5pro构建*
