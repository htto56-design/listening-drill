# -*- coding: utf-8 -*-
"""把 4 张照片整理成第 7~10 套，追加进 bank.json。

每套结构：Section A 长对话 4 题（同屏连做）+ Section B 短文 3~4 题（同屏连做）
答案取自卷面上的手写标记。
"""
import json, os, re

def Q(no, ans, opts, tip=None):
    return {"no": no, "answer": ans,
            "options": {k: {"en": v[0], "zh": v[1]} for k, v in zip("ABCD", opts)},
            "tip": tip}

SETS = []

# ---------------- 第 7 套 · 节日（Festivals Unit 4） ----------------
SETS.append({
    "id": 7, "title": "第7套", "topic": "节日",
    "questions": [
        Q(1, "D", [
            ("New Year's resolutions.", "新年的决心"),
            ("Reflections on the past year.", "对过去一年的回顾"),
            ("Festive atmosphere of the new year in town.", "城里新年的节日气氛"),
            ("How to celebrate the upcoming new year.", "如何庆祝即将到来的新年"),
        ]),
        Q(2, "B", [
            ("Having a cozy dinner at home.", "在家吃顿温馨的晚餐"),
            ("Going to a big outdoor event in the city.", "去城里的大型户外活动"),
            ("Watching the countdown on TV.", "在电视上看倒计时"),
            ("Reflecting on the past year.", "回顾过去一年"),
        ]),
        Q(3, "A", [
            ("Focusing on health.", "关注健康"),
            ("Learning a new skill or hobby.", "学一门新技能或爱好"),
            ("Making personal growth a priority.", "把个人成长放在首位"),
            ("Enjoying live music and fireworks.", "享受现场音乐和烟花"),
        ]),
        Q(4, "A", [
            ("By drinking champagne.", "喝香槟"),
            ("By hugging and wishing each other well.", "拥抱并互致祝福"),
            ("By reflecting on the past year.", "回顾过去一年"),
            ("By gathering around midnight.", "午夜时分聚在一起"),
        ]),
        Q(5, "C", [
            ("The story of Chang'e.", "嫦娥的故事"),
            ("The tradition of eating mooncakes.", "吃月饼的传统"),
            ("The origin and customs of the Mid-Autumn Festival.", "中秋节的起源与习俗"),
            ("The traditional celebrating events of the Mid-Autumn Festival.", "中秋节的传统庆祝活动"),
        ]),
        Q(6, "B", [
            ("The worship of Chang'e.", "对嫦娥的崇拜"),
            ("The worship of the moon.", "对月亮的崇拜"),
            ("The worship of the jade rabbit.", "对玉兔的崇拜"),
            ("The worship of the moon goddess.", "对月神的崇拜"),
        ]),
        Q(7, "A", [
            ("Reunion and affection.", "团圆与亲情"),
            ("Togetherness and friendship.", "相聚与友谊"),
            ("Reunion and friendship.", "团圆与友谊"),
            ("Tradition and affection.", "传统与亲情"),
        ]),
        Q(8, "C", [
            ("Expressions of gratitude.", "表达感恩"),
            ("Family reunions.", "家庭团聚"),
            ("Worship of gods and goddesses.", "对神灵的崇拜"),
            ("The appreciation of nature's beauty.", "对自然之美的欣赏"),
        ]),
    ],
    "tips": {
        "Conversation One": "①商量怎么庆祝新年，②她去城里的大型户外活动，③他的决心是关注健康，④最后举杯喝香槟。",
        "Passage One": "⑤中秋的起源与习俗，⑥古人拜的是月亮，⑦讲的是团圆与亲情，⑧最后提到对神灵的崇拜。",
    },
})

# ---------------- 第 8 套 · 饮食（Food Unit 3，照片缺第 8 题） ----------------
SETS.append({
    "id": 8, "title": "第8套", "topic": "饮食",
    "questions": [
        Q(1, "C", [
            ("Korean foods.", "韩国食物"),
            ("Korean restaurants.", "韩国餐馆"),
            ("Eating out.", "外出就餐"),
            ("Fried chickens.", "炸鸡"),
        ]),
        Q(2, "D", [
            ("It serves Korean food.", "它供应韩国菜"),
            ("It is named after its chef.", "它以厨师的名字命名"),
            ("She knows the owner of Jinjuu.", "她认识 Jinjuu 的老板"),
            ("It serves traditional Korean street food.", "它供应传统韩国街头小吃"),
        ]),
        Q(3, "C", [
            ("It is quite expensive to eat there.", "在那儿吃饭相当贵"),
            ("The price is quite reasonable in the restaurant.", "这家餐厅价格相当合理"),
            ("The pricing information is not found on its website.", "官网上找不到价格信息"),
            ("Jenny can't afford to eat there.", "珍妮吃不起那儿"),
        ]),
        Q(4, "B", [
            ("Ted.", "泰德"),
            ("Jenny.", "珍妮"),
            ("Jane.", "简"),
            ("They will split the bill.", "他们会各付各的"),
        ]),
        Q(5, "B", [
            ("Different flavors of Chinese food in different regions.", "不同地区中餐的不同风味"),
            ("Regional diversity, balance and visual appeal of Chinese food.", "中餐的地域多样性、平衡与视觉美感"),
            ("The importance of balance and harmony in Chinese food.", "中餐里平衡与和谐的重要性"),
            ("The importance of visual aesthetics in Chinese food.", "中餐视觉美学的重要性"),
        ]),
        Q(6, "D", [
            ("It is unique for Chinese cooking.", "它是中式烹饪独有的"),
            ("It is an excellent tool for the spicy food of Sichuan.", "它是做川菜辣味的好工具"),
            ("Rice and noodles are staple ingredients for it.", "米饭和面条是它的主要食材"),
            ("Foods are cooked quickly over high heat in it.", "食物在里面用大火快炒"),
        ]),
        Q(7, "C", [
            ("Flavors.", "风味"),
            ("Colors.", "色彩"),
            ("Nutrition.", "营养"),
            ("Textures.", "口感"),
        ]),
    ],
    "tips": {
        "Conversation One": "①两人在聊外出就餐，②那家店做传统韩国街头小吃，③可官网查不到价格，④最后珍妮买单。",
        "Passage One": "⑤中餐的地域多样性与视觉美感，⑥靠大火快炒，⑦最后落在营养上。",
    },
})

# ---------------- 第 9 套 · 教育（Education Unit 1） ----------------
SETS.append({
    "id": 9, "title": "第9套", "topic": "教育",
    "questions": [
        Q(1, "A", [
            ("Freshman.", "大一新生"),
            ("Sophomore.", "大二学生"),
            ("Junior.", "大三学生"),
            ("Senior.", "大四学生"),
        ]),
        Q(2, "A", [
            ("He joins in club activities.", "他参加社团活动"),
            ("He has classes.", "他有课"),
            ("He goes to the library.", "他去图书馆"),
            ("He meets his teacher.", "他去见老师"),
        ]),
        Q(3, "C", [
            ("Once a week.", "每周一次"),
            ("Once a day.", "每天一次"),
            ("Every other week.", "每两周一次"),
            ("Twice a day.", "每天两次"),
        ]),
        Q(4, "C", [
            ("Attending lectures.", "听课"),
            ("Running on the playground.", "在操场跑步"),
            ("Sightseeing in the city center.", "在市中心观光"),
            ("Doing presentations in different classes.", "在不同班级做展示"),
        ]),
        Q(5, "A", [
            ("Education.", "教育"),
            ("Employment.", "就业"),
            ("Poverty reduction.", "减贫"),
            ("Human rights.", "人权"),
        ]),
        Q(6, "B", [
            ("79%.", "79%"),
            ("97%.", "97%"),
            ("82%.", "82%"),
            ("41%.", "41%"),
        ]),
        Q(7, "B", [
            ("1,486.", "1,486"),
            ("2,756.", "2,756"),
            ("1,270.", "1,270"),
            ("1,217.", "1,217"),
        ]),
        Q(8, "A", [
            ("1,486.", "1,486"),
            ("2,756.", "2,756"),
            ("1,270.", "1,270"),
            ("1,217.", "1,217"),
        ]),
    ],
    "tips": {
        "Conversation One": "①他是大一新生，②课后去参加社团活动，③每两周一次，④在市中心观光。",
        "Passage One": "⑤讲的是教育，⑥97%，⑦2,756，⑧1,486。",
    },
})

# ---------------- 第 10 套 · 水资源（Water Unit 2） ----------------
SETS.append({
    "id": 10, "title": "第10套", "topic": "水资源",
    "questions": [
        Q(1, "B", [
            ("At a shop.", "在商店"),
            ("At a travel agency.", "在旅行社"),
            ("At a hotel.", "在酒店"),
            ("At a station.", "在车站"),
        ]),
        Q(2, "C", [
            ("Asia.", "亚洲"),
            ("America.", "美洲"),
            ("Africa.", "非洲"),
            ("Europe.", "欧洲"),
        ]),
        Q(3, "C", [
            ("One year ago.", "一年前"),
            ("Two years ago.", "两年前"),
            ("Three years ago.", "三年前"),
            ("Four years ago.", "四年前"),
        ]),
        Q(4, "B", [
            ("Discussing the importance of the Yangtze River.", "讨论长江的重要性"),
            ("Planning a trip to visit the Yangtze River.", "计划去长江旅游"),
            ("Comparing the Yangtze River with other rivers.", "把长江与其他河流作比较"),
            ("Sharing personal travel experiences.", "分享个人旅行经历"),
        ]),
        Q(5, "A", [
            ("Water pollution.", "水污染"),
            ("Water protection.", "水资源保护"),
            ("Water irrigation.", "水利灌溉"),
            ("Water supply.", "供水"),
        ]),
        Q(6, "D", [
            ("The development of the world.", "世界的发展"),
            ("The development of the Earth.", "地球的演化"),
            ("The development of agriculture.", "农业的发展"),
            ("The development of industry.", "工业的发展"),
        ]),
        Q(7, "D", [
            ("Rivers.", "河流"),
            ("Seas.", "海洋"),
            ("Oceans.", "大洋"),
            ("Lakes.", "湖泊"),
        ]),
        Q(8, "B", [
            ("Negative.", "否定的；消极的"),
            ("Positive.", "积极的；正面的"),
            ("Doubtful.", "怀疑的"),
            ("Hesitant.", "犹豫的"),
        ]),
    ],
    "tips": {
        "Conversation One": "①在旅行社，②她来自非洲，③三年前，④两人在计划去长江的旅行。",
        "Passage One": "⑤水污染，⑥工业发展是绕不开的因素，⑦湖泊，⑧作者态度是积极的。",
    },
})


def lcs(a, b):
    best, prev = 0, [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def build(spec):
    qs, prev, grange = [], None, None
    for q in spec["questions"]:
        if q["no"] <= 4:
            grp, rng, sec = "Conversation One", [1, 4], "A"
        else:
            grp, sec = "Passage One", "B"
            rng = [5, 8] if len(spec["questions"]) >= 8 else [5, len(spec["questions"])]
        q["section"] = sec
        q["group"] = grp
        q["range"] = rng
        q["tip"] = spec["tips"][grp]
        q["tipType"] = "chain"
        qs.append(q)
    return {"id": spec["id"], "title": spec["title"], "topic": spec["topic"], "questions": qs}


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank.json')
    bank = json.load(open(path, encoding="utf-8"))
    bank = [s for s in bank if s["id"] not in (7, 8, 9, 10)]

    warn = []
    for spec in SETS:
        st = build(spec)
        for q in st["questions"]:
            core = re.sub(r"[。，、；：！？（）《》“”%]", "", q["options"][q["answer"]]["zh"])
            need = 1 if len(core) <= 2 else 2
            if lcs(core, q["tip"]) < need:
                warn.append("WEAK %d-%d ans=%s" % (st["id"], q["no"], core))
        bank.append(st)

    bank.sort(key=lambda s: s["id"])
    json.dump(bank, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    total = sum(len(s["questions"]) for s in bank)
    print("sets", len(bank), "questions", total)
    for s in bank:
        print("  第%d套 %-4s %2d 题  %s" % (s["id"], s.get("topic", ""), len(s["questions"]), s["title"]))
    print("warn", warn if warn else "none")


if __name__ == "__main__":
    main()
