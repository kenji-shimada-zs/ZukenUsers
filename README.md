# 目的
Zuken CR8000で使用中のライセンス一覧と使用中ユーザーの名称を
一覧表示したい。
# 実行環境
AD参加済み

# build方法
PDFMergeのディレクトリで以下のコマンドを実行 (実行するPython環境にはpypdf,pyinstaller)をインストール済みの事 ※pathlibはpyinstallerのビルドに対してバージョンの制約があるので ビルドに失敗する時はpip uninstallでpathlibを取り除いてから実行する事 生成されたファイルはdist以下に.exeファイルが作成される。

pyinstaller UserList.py --onefile --exclude pip