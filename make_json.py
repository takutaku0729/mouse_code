import MeCab
import jaconv
import pandas as pd

def main():
    ita_csv = open('datas\make_GPT_dataset\data001.txt', encoding = "utf-8", mode = 'r')

    line = ita_csv.readline()
    
    tagger = MeCab.Tagger("-OAlign")    

    sentence_list = ita_csv.readlines()
    num = 0
    for sentence in sentence_list:
        num = num + 1
        align_out = open('dataset/nucc/nucc_v2_mc_align/' + str(num) + '.align', encoding = "utf-8", mode = 'w')
        sentence = sentence[0:-1]
        sentence_parced = jaconv.kata2hira(tagger.parse(sentence)).splitlines()

        for line in sentence_parced:
            line_buf = ''
            prev_code = ''
            for n in range(len(line)):
                if line[n] in "ゃゅょぁぃぅぇぉ":
                    prev_code = encoder(line[n-1:n])
                else:
                    line_buf += prev_code
                    prev_code = encoder(line[n])
            line_buf += prev_code

            line_buf=line_buf.replace("A-^","A-A")#exrule
            line_buf=line_buf.replace("I-^","I-I")#exrule
            line_buf=line_buf.replace("U-^","U-U")#exrule
            line_buf=line_buf.replace("E-^","E-E")#exrule
            line_buf=line_buf.replace("O-^","O-O")#exrule
            line_buf=line_buf.replace("*X","X-")#rule3
            line_buf=line_buf.replace("E-*","E-I")#rule4
            line_buf=line_buf.replace("A-*","A-I")#rule4
            line_buf=line_buf.replace("O-*","O-I")#rule5
            line_buf=line_buf.replace("I-*","I")#rule6
            line_buf=line_buf.replace("U-*","U")#rule6

            for c in range(len(line_buf)):
                align_out.write(line_buf[c])#ファイル出力
                if c%2 != 0:
                    align_out.write(" ")
            align_out.write("\n")

        align_out.close()

    ita_csv.close()


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
        "ー":"-^",
        "":""
    }
    return CODE[str]


if __name__ == '__main__':
    main()
    