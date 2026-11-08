# -*- coding: utf-8 -*-
"""把「题型套路」型妙招换成「答案串记」型记忆钩子。

规则：
- Section B/C：一段录音的 3~4 个答案串成一句带题号的话，读一遍就能把整段答案带走
- Section A：单题给一个短钩子，靠画面 / 谐音钉住那一个答案
- 句子里不出现选项字母，所以选项乱序时永远指不错
"""
import json, os, re

# 单题钩子：setId-no
SINGLE = {
    "1-1": "记：赶车别磨蹭，一路冲站台。",
    "1-2": "记：意餐、快餐都靠边，馋的还是中餐馆。",
    "1-3": "记：活儿干不完，先歇一会儿——休息一下。",
    "1-4": "记：聚会一场接一场，课自然跟不上。",
    "1-5": "记：八美元，发（8）财。",

    "2-1": "记：她不该选这么多课，贪多嚼不烂。",
    "2-2": "记：六美元，溜（6）得比谁都快。",
    "2-3": "记：2017，一起（17）走过的那年。",
    "2-4": "记：电梯出事，人没事——伤得不重。",
    "2-5": "记：下午有雨，出门带伞。",

    "3-1": "记：走累了，坐下喝杯咖啡。",
    "3-2": "记：13:00，下午一点整。",
    "3-3": "记：乌云压顶，暴风雨要来。",
    "3-4": "记：手慢一步，就没机会选这门课。",
    "3-5": "记：雨下得很大，门都出不去。",

    "4-1": "记：论文摊在桌上，一行没读。",
    "4-2": "记：总搬家，东西自然找不着。",
    "4-3": "记：箱子死沉，抬都抬不动。",
    "4-4": "记：网上购物是便宜，缺点也不少。",
    "4-5": "记：红色？她看一眼都嫌。",

    "5-1": "记：钱要算着花——仔细规划开支。",
    "5-2": "记：约在哪儿？餐厅。",
    "5-3": "记：玛吉？他认识好多年了。",
    "5-4": "记：纽约哪条街他都门儿清。",
    "5-5": "记：机会？她摇头——不划算。",

    "6-1": "记：衬衫照穿，领带免了。",
    "6-2": "记：三明治他请，钱包他掏。",
    "6-3": "记：先把车修好，别的再说。",
    "6-4": "记：她就好恐怖片这一口。",
    "6-5": "记：2:45，差一刻三点。",
}

# 段级串记：setId|篇名
GROUP = {
    "1|Conversation One": "⑥不明飞行物在⑦凌晨五点落地，⑧野兽把他从车里拖出来，⑨他说自己大概是喝醉了。",
    "1|Conversation Two": "⑩两人突击备考，⑪约在晚上7:30，⑫只能在家学习，⑬艾米怕是半夜才回。",
    "1|Passage One": "⑭家人坚定支持，⑮她写完三部小说又动第四部，⑯公开身份会毁掉女性名誉，⑰那部叫《桑迪顿》。",
    "1|Passage Two": "⑱1985年，⑲他在新创的投资公司兼职，⑳做金融与银行业投资，㉑只为让年轻人选对路。",
    "1|Passage Three": "㉒变的是气流，㉓只有两个，㉔北极暖得异常快。",

    "2|Conversation One": "⑥女服务员招呼顾客，⑦披萨不合她口味，⑧一半辣香肠蘑菇一半青椒，⑨送到南16东街1340号。",
    "2|Conversation Two": "⑩菲尔去日本公共澡堂，⑪什么都不用带，⑫顺便和邻居社交，⑬还互相搓背。",
    "2|Passage One": "⑭乱花钱它就电你，⑮255伏，⑯以后一切都联网，⑰人只买东西不看余额。",
    "2|Passage Two": "⑱俄罗斯的时尚，⑲没人买他们的武器了，⑳只能靠造枪，㉑爱国主义情绪高涨。",
    "2|Passage Three": "㉒电来自阳光，㉓撑了118小时，㉔就为展示清洁技术。",

    "3|Conversation One": "⑥他买得太多，⑦狗还是别人送的，⑧这些对他没好处，⑨女士最后生气了。",
    "3|Conversation Two": "⑩预报说会下雨，⑪可它从来不准，⑫干脆玩纸牌，⑬等天放晴。",
    "3|Passage One": "⑭OpenAI Gym，⑮一个有AI教练的健身房，⑯要做的是多任务算法。",
    "3|Passage Two": "⑰人最怕失去，⑱把脚搭在桌上，⑲摆强势姿势的更多去赌。",
    "3|Passage Three": "⑳她是棒球队的捡球棒狗，㉑专逗裁判笑，㉒被发现时身上没证件。",

    "4|Conversation One": "⑥她需要帮忙，⑦东西在湖底，⑧他喜欢「父亲」发在脸书的内容，⑨其实他连脸书都不会用。",
    "4|Conversation Two": "⑩时速20英里，⑪他求警察放他一马，⑫数字5，⑬警察与司机。",
    "4|Passage One": "⑭要么超重要么过轻，⑮这些人得不到足够医疗帮助，⑯她不愿为饮食去看医生，⑰725,000。",
    "4|Passage Two": "⑱大猩猩被枪杀，⑲大家说该用麻醉枪，⑳母亲和动物园都该负责。",
    "4|Passage Three": "㉑全球青年失业，㉒11.1%，㉓中东和北非最惨，㉔祸根是2008年金融危机。",

    "5|Conversation One": "⑥同学，⑦他劝她保证充足睡眠，⑧数字8，⑨可她只睡不到5小时。",
    "5|Conversation Two": "⑩父母是真爱他，⑪手机没问题，⑫他要的是独立，⑬这事只能他自己解决。",
    "5|Passage One": "⑭怕法国人听不成广播，⑮要挡住英语渗入，⑯发言人说法新法必要。",
    "5|Passage Two": "⑰人最怕失去，⑱把脚搭在桌上，⑲摆强势姿势的更多去赌。",
    "5|Passage Three": "⑳电来自阳光，㉑撑了118小时，㉒就为展示清洁技术。",

    "6|Conversation One": "⑥两人突击备考，⑦约在晚上7:30，⑧只能在家学习，⑨艾米怕是半夜才回。",
    "6|Conversation Two": "⑩她需要帮忙，⑪东西在湖底，⑫他喜欢「父亲」发在脸书的内容，⑬其实他连脸书都不会用。",
    "6|Passage One": "⑭乱花钱它就电你，⑮255伏，⑯以后一切都联网，⑰人只买东西不看余额。",
    "6|Passage Two": "⑱避免误解的建议，⑲关键在用词的选择，⑳把感受和判断分开，㉑4条。",
    "6|Passage Three": "㉒防止吃太多的新方法，㉓换小餐具，㉔饭量降29%，㉕说到底是缺乏自控。",
}


def lcs(a, b):
    """最长公共子串长度，用来检查串记里有没有带上答案本身"""
    best = 0
    la, lb = len(a), len(b)
    prev = [0] * (lb + 1)
    for i in range(1, la + 1):
        cur = [0] * (lb + 1)
        for j in range(1, lb + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank.json')
    bank = json.load(open(path, encoding='utf-8'))
    used_single, used_group = set(), set()
    warn = []

    for s in bank:
        for q in s['questions']:
            key_g = '%d|%s' % (s['id'], q.get('group'))
            key_s = '%d-%d' % (s['id'], q['no'])
            if q.get('group') and key_g in GROUP:
                q['tip'] = GROUP[key_g]
                used_group.add(key_g)
            elif key_s in SINGLE:
                q['tip'] = SINGLE[key_s]
                used_single.add(key_s)
            else:
                warn.append('MISSING %s' % key_s)
                continue
            # 数字选项没有译文时补上数字本身，避免界面出现「—」
            azh = (q['options'][q['answer']]['zh'] or '').strip()
            if not azh:
                en = q['options'][q['answer']]['en'].strip().rstrip('.')
                if re.match(r'^[\d,]+$', en):
                    q['options'][q['answer']]['zh'] = en
                azh = q['options'][q['answer']]['zh']
            # 校验：串记里必须出现答案内容（≥2 字公共子串）
            core = re.sub(r'[。，、；：！？（）《》“”]', '', azh)
            n = lcs(core, q['tip'])
            need = 1 if len(core) <= 2 else 2
            if n < need:
                warn.append('WEAK %s  ans=%s  lcs=%d  tip=%s' % (key_s, azh, n, q['tip']))
            # 旧字段退役
            q.pop('tipL', None)
            q.pop('tipR', None)
            q['tipType'] = 'chain' if q.get('group') else 'hook'

    for k in SINGLE:
        if k not in used_single:
            warn.append('UNUSED single %s' % k)
    for k in GROUP:
        if k not in used_group:
            warn.append('UNUSED group %s' % k)

    json.dump(bank, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('单题钩子 %d 条，串记 %d 条，题数 %d' % (
        len(used_single), len(used_group), sum(len(s['questions']) for s in bank)))
    print('平均长度 %.1f 字' % (
        sum(len(q['tip']) for s in bank for q in s['questions']) /
        sum(len(s['questions']) for s in bank)))
    if warn:
        print('--- 需人工确认 %d 条 ---' % len(warn))
        for w in warn:
            print(' ', w)
    else:
        print('校验通过：每条串记都带上了对应答案')


if __name__ == '__main__':
    main()
