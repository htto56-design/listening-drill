# -*- coding: utf-8 -*-
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
bank = json.load(open(os.path.join(HERE, 'bank_raw.json'), encoding='utf-8'))

def has_digit_start(s):
    return bool(re.match(r'^\s*[\$€£]?\d', s))

def classify(q):
    o = [q['options'][k]['en'] for k in 'ABCD']
    if sum(1 for x in o if has_digit_start(x)) >= 3: return 'number'
    if sum(1 for x in o if x.lower().startswith('because')) >= 2: return 'reason'
    if sum(1 for x in o if re.match(r'^To\s+[a-z]', x)) >= 2: return 'purpose'
    if sum(1 for x in o if re.match(r'^[A-Z][a-z]+\s+and\s+[a-z]+', x)) >= 2: return 'relation'
    if sum(1 for x in o if re.search(r'\b(thinks?|believes?|likes?|prefers?|agrees?|should)\b', x, re.I)) >= 2: return 'attitude'
    if sum(1 for x in o if re.match(r'^(In|At|On|During)\b', x)) >= 2: return 'timeplace'
    if sum(1 for x in o if len(x.split()) <= 4) >= 3: return 'short'
    return 'detail'

T = {
'number': [
 "数字题只记「数字 + 单位」两件事：听到 five minutes 立刻写 5min，别在心里翻译。答案 {ans} 就是这组数字，其余三项多是近音干扰（15/50、$8/$18）。",
 "先把四个选项的数字按大小排序，听的时候只判断「大中小」三档，命中区间再回头核对。本题落在 {ans}，锚点是 {zh}。",
 "时间/价格题最怕记混，听写时用符号代替汉字：5:00 A.M. 写成「5↑」。答案 {ans} = {zh}，先锁数字再对单位。",
 "这类题常设「同数不同单位」的坑：分钟 vs 小时、美元 vs 美分。听清单位再选，答案 {ans}（{zh}）单位是完整的。",
 "别被开头数字带走——真正的数字往往在 but / actually 之后。本题答案 {ans}：{zh}，记住这个落点即可。",
],
'reason': [
 "原因题听到 because / due to / that's why 就要停笔，答案基本紧跟其后。本题 {ans} 项就是那句原因的复述：{zh}。",
 "四个选项都以 Because 开头时，先砍掉和说话人态度相反的两项，剩下两项再听「是谁的原因」。答案 {ans}：{zh}。",
 "听力里的原因常藏在语气转折后：先抱怨、再解释。锁定 {ans}，锚点「{zh}」——听到对应表达就选它。",
 "原因题不要逐词翻译，只抓「因为什么」这个名词性核心。本题核心是「{zh}」，对应选项 {ans}。",
 "若听到两个原因，选「直接原因」而不是背景原因。答案 {ans}（{zh}）是说话人当场给出的那一个。",
],
'purpose': [
 "目的题先看动词不定式 To... 的动词，四个选项的动词往往互不相同，听清动作就赢一半。答案 {ans}：{zh}。",
 "To 开头的选项最容易混，把每项缩成一个中文动词（保护/阻止/鼓励），听到哪个动作选哪个。本题是 {ans} → {zh}。",
 "目的题常以 What's the purpose / Why does he... 提问，答案多在段落开头或结尾一句。锁定 {ans}（{zh}）。",
 "先排除「太绝对」的选项（the most / all over the world），答案通常克制。本题 {ans}：{zh}。",
 "听到 in order to / so as to / so that 就是答案区，紧随其后的动作即选项。答案 {ans} = {zh}。",
],
'relation': [
 "身份关系题先定场景（餐厅/机场/学校/医院），再定尊卑：服务员对顾客、老师对学生。答案 {ans}：{zh}。",
 "四个选项都是「A and B」，只要听出其中一方身份就能反推。本题女方是顾客，所以选 {ans}（{zh}）。",
 "关系题的关键是称呼语和语气：Could I have... 是顾客，Can I help you 是服务方。答案 {ans}：{zh}。",
 "别被性别词骗了：he/she 在听力里常吞音，靠职业名词判断更稳。本题 {ans} = {zh}。",
 "场景词是硬线索：menu→餐厅，boarding→机场，prescription→医院。本题场景对应 {ans}（{zh}）。",
],
'attitude': [
 "态度题只信转折词后面的内容：but / actually / to be honest 之后才是真心话。答案 {ans}：{zh}。",
 "四个选项主语不同（he/she/the woman），先分清是谁在评价，再判正负。本题评价者是题目里的人，答案 {ans}（{zh}）。",
 "含 should / shouldn't 的选项通常是建议类答案，听到 had better / why don't you 就对应上。本题 {ans}：{zh}。",
 "否定态度的表达很委婉：not really / I'm afraid / that's not quite...，听到就当「不支持」。答案 {ans}（{zh}）。",
 "先给四个选项标 +/−，听的时候只需判断正负，两个同号的直接排除。本题为 {ans}：{zh}。",
],
'timeplace': [
 "时间地点题先记「最晚出现的那个」，听力习惯把更正信息放在后面。答案 {ans}：{zh}。",
 "In/At/On 开头的选项先看介词：具体时刻用 at，年月用 in，星期用 on，语法也能帮你排除。本题 {ans}（{zh}）。",
 "地点题抓场景名词即可，不必听懂整句。本题落点 {ans} = {zh}。",
 "时间题注意「提前/推迟」两个动词：earlier / put off，方向反了答案就反。本题 {ans}：{zh}。",
 "若听到两个地点，选「最后决定要去」的那个。答案 {ans}（{zh}）。",
],
'short': [
 "短选项题靠「同义替换」得分：原文用一个词，选项换另一个词。答案 {ans}：{zh}，就是这个替换关系。",
 "四个选项都极短时，考的是细节词而不是理解，听到哪个选哪个，别过度推理。本题 {ans}（{zh}）。",
 "短选项常是数字、名词或动作，先在心里给每项配一个中文词，听到即刻匹配。答案 {ans} = {zh}。",
 "这类题干扰项往往也在原文出现过，但搭配错了。认准 {ans}（{zh}）这个完整搭配。",
 "把选项读一遍再听，大脑会自动「点亮」听到的词。本题点亮的是 {ans}：{zh}。",
],
'detail': [
 "细节题先看选项重复的部分，重复越多越可能是同义改写。答案 {ans}：{zh}。",
 "长选项先砍掉后半句相同的部分，只比较差异点，差异点就是考点。本题差异落在 {ans}（{zh}）。",
 "听到与选项「一模一样」的原文反而要小心，正确答案多为改写。本题 {ans}：{zh}。",
 "这题考「谁做了什么」，先把主语钉死，再看动作。答案 {ans}（{zh}）。",
 "实在没听清就用排除法：与常识冲突的、太绝对的先划掉。本题 {ans}：{zh}。",
],
}

def short_zh(s, n=22):
    s = re.sub(r'[。，、；：！？,.;:!?"“”]', '', s or '')
    return s[:n] if s else ''

def num_zh(en):
    e = en.strip().rstrip('.')
    m = re.match(r'^\$([\d,.]+)$', e)
    if m: return f'{m.group(1)} 美元'
    m = re.match(r'^([\d.]+)%$', e)
    if m: return f'百分之 {m.group(1)}'
    m = re.match(r'^(\d{1,2}):(\d{2})\s*(A\.M\.|P\.M\.)?$', e, re.I)
    if m:
        ap = ' 凌晨/上午' if (m.group(3) or '').lower() == 'a.m.' else (' 下午/晚上' if (m.group(3) or '').lower() == 'p.m.' else '')
        return f'{m.group(1)} 点 {m.group(2)} 分{ap}'
    m = re.match(r'^(19|20)\d{2}$', e)
    if m: return f'{e} 年'
    return ''

cnt = {}
for s in bank:
    for q in s['questions']:
        cat = classify(q)
        cnt[cat] = cnt.get(cat, 0) + 1
        q['type'] = cat
        zh = q['options'][q['answer']]['zh'] or num_zh(q['options'][q['answer']]['en'])
        pool = T[cat]
        idx = (s['id'] * 7 + q['no'] * 3) % len(pool)
        tpl = pool[idx]
        zhx = short_zh(zh) or q['options'][q['answer']]['en']
        q['tip'] = tpl.format(ans=q['answer'], zh=zhx)
        # 选项乱序时要把「答案 X」换成界面上的新字母：预先切出字母两侧的文本
        pre, post = tpl.split('{ans}')
        q['tipL'] = pre.format(zh=zhx)
        q['tipR'] = post.format(zh=zhx)
        for k in 'ABCD':
            if not q['options'][k]['zh']:
                q['options'][k]['zh'] = num_zh(q['options'][k]['en'])
        # 中文关键词（用于答案卡高亮）
        q['key'] = short_zh(zh)

json.dump(bank, open(os.path.join(HERE, 'bank.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(cnt)
print(sum(len(s['questions']) for s in bank), '题')
for q in bank[0]['questions'][:3]:
    print(q['no'], q['type'], '|', q['tip'])
print(json.dumps(bank[4]['questions'][15], ensure_ascii=False, indent=1)[:600])
