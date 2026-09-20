# Model Museum · 手机 3D 展示

个人非商业技术研究与产品设计展示。纯静态 HTML / CSS / JavaScript + Three.js，无需后端、数据库或 API Key。

## 当前版本

- 简约亮白界面，左上角显示当前机型。
- 苹果 iPhone 18 Pro / Pro Max、小米 17 Ultra、华为 Pura 90 Pro Max、三星 Galaxy S26 Ultra。
- 品牌、机型、配色切换；拖动旋转、滚轮/双指缩放、视角预设、自动旋转及全屏。
- Three.js 与 GLB 文件随站点部署，不依赖外部模型地址。

## 部署到 Vercel

1. 在 Vercel 中导入 `SherW2012/model-museum`。
2. Root Directory 保持仓库根目录；Framework Preset 为 `Other`。
3. `vercel.json` 已设置跳过构建，Output Directory 为 `dist`。无需添加环境变量。
4. 点击 Deploy；后续向 `main` 提交会由已连接的 Vercel 项目自动部署。

仅上传 GitHub 不会自动创建 Vercel 项目，首次需要在 Vercel 导入仓库。

## 本地查看

在仓库根目录运行 `python -m http.server 8080 --directory dist`，浏览器访问 `http://localhost:8080`。请使用支持 WebGL2 的浏览器；不要直接双击 HTML 文件。

## 文件说明

- `dist/`：可直接部署的网站，含代码、模型、图片及 Three.js。
- `dist/catalog.js`：机型、配色、来源与模型路径。
- `scripts/`：模型转换、外观重建脚本；浏览网站时无需 Blender。
- `PROVENANCE.md`：素材来源、制作方法与既有验证记录。
- `THIRD_PARTY_NOTICES.md`：第三方素材与许可说明。

## 用途与素材

本站用于个人非商业技术研究与产品设计欣赏，不代表任何品牌，与相关品牌无隶属、合作或授权关系。商标、产品名称及第三方素材权利归相应权利人。自行重建的模型仅为近似外观，不是工程模型。

非商业声明不授予第三方素材使用权。Apple 模型和参考图的来源已记录，但本项目尚未核实独立的公开转载许可；不要把它们作为自有素材重新授权。详情见第三方说明。
