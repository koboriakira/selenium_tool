# プロセスが終了しないように無限ループする
# このプロセスは、systemdのサービスとして起動される
import time

while True:
    time.sleep(60)
