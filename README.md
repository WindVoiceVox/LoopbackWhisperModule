# Name

LoopbackWhisperModule

Whisperとsoundcardモジュールを連携させて、現在PCで再生中の音声を文字起こしする。

# DEMO

LoopbackWhisperModuleオブジェクトを作成して、loop()を呼び出します。
LoopbackWhisperModuleはsoundcardモジュールを通して現在再生中の音声を取得し、文字起こしします。
文字起こしした結果はターミナルに表示されます。

loop()を呼び出した後は制御が戻らないので、終了するにはターミナルでCtrl+Cをしてください。

```python
from LoopbackWhisperModule import LoopbackWhisperModule

lwm = LoopbackWhisperModule()
lwm.loop()
```

# Requirement

- whisper
- soundcard

# Installation

通常通りpipでインストールできます。

You can install with pip as usual.

```bash
pip install git+https://github.com/WindVoiceVox/LoopbackWhisperModule
```

# Note

このモジュールは [TadaoYamaoka / LoopbackWhisper](https://github.com/TadaoYamaoka/LoopbackWhisper)をクラスにしたものです

# Author

WindVoice

# License

LoopbackWhisperModule is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
