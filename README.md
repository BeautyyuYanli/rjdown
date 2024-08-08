# 人教电子教材下载

从 [人民教育出版社官网](https://jc.pep.com.cn/) 下载人教版电子教材生成 PDF 文件。

## 使用方法

1. 打开想要下载教材的在线阅读页面，获取教材 id 和总页数，写入配置文件 [conf.toml](conf.toml) 。例如 [数学-一年级上册](https://book.pep.com.cn/1221001101121/mobile/index.html) ，其 id 为 URL 中的 `1221001101121` ，总页数为 120，配置文件即为：

```toml
[[books]]
name="数学-一年级上册"
id="1221001101121"
total_page=120
```

2.  打开浏览器的开发者工具，在“**网络**”标签中找到对具体某一页图片的请求，把请求头中的 `User-Agent`(可选), `Cookie`(必须) 加到 [conf.toml](conf.toml) 里。

```toml
[request_header]
Cookie="YourCookie"
User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0"
```

3. (可选) 设置请求频率，单位为请求/秒。可能有助于规避风控。

```toml
request_per_second=5
```

4. 运行如下命令，以激活虚拟环境、执行脚本。文件会下载到当前目录下的 `output` 文件夹中。

```
pip install pdm
pdm sync
pdm run download conf.toml
```

## 注意事项

如果报错 "...Page Verification...", 可以在浏览器中刷新页面完成验证, 然后更新 Cookie, 运行脚本。
