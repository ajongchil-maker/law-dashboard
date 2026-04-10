import urllib.request
import urllib.parse
import json
import datetime
import os

OC = os.environ['LAW_API_KEY']
KEYWORDS = ['어린이제품', '화장품', '위생용품', '원산지']
result = {}

for kw in KEYWORDS:
    url = (
        'https://www.law.go.kr/DRF/lawSearch.do'
        '?OC=' + OC +
        '&target=law'
        '&query=' + urllib.parse.quote(kw) +
        '&type=JSON'
        '&display=30'
        '&page=1'
        '&sort=date'
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            raw = res.read().decode('utf-8')
        print(f'[{kw}] 원문: {raw[:200]}')
        data = json.loads(raw)
        law_search = data.get('LawSearch', {})
        laws = law_search.get('law', [])
        if isinstance(laws, dict):
            laws = [laws]
        result[kw] = laws
        print(f'[{kw}] {len(laws)}건 수집 완료')
    except Exception as e:
        print(f'[{kw}] 오류: {e}')
        result[kw] = []

kst = datetime.timezone(datetime.timedelta(hours=9))
result['updated'] = datetime.datetime.now(kst).strftime('%Y-%m-%d %H:%M KST')
result['total'] = sum(len(v) for k, v in result.items() if k not in ('updated', 'total'))

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'완료: {result["updated"]} 총 {result["total"]}건')
