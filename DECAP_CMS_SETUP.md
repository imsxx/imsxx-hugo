# Decap CMS 集成指南

本文档说明如何为 imsxx-hugo 博客项目集成 Decap CMS（原 Netlify CMS），实现在线协作编辑功能。

## 已完成的配置

### 1. CMS 文件结构
```
static/
└── admin/
    ├── index.html     # CMS 管理界面
    └── config.yml     # CMS 配置文件

layouts/
└── partials/
    └── head.html      # Netlify Identity Widget 脚本
```

### 2. 配置说明

- **后端**: 使用 Git Gateway 连接 GitHub
- **工作流**: 启用编辑工作流（草稿 → 审核 → 发布）
- **媒体存储**: 图片存储在 `static/images/uploads/`
- **内容集合**: 配置了博客文章和页面管理

## Netlify 部署配置

### 1. 连接 GitHub 仓库

1. 登录 [Netlify](https://netlify.com)
2. 点击 "New site from Git"
3. 选择 GitHub 并授权
4. 选择 `imsxx/imsxx-hugo` 仓库
5. 配置构建设置：
   - **Build command**: `hugo --minify`
   - **Publish directory**: `public`
   - **Environment variables**: 
     - `HUGO_VERSION`: `0.146.0`（或更高版本）

### 2. 启用 Netlify Identity

1. 在 Netlify 站点设置中，转到 "Identity"
2. 点击 "Enable Identity"
3. 在 "Registration preferences" 中选择 "Invite only"（推荐）
4. 在 "External providers" 中可以启用 GitHub 登录

### 3. 启用 Git Gateway

1. 在 Identity 设置中，转到 "Services"
2. 点击 "Enable Git Gateway"
3. 这将允许 CMS 通过 Netlify 访问 GitHub 仓库

### 4. 邀请用户

1. 在 Identity 标签页中，点击 "Invite users"
2. 输入要邀请的用户邮箱
3. 用户将收到邀请邮件来设置密码

## 使用 CMS

### 访问管理界面

部署完成后，访问 `https://你的域名.netlify.app/admin/` 进入 CMS 管理界面。

### 功能特性

1. **文章管理**
   - 创建、编辑、删除博客文章
   - 支持 Markdown 编辑器
   - 实时预览
   - 设置分类和标签

2. **媒体管理**
   - 上传和管理图片
   - 支持拖拽上传
   - 图片优化

3. **工作流**
   - 草稿状态
   - 待审核状态
   - 发布状态

### 文章字段说明

- **标题**: 文章标题
- **作者**: 默认为 "梦随乡兮"
- **发布日期**: 文章发布时间
- **URL别名**: 自定义 URL slug
- **分类**: 文章分类（可多选）
- **标签**: 文章标签（可多选）
- **摘要**: 文章摘要描述
- **特色图片**: 文章封面图
- **草稿**: 是否为草稿状态
- **正文**: 文章内容（Markdown 格式）

## 自定义域名配置

如果使用自定义域名（如 imsxx.com），需要：

1. 在 Netlify 中配置自定义域名
2. 更新 `static/admin/config.yml` 中的 `site_url` 和 `display_url`
3. 确保 SSL 证书正确配置

## 故障排除

### 常见问题

1. **无法登录 CMS**
   - 检查 Netlify Identity 是否已启用
   - 确认用户已被邀请并激活
   - 检查 Git Gateway 是否已启用

2. **文章无法保存**
   - 检查 GitHub 仓库权限
   - 确认 Git Gateway 配置正确
   - 查看 Netlify 构建日志

3. **图片上传失败**
   - 检查媒体文件夹路径配置
   - 确认文件大小限制
   - 检查网络连接

### 调试步骤

1. 检查浏览器控制台错误信息
2. 查看 Netlify 部署日志
3. 验证 `config.yml` 语法正确性
4. 确认所有必要的脚本已加载

## 进阶配置

### 自定义字段

可以在 `static/admin/config.yml` 中添加更多字段：

```yaml
fields:
  - {label: "SEO标题", name: "seo_title", widget: "string", required: false}
  - {label: "SEO描述", name: "seo_description", widget: "text", required: false}
  - {label: "是否置顶", name: "sticky", widget: "boolean", default: false}
```

### 媒体库配置

当前使用 Uploadcare 作为媒体库，可以：

1. 注册 [Uploadcare](https://uploadcare.com) 账户
2. 获取 Public Key
3. 替换 `config.yml` 中的 `demopublickey`

## 支持

如有问题，请：

1. 查看 [Decap CMS 官方文档](https://decapcms.org/docs/)
2. 检查 [Netlify 文档](https://docs.netlify.com/)
3. 在项目 Issues 中提问

---

配置完成后，你就可以通过 Web 界面轻松管理博客内容，支持多人协作编辑！