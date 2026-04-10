Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\AbiodunFagbuaro\OneDrive - Architech\Desktop\Ergo"
WshShell.Run """C:\Users\AbiodunFagbuaro\AppData\Local\Programs\Python\Python314\python.exe"" ergo.py", 0, False
