#!/bin/bash

echo "現新比較ツールの設定を始めます。"

##設定ファイルを編集する。
is_setting() {
    read -p "設定が必要な場合はyを押下して下さい。y/n：" yn_flag
    if [ $yn_flag = "y" ]
    then
        echo "設定を始めます。"
        ##設定関数を呼ぶ。今はコールできていない。
        return 0
    elif [ $yn_flag = "n" ]
    then
        echo "設定は行いません。"
        return 0
    else
        echo "設定をする場合はy、設定をしない場合はnを押下して下さい。"
        return 1
    fi
}

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