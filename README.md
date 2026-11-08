# 听力刷题 · 连做版

一个**完全离线**的英语听力刷题工具，单文件 HTML，双击就能用。另附 Windows 桌面版与安卓版，三端跑的是**同一份 HTML**（apk 内嵌资源与 html 的 MD5 一致）。

- 11 套卷 · 179 题（六级听力真题 6 套 + 教材听力 5 套）
- 1 块课文填空（*Happy Birthday to You* 版权案，20 空）
- 不联网、不登录、无广告，答题记录只存在本机 `localStorage`

## 直接使用

| 文件 | 适用 | 说明 |
|---|---|---|
| `听力刷题-连做版.html` | 全平台 | 浏览器双击打开，Chrome / Edge / Safari 均可 |
| `听力刷题-连做版.exe` | Windows | 独立窗口，免安装；需要系统自带 WebView2（Win10/11 默认有） |
| `听力刷题-连做版.apk` | Android 5.0+ | 包名 `com.listen.drill.v3`，可与旧版共存 |

## 功能

**1. 一题一屏 / 同篇连做**

- Section A 的短对话：一题一屏，选完立刻判对错
- 长对话、短文：同一段材料的 3~4 题排在同一屏，往下翻连着做完，再点「提交本组」一次性判分
- 每屏底部固定「上一题 / 提交本组 / 下一组」

**2. 逐题判分**

提交后每题单独显示「正确 / 错误」，正确项绿框打勾、错选项标红，下方给答案、中文与串记；顶部一条「本组 4 题 · 答对 3」，题号色块一眼看出哪题错。

**3. 随机练习分三类**

短对话 30 题（一题一屏）· 长对话 68 题（17 篇）· 短文听力 81 题（23 篇）· 全部混合 179 题。

**4. 选项乱序**

首页开关，打开后所有练习的 A/B/C/D 位置逐题随机重排，防止靠位置记答案。进入练习时洗一次、整局固定，翻回上一题不会变。

**5. 串记 / 记忆钩子**

不给「同义替换」这类套路，直接给能背的：

- 长对话、短文 → 把这一篇 3~4 个答案串成一句话，题号嵌在句子里
  > ⑥不明飞行物在⑦凌晨五点落地，⑧野兽把他从车里拖出来，⑨他说自己大概是喝醉了。
- 短对话 → 一句短钩子，靠画面或谐音钉住答案
  > 记：八美元，发（8）财。

文案里不出现选项字母，所以选项乱序时不会指错。

**6. 课文填空**

按课文填词，边填边判：对的变绿打 ✓，错的变红打 ✗，改对自动转绿；`Enter` 跳下一空，可「显示答案」「重做」，全对记录最佳成绩。

**7. 键盘快捷键**

| 键 | 作用 |
|---|---|
| `A/B/C/D` 或 `1/2/3/4` | 选答案（连做页自动跳到下一道没做的题） |
| `←` | 上一题 |
| `Enter` | 提交本组 / 下一题 / 下一组；填空页跳到下一个空 |

## 题库结构

```
第 1~6 套    六级听力真题   24 题/套   Section A 短对话 5 + 长对话 + 短文
第 7~11 套   教材听力       7~8 题/套  Section A 长对话 4 + Section B 短文 3~4
课文填空     Happy Birthday to You     20 空
```

每套卷的题目存在 `src/bank.json`，字段：

```json
{
  "id": 11, "title": "第11套", "topic": "城市生活",
  "questions": [{
    "no": 1, "section": "A", "group": "Conversation One", "range": [1, 4],
    "answer": "C",
    "options": { "A": { "en": "Living expenses in London.", "zh": "伦敦的生活开支" }, "...": {} },
    "tip": "①聊的是在大城市生活，②房东要涨房租……"
  }]
}
```

`group` 相同的连续题目会被合成一个「连做单元」；没有 `group` 的题就是一题一屏。

## 目录

```
听力刷题-连做版.html     产物：单文件应用
听力刷题-连做版.exe      产物：Windows
听力刷题-连做版.apk      产物：Android
src/
  app_template_v3.html   前端模板（含 __BANK__ 占位符）
  bank.json              题库
  build.py               构建：模板 + 题库 → 单文件 HTML
  make_tips.py           生成串记
  mnemonic.py            串记文案与校验
  new_sets.py            第 7~10 套录入
  set11.py               第 11 套录入
desktop/
  launcher.py            pywebview 外壳（本地 HTTP + Host 白名单）
  app.ico
android/
  AndroidManifest.xml    单 Activity + WebView
  src/.../MainActivity.java
  build.sh               aapt2 + javac + d8 + apksigner 手工打包脚本
  res/  debug.keystore
docs/
  使用说明.txt
  代码审查报告.md
```

## 重新构建

只需要 Python 3：

```bash
python src/build.py
# 输出：项目根目录下的 听力刷题-连做版.html
```

桌面版（Windows，需要 `pip install pywebview pyinstaller`）：

```bash
cp 听力刷题-连做版.html desktop/index.html
cd desktop
pyinstaller --onefile --windowed --name "听力刷题-连做版" \
  --icon app.ico --add-data "index.html;." --collect-all webview launcher.py
```

安卓版需要 JDK 17 + Android SDK（build-tools 34、platform 34），把 html 放到 `android/assets/index.html` 后运行 `android/build.sh`。

## 已知限制

- **没有音频**：题库只有选项、译文和串记，需要配合原卷音频使用。
- **第 11 套答案待核**：卷面笔迹很淡，7 个答案是按字形 + 语义互证得出（1C 2B 3C 4D / 5B 6B 7C），第 4 题旁有手写「工作 机会」可确证，其余请对照标准答案。
- **apk 未真机验证**：本机没有安卓设备，只做了静态校验（签名、清单、内嵌资源 MD5）。
- **第 8 套缺第 8 题**：原卷照片只拍到第 7 题。

## License

仅用于个人学习。题目文字版权归原出版方所有。
