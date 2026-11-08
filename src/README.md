# src —— 题库与构建脚本

`build.py` 是唯一需要跑的一步：

```bash
python src/build.py      # 模板 + 题库 → 根目录的 听力刷题-连做版.html
```

## 数据

| 文件 | 说明 |
|---|---|
| `bank.json` | 11 套 179 题，字段见根目录 README |
| `app_template_v3.html` | 前端模板，`__BANK__` 处注入题库 JSON；课文填空的数据写死在模板里的 `CLOZE` 常量中 |

## 内容编辑脚本

这几个脚本是当初录入题库时用的，留着方便日后加卷子。它们都读写同目录的 `bank.json`，跑之前先备份。

| 脚本 | 作用 |
|---|---|
| `make_tips.py` | 按题型批量生成串记（默认模板，需配合 `bank_raw.json`） |
| `mnemonic.py` | 手工串记文案表 + 校验（每条必须包含正确选项的核心词） |
| `new_sets.py` | 录入第 7~10 套（教材听力） |
| `set11.py` | 录入第 11 套（Cities Unit 5） |

加一套新卷的常规做法：照 `set11.py` 的结构写一份，改 `id / title / topic / questions`，跑一次即可；`group` 相同的连续题目会被合成一个「连做单元」。

`mnemonic.py` 里的校验逻辑值得保留——它保证每条串记都真的包含答案内容，不会写成空话。
