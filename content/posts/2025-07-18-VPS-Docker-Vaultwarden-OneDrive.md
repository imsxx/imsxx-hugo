---
title: VPS + Docker + Vaultwarden 自动化备份至 OneDrive 超详细图文指南（含所有踩坑点及解决方案）
author: 梦随乡兮
date: 2025-07-18T00:00:00+00:00
slug: "VPS-Docker-Vaultwarden-OneDrive"
categories: ["笔记"]
tags: 
- VPS
- Docker
- Vaultwarden
- OneDrive
---

## 前言

在 VPS 上用 Docker 搭建 Vaultwarden 后，数据安全一直是我最关心的问题，虽然谷歌浏览器的密码器它是明文存储，但好歹它不会遗失，而自建密码器就得考虑备份问题了。

本教程将手把手地指导你完成一整套“设置好就忘掉它”的备份方案：每天自动将 Vaultwarden 的数据打包，并安全地上传到你的 Microsoft OneDrive 网盘。我们将直接采用最稳定、最高效的方法，让你一次性配置成功。

这篇文章是我从零开始的完整实战记录，它不仅包含了成功的步骤，更详尽地剖析了我遇到的**每一个坑**——从环境配置、脚本权限到 `cron` 定时任务的各种疑难杂症——以及最终被验证有效的**终极解决方案**。如果你也想为你的重要数据上一道保险，这篇文章将是你的最佳导航。

## 我的环境与目标

* **服务器**: Google Cloud VPS (Debian / Ubuntu 系统)
* **服务**: Vaultwarden (通过 Docker 部署)
* **备份目标**: Microsoft OneDrive
* **最终目标**: 每日定时、全自动、异地备份。

### 第一步：安装与配置 Rclone（连接 VPS 与 OneDrive 的桥梁）

**1. 安装 Rclone**

```bash
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```

> **⚠️ 踩坑点 #1：解压工具缺失**
> 
> **遭遇**：脚本报错 `unzip` 工具未找到。
> **分析**：纯净的 VPS 系统缺少基础解压工具。
> **解决**：先安装 `unzip`：`sudo apt-get update && sudo apt-get install unzip -y`，然后重新运行安装脚本。

**2. 配置 Rclone**
运行 `rclone config`，根据提示开始配置。

* **新建连接**：选 `n) New remote`，命名为 `onedrive`。
* **选择云盘类型**：选择 `Microsoft OneDrive`。
* **客户端 ID 和密钥**：全部直接回车，留空。
* **区域**：直接回车，选择 `global`。
* **高级配置**：选 `n` (No)。
* **自动配置**：选 `n` (No)，这是在无浏览器 VPS 上的关键！

> **⚠️ 踩坑点 #2：如何在无浏览器的服务器上授权？**
> 
> **遭遇**：选择了 `n` 之后，终端提示我需要一个 `config_token`。
> **分析**：这是 Rclone 的远程授权机制，需要在有浏览器的电脑上生成授权令牌。
> **解决**：
> 
> 1. 在**自己的个人电脑**上同样安装 Rclone。
> 2. 在个人电脑的命令行中运行 `rclone authorize "onedrive"`。
> 3. 浏览器会自动弹出并引导你登录微软账户、授权。
> 4. 授权成功后，回到个人电脑的命令行窗口，复制那一整大串 `{...}` 的 JSON 文本。
> 5. 将这串文本完整地粘贴回**VPS 的终端**里 `config_token>` 提示符之后，按回车。

之后一路确认，选择你的个人 OneDrive，即可完成配置。

### 第二步：编写一个稳定可靠的备份脚本

**1. 找到 Vaultwarden 数据目录**

> **⚠️ 踩坑点 #3：数据目录路径不确定**
> 
> **分析**：备份脚本需要知道 Docker 容器映射到 VPS 上的真实数据路径。
> **解决**：运行 `sudo docker inspect vaultwarden`，在输出中找到 `"Mounts"` 部分，里面的 `"Source"` 对应的路径就是我们需要的。在我的例子中是 `"/vw-data"`。

**2. 最终版 `backup.sh` 脚本**
创建 `nano backup.sh` 文件，将以下经过千锤百炼的最终代码完整粘贴进去：

```bash
#!/bin/bash

# 任何命令失败则立即退出
set -e

# --- 开始配置 ---
CONTAINER_NAME="vaultwarden"
VAULTWARDEN_DATA_DIR="/vw-data"
BACKUP_DIR="/home/imsxx_com/vaultwarden_backups"
RCLONE_REMOTE_NAME="onedrive"
ONEDRIVE_BACKUP_DIR="VaultwardenBackups"
RCLONE_CONFIG_PATH="/home/imsxx_com/.config/rclone/rclone.conf"
# --- 结束配置 ---

echo "备份流程开始于: $(date +"%Y-%m-%d %H:%M:%S")"

mkdir -p "$BACKUP_DIR"

BACKUP_FILE="vaultwarden-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
BACKUP_FILE_PATH="$BACKUP_DIR/$BACKUP_FILE"

echo "准备停止 Vaultwarden 容器..."
sudo docker stop "$CONTAINER_NAME"

echo "容器已停止，开始创建备份文件: $BACKUP_FILE_PATH"
tar -czf "$BACKUP_FILE_PATH" -C "$VAULTWARDEN_DATA_DIR" .

echo "备份文件创建完成，准备重启 Vaultwarden 容器..."
sudo docker start "$CONTAINER_NAME"

echo "容器已重启。本地备份完成。"

echo "开始上传备份文件到 OneDrive..."
rclone --config "$RCLONE_CONFIG_PATH" copy "$BACKUP_FILE_PATH" "$RCLONE_REMOTE_NAME:$ONEDRIVE_BACKUP_DIR" --progress

echo "文件上传成功。"

echo "开始清理7天前的本地旧备份..."
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +7 -delete
echo "旧备份清理完毕。"

echo "备份流程全部完成于: $(date +"%Y-%m-%d %H:%M:%S")"
```

**3. 添加执行权限**

```bash
chmod +x backup.sh
```

### 第三步：设置 Cron 定时任务

这是整个流程的终点，也是最容易失败的地方。

**1. 手动执行脚本，发现权限“连环坑”**

> **⚠️ 踩坑点 #4：`sudo` 密码问题**
> 
> **遭遇**：设置了 `cron` 任务后，发现不执行。查看日志 `cat ...backup.log`，发现错误 `sudo: a password is required`。
> **分析**：`cron` 在后台非交互式环境运行，无法响应 `sudo` 的密码输入请求。
> **解决**：通过 `sudo visudo` 命令，在打开的 `sudoers` 文件末尾添加一行，给予指定命令免密权限：
> 
> ```
> imsxx_com ALL=(ALL) NOPASSWD: /usr/bin/docker stop vaultwarden, /usr/bin/docker start vaultwarden
> ```

> **⚠️ 踩坑点 #5：`tar` 打包权限问题**
> 
> **遭遇**：解决了 `sudo` 问题后，手动以普通用户身份 `./backup.sh` 模拟 `cron` 执行，又报 `tar: Permission denied`。
> **分析**：之前用 `sudo` 运行脚本时，创建的 `vaultwarden_backups` 文件夹所有者是 `root`，普通用户 `imsxx_com` 没有写入权限。
> **解决**：用 `chown` 命令将文件夹“物归原主”：
> 
> ```bash
> sudo chown -R imsxx_com:imsxx_com /home/imsxx_com/vaultwarden_backups
> ```

**2. 最终的定时任务设置**

> **⚠️ 踩坑点 #6：Cron 的“极简”环境问题**
> 
> **遭遇**：解决了所有权限问题，手动 `./backup.sh` 已完美，但 `cron` 自动执行依然失败！
> **分析**：`cron` 的执行环境非常干净，它不知道各种命令的路径 (`PATH`)，也不会加载用户的环境变量配置文件 (`.profile`)。这是 `cron` 任务失败最根本、最常见的原因。
> **终极解决**：在 `crontab` 命令中，强制 `cron` 在运行脚本前先加载完整的用户环境。
> 
> 1. 运行 `crontab -e` 打开编辑器。
> 2. 写入下面这行**黄金代码**，这是解决所有 `cron` 疑难杂症的法宝：
>     ```bash
>     10 0 * * * /bin/bash -c 'source ~/.profile; /home/imsxx_com/backup.sh' >> /home/imsxx_com/vaultwarden_backup.log 2>&1
>     ```
>     
>     这行命令让 `cron` 先加载了 `.profile` 文件（相当于给机器人看了说明书），然后再执行我们的脚本，确保万无一失。我设置的时间是北京时间每天的 `00:10`。

### 第四步：个性化调整

**1. 修改服务器时区为北京时间**

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

**2. 验证最终成果**
设置好 `cron` 后，耐心等待设定的时间点到来。00:10登录你的 OneDrive，看到那个以北京时间命名的崭新备份文件时，就代表着你的自动化系统已经完美、稳定地开始运行了！你也可以把备份时间换成其他你想要的时间，只需要修改坑点6里代码行前面的10 0，它是24小时制的反写，也即分在前，时在后。如果你想改成每天凌晨03:00，就写成 0 3。

## 总结

从最初的构想，到踩遍环境、权限、`cron` 的每一个坑，再到最终看着备份文件准时出现在 OneDrive，这段经历让我受益匪浅。为重要数据建立一套自动化、异地的备份策略，是每一位服务器管理者应有的自觉。希望我这份详尽的“踩坑”与“填坑”指南，能为你节省大量的时间和精力，让你一步到位，高枕无忧。
