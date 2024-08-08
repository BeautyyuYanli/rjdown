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

2.  打开浏览器的开发者工具，在“**网络**”标签中找到对具体某一页图片的请求，把请求头中的 `referer`, `cookie` 加到代码里。

```py
request_header={ 
    "Referer": "Your-Referer", # 这个不加会返回403
    "Cookie": "Your-Cookie" # 这个不加会返回机器人验证
}

...

def main():
    ...
    client = httpx.Client(headers=request_header)  # 这边记得加上
```

3. 运行如下命令，以激活虚拟环境、执行脚本。文件会下载到当前目录下的 `output` 文件夹中。

```
pip install pdm
pdm sync
pdm run download conf.toml
```
