# voice
基于HoshinoBot V2的合成语音插件

项目地址：https://github.com/Yuri-YuzuChaN/voice

如果对该项目的语音训练有兴趣，可以查看项目 [MoeGoe](https://github.com/CjangCjengh/MoeGoe) 和 [Hugging Face](https://huggingface.co/spaces/skytnt/moe-japanese-tts)

## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/voice`
2. pip以下依赖：`aiohttp`, `websockets`
3. 在 `config/__bot__.py` 模块列表中添加 `voice`
4. 重启HoshinoBot

**请务必将 `nonebot` 和 `aiocqhttp` 依赖更新至最新版本**

## 指令说明

[角色]说[语言] [文本]：合成自定义语言

- 例如：宁宁说日文 はじめまして

[语言]语言帮助：查看该语音可用角色

- 例如：中文语言帮助

语言分类：

- 译文：输入中文自动翻译成日语
- 日语：纯日语，尽量输入假名
- 日文：纯日语，尽量输入假名
- 韩语：纯韩语
- 中文：纯中文语音

## 更新说明

**2022-08-28**

1. API从HTTP更改为WS
2. 新增《美少女万花镜》
3. 修改中文语速

**2022-08-26**

1. 修改API请求内容
2. 修改语音帮助
