# 自定义字体配置说明

本文档记录了网站自定义字体 SmileySans 的配置方法，确保在主题更新或更换时不会丢失字体设置。

## 字体文件

- **字体名称**: SmileySans (得意黑)
- **文件位置**: `static/fonts/SmileySans-Oblique.otf.woff2`
- **字体格式**: WOFF2 (Web Open Font Format 2.0)

## 配置文件

### 1. CSS 样式文件

**文件路径**: `assets/css/custom.css`

```css
@font-face {
  font-family: 'SmileySans';
  src: url('/fonts/SmileySans-Oblique.otf.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

body {
  font-family: 'SmileySans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 文章正文字体 */
.prose {
  font-family: 'SmileySans', ui-sans-serif, system-ui, sans-serif !important;
}

/* 确保文章内所有文本元素都使用自定义字体 */
.prose p,
.prose h1,
.prose h2,
.prose h3,
.prose h4,
.prose h5,
.prose h6,
.prose li,
.prose blockquote,
.prose td,
.prose th {
  font-family: 'SmileySans', ui-sans-serif, system-ui, sans-serif !important;
}
```

### 2. HTML 模板引用

**文件路径**: `themes/hugo-narrow/layouts/baseof.html`

在 `<head>` 部分添加以下代码：

```html
{{ $customCSS := resources.Get "css/custom.css" | resources.Minify }}
<link rel="stylesheet" href="{{ $customCSS.RelPermalink }}">
```

## 主题更换/更新注意事项

### 更换主题时

1. **保留字体文件**: 确保 `static/fonts/` 目录及其内容被保留
2. **保留CSS文件**: 确保 `assets/css/custom.css` 文件被保留
3. **更新模板引用**: 在新主题的 `baseof.html` 或相应的头部模板中添加CSS引用

### 更新主题时

1. **备份配置**: 更新前备份 `themes/hugo-narrow/layouts/baseof.html` 中的自定义CSS引用
2. **重新应用**: 更新后重新添加CSS引用到新的模板文件中

## 验证方法

1. 启动 Hugo 服务器: `hugo server`
2. 打开浏览器访问 `http://localhost:1313/`
3. 检查页面字体是否为 SmileySans
4. 特别检查文章正文字体是否生效

## 故障排除

### 字体未加载

- 检查字体文件路径是否正确
- 检查浏览器开发者工具的网络面板，确认字体文件加载成功
- 检查CSS文件是否正确引用

### 文章正文字体未生效

- 确认 `.prose` 相关的CSS规则已添加
- 检查CSS优先级，必要时使用 `!important`

### 主题更新后字体丢失

- 检查 `baseof.html` 中的CSS引用是否还存在
- 重新添加CSS引用代码

## 字体切换功能

### 功能说明
- 在菜单栏添加了字体切换按钮（位于配色切换按钮前面）
- 支持两种字体模式：
  - **SmileySans**: 自定义字体（默认）
  - **系统字体**: 使用系统默认字体
- 字体设置会保存在浏览器本地存储中

### 实现文件
1. **UI组件**: `themes/hugo-narrow/layouts/_partials/ui/font-switcher.html`
2. **JavaScript逻辑**: `themes/hugo-narrow/assets/js/main.js` (UIManager类)
3. **CSS样式**: `assets/css/custom.css` (字体切换相关样式)
4. **配置**: `hugo.toml` (showFontSwitch参数)

### 技术实现
- 通过 `data-font` 属性控制HTML根元素的字体模式
- JavaScript管理字体状态和本地存储
- CSS使用属性选择器应用不同字体

## 配置历史

- **2025-07-22**: 初始配置，添加 SmileySans 字体支持
- **2025-07-22**: 修复文章正文字体不生效问题
- **2025-07-22**: 添加配置文档和说明注释
- **2025-01-XX**: 添加字体切换功能