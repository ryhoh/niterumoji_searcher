#!/bin/sh

# 色設定
bg="black"
fg="white"

# フォント設定
# font="/System/Library/Fonts/Menlo.ttc"
font="/Users/tetsuya/Library/Fonts/unifont-13.0.03.ttf"
#font="/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
fontsize="18"

# 出力ファイル名
outfile="$1"

if [ "$1." == "." ]; then
outfile="text.png"
fi

# 変換
convert -background $bg -bordercolor $bg -fill $fg -font "$font" \
    -pointsize $fontsize -gravity North \
    -extent 28x28 \
    label:@- $outfile
