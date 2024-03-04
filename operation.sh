#!/bin/bash

##設定ファイルを編集する。
is_setting() {
    echo "初期設定を行います。初めて利用する方はyを押して下さい。"
    read -p "y/n：" yn_flag
    if [ $yn_flag = "y" ]
    then
        echo "設定を始めます。"
        ##設定関数を呼ぶ。今は関数を作っていない。
        return 0
    elif [ $yn_flag = "n" ]
    then

        return 0
    else
        echo "初期設定をする場合はy、初期設定をしない場合はnを押下して下さい。"
        return 1
    fi
}

##ここからmain処理となる。

echo "現新比較ツールの設定を始めます。"

while :
do
    is_setting "$1"
    status=$?
    echo ""
    if [ $status = 0 ]
    then
        break
    fi
done

##ファイルアップロードを促す。

##現新比較のツールを実行する。

##ファイルダウンロードを促す。