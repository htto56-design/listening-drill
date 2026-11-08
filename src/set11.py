# -*- coding: utf-8 -*-
"""第 11 套 · 城市（Cities Unit 5），Section A 长对话 4 题 + Section B 短文 3 题。"""
import json, os, re

def Q(no, ans, opts):
    return {"no": no, "answer": ans,
            "options": {k: {"en": v[0], "zh": v[1]} for k, v in zip("ABCD", opts)}}

SET = {
    "id": 11, "title": "第11套", "topic": "城市生活",
    "tips": {
        "Conversation One": "①聊的是在大城市生活，②房东要涨房租，"
                            "③劝他少下馆子少点外卖，④图的还是工作机会多。",
        "Passage One": "⑤通篇是西安简介，⑥兵马俑近 9,000，⑦当年是全球人口最多的城市。",
    },
    "questions": [
        Q(1, "C", [
            ("Living expenses in London.", "伦敦的生活开支"),
            ("Traffic jams in London.", "伦敦的交通拥堵"),
            ("Living in big cities.", "在大城市生活"),
            ("Pollution in London.", "伦敦的污染"),
        ]),
        Q(2, "B", [
            ("Jane wanted the landlord to reduce the rent.", "简希望房东降房租"),
            ("The landlord wanted to increase the rent.", "房东想涨房租"),
            ("The landlord wanted Jane to move.", "房东想让简搬走"),
            ("Jane wanted to move.", "简想搬家"),
        ]),
        Q(3, "C", [
            ("He should take the tube instead of riding a bicycle.", "他该坐地铁，别骑自行车"),
            ("He should find an apartment near Hyde Park Corner.", "他该在海德公园角附近找房子"),
            ("He should cut the expenses on dining out and takeaways.", "他该削减下馆子和点外卖的开销"),
            ("He should find a high-paying job.", "他该找份高薪工作"),
        ]),
        Q(4, "D", [
            ("It is cheaper to live in a big city.", "在大城市生活更便宜"),
            ("There are fewer environmental problems.", "环境问题更少"),
            ("The traffic is less heavy.", "交通没那么拥堵"),
            ("There are more job opportunities.", "工作机会更多"),
        ]),
        Q(5, "B", [
            ("A brief introduction to Qin Shi Huang.", "秦始皇简介"),
            ("A brief introduction to Xi'an.", "西安简介"),
            ("The story of terracotta troops.", "兵马俑的故事"),
            ("The religions in Xi'an.", "西安的宗教"),
        ]),
        Q(6, "B", [
            ("About 2,200.", "约 2,200"),
            ("Almost 9,000.", "近 9,000"),
            ("Around 700,000.", "约 700,000"),
            ("About 10,000.", "约 10,000"),
        ]),
        Q(7, "C", [
            ("It became the religious center of Islam.", "它成了伊斯兰教的宗教中心"),
            ("It was linked to West and Central Asia.", "它与西亚、中亚相连"),
            ("It became the most populous city in the world.", "它成了世界上人口最多的城市"),
            ("It had the largest mosque in the world.", "它有世界上最大的清真寺"),
        ]),
    ],
}


def lcs(a, b):
    best = 0
    for i in range(len(a)):
        for j in range(i + 2, len(a) + 1):
            if a[i:j] in b:
                best = max(best, j - i)
            else:
                break
    return best


def build(spec):
    qs = []
    for q in spec["questions"]:
        if q["no"] <= 4:
            grp, rng, sec = "Conversation One", [1, 4], "A"
        else:
            grp, sec = "Passage One", "B"
            rng = [5, len(spec["questions"])]
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
    bank = [s for s in bank if s["id"] != 11]
    st = build(SET)
    bank.append(st)
    bank.sort(key=lambda s: s["id"])

    warn = []
    for q in st["questions"]:
        core = re.sub(r"[。，、；：！？（）《》“”%]", "", q["options"][q["answer"]]["zh"])
        need = 1 if len(core) <= 2 else 2
        if lcs(core, q["tip"]) < need:
            warn.append("WEAK %d-%d %s" % (st["id"], q["no"], core))

    json.dump(bank, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    total = sum(len(s["questions"]) for s in bank)
    print("sets", len(bank), "questions", total)
    for q in st["questions"]:
        print("  Q%-2d %s  %s" % (q["no"], q["answer"], q["options"][q["answer"]]["zh"]))
    print("warn", warn if warn else "none")


if __name__ == "__main__":
    main()
