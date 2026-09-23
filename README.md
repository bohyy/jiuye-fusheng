# 旧页浮生

古籍中的三段人生：青瓷、皮影与苏绣。基于 Twine / Harlowe 的交互影游，包含剧情分支、手艺小游戏、剧情 QTE、浮生手札与本地存档。

## 网页发布结构

- `index.html`：交互游戏与界面代码。
- `assets/`：从本地游戏导出中无损提取的界面图片、图标与音频，重复素材合并。
- `media-manifest.json`：31 段原始剧情视频的章节、原片校验值与发布地址。视频上传到 Cloudflare R2，不做转码；`media-v1` Release 原片仍保留作为备份。

在线访问：<https://bohyy.github.io/jiuye-fusheng/>

GitHub Pages 从 `main` 分支根目录发布。视频源已切换到 Cloudflare R2 的公开 HTTPS 试播地址。

当前使用 `r2.dev` 开发地址，有速率限制且不提供 CDN 缓存，适合本次免费额度试播。正式大规模访问需另行配置自定义域名；见 [Cloudflare 公开存储桶说明](https://developers.cloudflare.com/r2/buckets/public-buckets/)。

存档保存在玩家当前浏览器的本地存储中，不会上传到 GitHub。网页与本地文件使用不同的存储空间。

本仓库只包含游戏发布内容，不包含论文、私人文档、电脑路径和项目备份。

原画质视频按需加载，流畅度取决于网络。视频来自 R2，与网页跨域；浏览器可能限制存档视频截图，此时显示章节主题图，路线、进度和属性仍正常保存。31 段视频已核对大小、视频类型及首中尾抽样字节；这是抽样核验，不是远程整片 SHA-256 校验。

## 更新网页

在本地游戏修改完成后运行：

```sh
python3 tools/build-site.py --input /path/to/current-twine-export.html
```

检查后将变更提交并推送到 `main`；GitHub Pages 会自动更新。该脚本不转码视频。若替换剧情视频，应新建素材版本并同步修改 `media-manifest.json`。
