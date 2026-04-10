import urllib.request
import urllib.parse
import json
import datetime
import os

API_KEY = os.environ.get('LAW_API_KEY', '')
KEYWORDS = ['어린이제품', '화장품', '위생용품', '원산지']
result = {}

for kw in KEYWORDS:
    params = urllib.parse.urlencode({
        'serviceKey': API_KEY,
        'query': kw,
        'numOfRows': '30',
        'pageNo': '1',
        'target': 'law',
        'type': 'XML'
    })
    url = f'http://apis.data.go.kr/1170000/law/lawSearchList.do?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        import xml.etree.ElementTree as ET
        with urllib.request.urlopen(req, timeout=20) as res:
            raw = res.read().decode('utf-8')
        root = ET.fromstring(raw)
        laws = []
        for item in root.findall('.//law'):
            laws.append({
                '법령명한글': item.findtext('법령명한글', ''),
                '법령구분명': item.findtext('법령구분명', ''),
                '소관부처명': item.findtext('소관부처명', ''),
                '공포일자':   item.findtext('공포일자', ''),
                '시행일자':   item.findtext('시행일자', ''),
                '법령상세링크': item.findtext('법령상세링크', 'https://www.law.go.kr'),
            })
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
