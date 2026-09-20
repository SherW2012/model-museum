# Model Museum · 手机 3D 展示

个人非商业 Web 3D / 产品外观设计研究项目。

## 当前可运行版本

- Apple 风格简约亮白界面：左上角仅显示机型名称，不放网站 Logo。
- Apple iPhone 18 Pro、iPhone 18 Pro Max（各四种示意配色）；Xiaomi 17 Ultra（三色）；HUAWEI Pura 90 Pro Max（五色）；Samsung Galaxy S26 Ultra（四色）。
- 切换品牌、机型和配色；拖拽旋转、鼠标滚轮/双指缩放、正反面预设、自动旋转、局部放大和全屏。
- 纯静态 `index.html`，使用 Three.js 的 WebGL 渲染；无需服务器、数据库、账户、API Key 或环境变量。

**源码来源说明：** 原先发布在 ChatGPT Site 的版本无法从本次会话读取原始文件，因此本仓库当前的 `index.html` 是按此前确定的功能与视觉需求重新构建的**可部署版本**，并非原站点逐文件原样迁移。设备由程序化几何体生成，是外观示意模型，不含官方或高精度 GLB/CAD 模型；实际尺寸、结构与配色未作官方校验。此前 README 中对 `dist/`、本地 GLB、素材许可文档及转换脚本的说明与仓库当时的真实文件不符，现已纠正。

## 部署至 Vercel

1. 在 [Vercel](https://vercel.com/new) 中选择导入 `SherW2012/model-museum`。
2. Root Directory 选仓库根目录，Framework Preset 选 `Other`。
3. Build Command 保持空白/不启用；Output Directory 保持默认，不填 `dist`。
4. 部署。后续向 `main` 推送代码，已连接的 Vercel 项目会自动部署。

仅提交 GitHub 并不会自动创建 Vercel 项目，首次需完成 Vercel 导入。

## 本地运行

```bash
python -m http.server 8080
```

然后打开 `http://localhost:8080`。不要双击 `index.html` 使用 `file://` 打开。

## 依赖与文件

- `index.html`：HTML、CSS、JavaScript、机型配置及程序化 3D 几何体。
- `vercel.json`：静态托管的基础 HTTP 头配置。
- Three.js `0.180.0` 与 `OrbitControls` 通过 jsDelivr CDN 加载，**运行时需要连接 CDN**；本仓库目前没有打包或镜像第三方 JS 文件。

## 非商业及权利声明

项目独立开发，仅作个人非商业设计、前端技术与交互研究；不代表 Apple、小米、华为、三星，与这些公司无隶属、合作或授权关系。公司与产品名称归各自权利人。非商业用途本身并不自动授予第三方商标、工业设计或素材使用许可。本项目未分发第三方设备模型、图片或 GLB 素材。
