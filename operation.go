package main

//pythonで実行ファイルを生成、
//Goで実行ファイルを生成して、pythonの実行ファイルをGoの実行ファイルに渡す方が綺麗かな。

// #cgo pkg-config: python3
// #include <Python.h>
import "C"

import (
	"bufio"
	"fmt"
	"os"
)

func isSetting() bool {
	fmt.Println("初期設定を行います。初めて利用する方はyを押して下さい。")
	fmt.Print("y/n：")

	reader := bufio.NewReader(os.Stdin)
	ynFlag, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("入力エラー:", err)
		return false
	}

	ynFlag = ynFlag[:len(ynFlag)-1] // 改行文字を削除
	if ynFlag == "y" {
		fmt.Println("設定を始めます。")
		// 設定関数を呼ぶ
		return true
	} else if ynFlag == "n" {
		return true
	} else {
		fmt.Println("初期設定をする場合はy、初期設定をしない場合はnを押下して下さい。")
		return false
	}
}

func main() {
	fmt.Println("現新比較ツールの設定を始めます。")
	for {
		if isSetting() {
			break
		}
		fmt.Println()
	}

	fmt.Println("現新比較ツールを実行します。")

	defer C.Py_Finalize()
	C.Py_Initialize()
}
