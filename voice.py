from nonebot import MessageSegment, NoneBot
from hoshino import Service, priv
from hoshino.typing import CQEvent
from typing import Dict, Union

import aiohttp, base64, time, random, hashlib

help = '''[角色]说[语言] [文本]：合成自定义语言
例如：宁宁说日文 はじめまして
[语言]语言帮助：查看可用角色
例如：中文语言帮助

语言分类：
- 译文：输入中文自动翻译成日语
- 日语：纯日语，尽量输入假名
- 日文：纯日语，尽量输入假名
- 韩语：纯韩语
- 中文：原神语音'''

sv = Service('模拟语音', manage_priv=priv.ADMIN, enable_on_default=True, help_=help)

ALLModel: Dict[str, Dict[str, str]] = {
    'tolove': {'小暗': '金色の闇', '茉茉': 'モモ', '娜娜': 'ナナ', '美柑': '結城美柑', '唯': '古手川唯', '芽亚': '黒咲芽亜', '涅墨西斯': 'ネメシス', '静': '村雨静', '希莉奴': 'セリーヌ', '菈菈': 'ララ', '沙姫': '天条院沙姫', '春菜': '西連寺春菜', 'ルン': 'ルン', '芽衣': 'メイ', '恭子': '霧崎恭子', '里纱': '籾岡里紗', '未央': '沢田未央',
            '提亚悠': 'ティアーユ', '九条凛': '九条凛', '藤崎绫': '藤崎綾', '结城华': '結城華', '涼子': '御門涼子', 'アゼンダ': 'アゼンダ', '梨子': '夕崎梨子', '梨斗': '結城梨斗', '佩凯': 'ペケ', '健一': '猿山ケンイチ', 'レン': 'レン', '校长': '校長'},
    'yuzu': {'宁宁': '綾地寧々', '爱瑠': '因幡めぐる', '芳乃': '朝武芳乃', '茉子': '常陸茉子', '丛雨': 'ムラサメ', '小春': '鞍馬小春', '七海': '在原七海'},
    'zero': {},
    'sora': {'穹': '春日野穹', '瑛': '天女目瑛', '奈绪': '依媛奈緒', '一叶': '渚一葉'},
    'dracu': {'美羽': '矢来美羽', '梓': '布良梓', '艾莉娜': 'エリナ', '莉音': '稲丛莉音', '尼古拉': 'ニコラ', '小夜': '荒神小夜', '夕里': '大房ひよ里', '萌香': '淡路萌香', '安娜': 'アンナ', '直太': '倉端直太', '兵马': '枡形兵馬', '元树': '扇元樹'},
    'stella': {'夏目': '四季ナツメ', '栞那': '明月栞那', '希': '墨染希', '爱衣': '火打谷愛衣', '凉音': '汐山涼音' },
    'mangekyo': {'莲华': '蓮華', '雾枝': '篝ノ霧枝', '雫': '沢渡雫', '灯露椎': '灯露椎', '夕莉': '覡夕莉'},
    'hamidashi': {'姬爱': '和泉妃愛', '华乃': '常盤華乃', '日海': '錦あすみ', '诗音': '鎌倉詩桜', '天梨': '竜閑天梨', '和泉里': '和泉里', '广梦': '新川広夢', '莉莉子': '聖莉々子'}
}
KR = {'Sua': 0, 'Mimiru': 1, 'Arin': 2, 'Yeonhwa': 3, 'Yuhwa': 4, 'Seonbae': 5}
CN = ['派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶', '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉',
    '优菈', '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗', '甘雨', '七七', '刻晴', '神里绫华', '雷泽', '神里绫人',
    '罗莎莉亚', '阿贝多', '八重神子', '宵宫', '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎', '达达利亚', '莫娜', 
    '班尼特', '申鹤', '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云', '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏']
XCW = ['xcw', '小仓唯', '镜华']

Model = []
VoiceList = []
for k in list(ALLModel.keys()):
    Model.append(k)
    for i in list(ALLModel[k].keys()):
        VoiceList.append(i)

VoiceAPI = 'http://106.53.138.218:6321/api/voice'
MoeGoeAPI = 'https://moegoe.azurewebsites.net/api/'
GenshinAPI = 'http://233366.proxy.nscc-gz.cn:8888'
XcwAPI = 'http://prts.tencentbot.top/0/'
TranslateAPI = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

class Error(Exception):

    def __init__(self, args: object) -> None:
        self.error = args

async def voiceApi(api: str, params: Union[str, dict] = None) -> str:
    async with aiohttp.request('GET', api, params=params) as resp:
        if resp.status == 200:
            data = await resp.read()
        else:
            raise Error(resp.status)
    return 'base64://' + base64.b64encode(data).decode()

@sv.on_prefix([i + '说韩语' for i in KR.keys()])
@sv.on_prefix([i + '说' + n for i in VoiceList for n in ('译文', '日语', '日文')])
@sv.on_prefix([i + '说中文' for i in CN])
@sv.on_prefix([i + '说日语' for i in XCW])
async def voice(bot: NoneBot, ev: CQEvent):
    try:
        text: str = ev.message.extract_plain_text().strip()
        if not text:
            await bot.send(ev, '请输入需要合成语音的文本', at_sender=True)
            return
        preid: str = ev.prefix[:-3]
        prelang: str = ev.prefix[-2:]
        if prelang == '中文':
            voice = await voiceApi(GenshinAPI, {'speaker': preid, 'text': text, 'length': 1.0})
        elif prelang == '韩语':
            lang = 'speakkr'
            id = KR[preid]
            voice = await voiceApi(MoeGoeAPI + lang, {'id': id, 'text': text})
        else:
            if prelang == '译文':
                text = await translate(text)
            if preid in XCW:
                voice = await voiceApi(XcwAPI + text)
            elif preid in VoiceList:
                for model, name in ALLModel.items():
                    if preid in name:
                        models = model
                        break
                voice = await voiceApi(VoiceAPI, {'model': models, 'speaker': preid, 'text': text})
            else:
                raise Error()
        data = MessageSegment.record(voice)
    except Error as e:
        data = f'发生错误：{e.error}'
        sv.logger.error(data)
    except Exception as e:
        data = f'发生错误：{e}'
        sv.logger.error(data)

    await bot.send(ev, data)

@sv.on_suffix('语言帮助')
async def voicehelp(bot: NoneBot, ev: CQEvent):
    args = ev.message.extract_plain_text().strip()
    if not args:
        return
    if args == '日文' or args == '译文' or args == '日语':
        data = VoiceList
        for i in XCW:
            data.append(i)
    elif args == '中文':
        data = CN
    elif args == '韩语':
        data = [i for i in KR.keys()]
    else:
        return
    await bot.send(ev, '可使用的角色名：\n' + '|'.join(data))


async def translate(text: str) -> str:
    lts = str(int(time.time() * 1000))
    salt = lts + str(random.randint(0, 9))
    sign_str = 'fanyideskweb' + text + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
    m = hashlib.md5()
    m.update(sign_str.encode())
    sign = m.hexdigest()

    headers = {
        'Referer': 'https://fanyi.youdao.com/',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1124603977@10.108.162.139; JSESSIONID=aaamH0NjhkDAeAV9d28-x; OUTFOX_SEARCH_USER_ID_NCOO=1827884489.6445506; fanyi-ad-id=305426; fanyi-ad-closed=1; ___rl__test__cookies=1649216072438',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    data = {
        'i': text,
        'from': 'zh-CHS',
        'to': 'ja',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': 'a0d7903aeead729d96af5ac89c04d48e',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }

    async with aiohttp.request('POST', TranslateAPI, headers=headers, data=data) as resp:
        response = await resp.json()

    return response['translateResult'][0][0]['tgt']