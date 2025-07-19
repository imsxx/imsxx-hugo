# Decap CMS 集成指南

本文档说明如何为 imsxx-hugo 博客项目集成 Decap CMS（原 Netlify CMS），实现在线协作编辑功能。适用于 GitHub + Cloudflare Pages 部署方式。

## 已完成的配置

### 1. CMS 文件结构
```
static/
└── admin/
    ├── index.html     # CMS 管理界面
    └── config.yml     # CMS 配置文件
```

### 2. 配置说明

- **后端**: 直接使用 GitHub API 连接仓库
- **认证方式**: GitHub OAuth 应用认证
- **工作流**: 启用编辑工作流（草稿 → 审核 → 发布）
- **媒体存储**: 图片存储在 `static/images/uploads/`
- **内容集合**: 配置了博客文章和页面管理

## GitHub OAuth 应用配置

### 1. 创建 GitHub OAuth 应用

1. 登录 GitHub，进入 [Settings > Developer settings > OAuth Apps](https://github.com/settings/developers)
2. 点击 "New OAuth App"
3. 填写应用信息：
   - **Application name**: `imsxx-hugo-cms`
   - **Homepage URL**: `https://imsxx.com`
   - **Authorization callback URL**: `https://imsxx.com/admin/`
4. 点击 "Register application"
5. 记录生成的 **Client ID** 和 **Client Secret**

### 2. 配置 CMS 认证

在 `static/admin/config.yml` 中添加 GitHub OAuth 配置：

```yaml
backend:
  name: github
  repo: imsxx/imsxx-hugo
  branch: main
  auth_type: pkce # 推荐使用 PKCE 认证
```

### 3. Cloudflare Pages 部署

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 "Pages" 部分
3. 点击 "Create a project" > "Connect to Git"
4. 选择 `imsxx/imsxx-hugo` 仓库
5. 配置构建设置：
   - **Framework preset**: Hugo
   - **Build command**: `hugo --minify`
   - **Build output directory**: `public`
   - **Environment variables**: 
     - `HUGO_VERSION`: `0.146.0`

### 4. 配置自定义域名

1. 在 Cloudflare Pages 项目设置中添加自定义域名 `imsxx.com`
2. 确保 DNS 记录正确指向 Cloudflare Pages
3. 启用 SSL/TLS 加密

## 使用 CMS

### 访问管理界面

1. 访问 `https://imsxx.com/admin/`
2. 点击 "Login with GitHub" 进行 GitHub OAuth 认证
3. 授权应用访问仓库权限
4. 开始编辑内容

### 功能特性

- **在线编辑**: 直接在浏览器中编写和编辑文章
- **实时预览**: 支持 Markdown 实时预览
- **媒体管理**: 上传和管理图片等媒体文件
- **工作流管理**: 支持草稿、审核、发布流程
- **协作编辑**: 多人协作编辑和审核
- **中文界面**: 完全中文化的管理界面

### 文章字段说明

- **标题**: 文章标题
- **作者**: 默认为 "梦随乡兮"
- **发布日期**: 文章发布时间
- **URL别名**: 自定义文章 URL（可选）
- **分类**: 文章分类标签
- **标签**: 文章标签
- **摘要**: 文章简介（可选）
- **特色图片**: 文章封面图（可选）
- **草稿**: 是否为草稿状态
- **正文**: 文章内容（Markdown 格式）

## 自定义域名配置

如果使用自定义域名，需要更新以下配置：

1. 在 `config.yml` 中更新 `site_url`
2. 在 GitHub OAuth 应用中更新回调 URL
3. 确保域名正确解析到 Cloudflare Pages

## 故障排除

### 1. 无法访问 /admin/ 页面
- 检查 `static/admin/index.html` 文件是否存在
- 确认网站已正确部署到 Cloudflare Pages
- 检查自定义域名配置是否正确

### 2. GitHub OAuth 登录问题
- 确认 OAuth 应用的回调 URL 配置正确
- 检查 `config.yml` 中的仓库名称是否正确
- 确认 OAuth 应用状态为 Active

### 3. 无法保存文章
- 确认 GitHub 用户有仓库的写入权限
- 检查分支名称配置是否正确（main/master）
- 查看浏览器控制台错误信息
- 确认 GitHub API 访问限制

### 4. 图片上传失败
- 检查媒体文件夹路径配置
- 确认文件大小限制
- 验证图片格式支持

### 调试步骤

1. 检查浏览器控制台错误信息
2. 查看 Cloudflare Pages 部署日志
3. 验证 `config.yml` 语法正确性
4. 确认所有必要的脚本已加载

## 进阶配置

### 自定义字段

<<<<<<< HEAD
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
=======
可以在 `config.yml` 中添加更多自定义字段，如：

```yaml
fields:
  - {label: "SEO关键词", name: "keywords", widget: "list", required: false}
  - {label: "文章类型", name: "type", widget: "select", options: ["技术", "生活", "随笔"]}
  - {label: "置顶", name: "sticky", widget: "boolean", default: false}
```

### 多语言支持

如需支持多语言，可以配置多个集合：

```yaml
collections:
  - name: "blog-zh"
    label: "中文博客"
    folder: "content/zh/posts"
  - name: "blog-en"
    label: "English Blog"
    folder: "content/en/posts"
```

### 自定义预览模板

可以创建自定义预览模板来更好地展示内容预览效果。

---

**注意**: 首次使用需要完成 GitHub OAuth 应用配置，确保所有权限设置正确。
>>>>>>> 8d82209fdaa6d8e4e8356253b12e95bb9d7e0cf4
