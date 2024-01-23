# 人教电子教材下载

从 [人教版官方电子教材](https://jc.pep.com.cn/) 下载产生 PDF 文件。

修改配置文件 [conf.toml](conf.toml)。例如 [日语必修一](https://book.pep.com.cn/1414001121221/mobile/index.html) 的 id 为 URL 中的 `1414001121221` ，总页数 92。

然后运行

```
pip install pdm
pdm sync
pdm run download conf.toml
```

文件会下载到当前目录下的 `output` 文件夹中。
