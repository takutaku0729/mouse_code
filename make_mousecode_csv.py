import MeCab
import jaconv
import pandas as pd
import unicodedata

def main():
    txtf = open('datas\make_GPT_dataset\data001.txt', encoding = "utf-8", mode = 'r')
    tagger = MeCab.Tagger("-Oyomi") #読み変換タグ
    sentence_list = txtf.readlines()    #文リスト作成
    csv_out = open('datas\make_GPT_dataset\data001.csv', encoding = "utf-8", mode = 'w') #csv出力ファイル
    csv_out.write("scentence,mousecode\n")
    for sentence in sentence_list:  #1文ずつ処理
        s_kana = jaconv.kata2hira(tagger.parse(sentence)) #かな変換
        s_kana = unicodedata.normalize("NFKC",s_kana)
        mcode = ''  #文字コード
        prev_mcode = '' #前文字コード参照用
        for n in range(len(s_kana)):  #1文字ずつ処理
            if s_kana[n] in "ゃゅょぁぃぅぇぉ":   #前文字コード参照が必要な変換
                prev_mcode = encoder(s_kana[n-1:n])
            else:
                mcode += prev_mcode
                prev_mcode = encoder(s_kana[n])
        mcode += prev_mcode

        #変換規則適用
        mcode=mcode.replace("A-^","A-A")#exrule
        mcode=mcode.replace("I-^","I-I")#exrule
        mcode=mcode.replace("U-^","U-U")#exrule
        mcode=mcode.replace("E-^","E-E")#exrule
        mcode=mcode.replace("O-^","O-O")#exrule
        mcode=mcode.replace("*X","X-")#rule3
        mcode=mcode.replace("E-*","E-I")#rule4
        mcode=mcode.replace("A-*","A-I")#rule4
        mcode=mcode.replace("O-*","O-I")#rule5
        mcode=mcode.replace("I-*","I")#rule6
        mcode=mcode.replace("U-*","U")#rule6

        #export
        csv_out.write(mcode +"," + sentence.strip() + "\n")

    csv_out.close()
    txtf.close()


def encoder(str):
    CODE = {
        "あ":"-A","か":"-A","は":"-A","が":"-A",
        "さ":"IA","た":"IA","な":"IA","や":"IA","ら":"IA","ざ":"IA","だ":"IA","きゃ":"IA","しゃ":"IA","ちゃ":"IA","にゃ":"IA","ひゃ":"IA","りゃ":"IA","ぎゃ":"IA","じゃ":"IA",
        "わ":"UA","ふぁ":"UA",
        "ま":"XA","ば":"XA","ヴぁ":"XA","ぱ":"XA","みゃ":"XA","びゃ":"XA","ぴゃ":"XA",
        "い":"-I","き":"-I","し":"-I","ち":"-I","に":"-I","ひ":"-I","り":"-I","ぎ":"-I","じ":"-I","ぢ":"-I",
        "うぃ":"UI","ふぃ":"UI",
        "み":"XI","び":"XI","ヴぃ":"XI","ぴ":"XI",
        "う":"-U","く":"-U","す":"-U","つ":"-U","ぬ":"-U","ふ":"-U","ゆ":"-U","る":"-U","ぐ":"-U","ず":"-U","づ":"-U","きゅ":"-U","しゅ":"-U","ちゅ":"-U","にゅ":"-U","ひゅ":"-U","りゅ":"-U","ぎゅ":"-U","じゅ":"-U",
        "む":"XU","ぶ":"XU","ヴ":"XU","ぷ":"XU","みゅ":"XU","びゅ":"XU","ぴゅ":"XU",
        "え":"-E","け":"-E","へ":"-E","げ":"-E",
        "せ":"IE","て":"IE","ね":"IE","れ":"IE","ぜ":"IE","で":"IE","きぇ":"IE","しぇ":"IE","ちぇ":"IE","にぇ":"IE","ひぇ":"IE","りぇ":"IE","ぎぇ":"IE","じぇ":"IE",
        "うぇ":"UE","ふぇ":"UE",
        "め":"XE","べ":"XE","ヴぇ":"XE","ぺ":"XE","みぇ":"XE","びぇ":"XE","ぴぇ":"XE",
        "お":"-O","こ":"-O","ほ":"-O","ご":"-O",
        "そ":"UO","と":"UO","の":"UO","よ":"UO","ろ":"UO","を":"UO","ぞ":"UO","ど":"UO","きょ":"UO","しょ":"UO","ちょ":"UO","にょ":"UO","ひょ":"UO","りょ":"UO","ぎょ":"UO","じょ":"UO","ふぉ":"UO",
        "も":"XO","ぼ":"XO","ヴぉ":"XO","ぽ":"XO","みょ":"XO","びょ":"XO","ぴょ":"XO",
        "っ":"-*","ん":"-*",
        "ー":"-^","\n":"",
        "、":" ","。":" ","・":" "
    }
    if str in CODE:
        return CODE[str]
    else:
        return ""


if __name__ == '__main__':
    main()
    