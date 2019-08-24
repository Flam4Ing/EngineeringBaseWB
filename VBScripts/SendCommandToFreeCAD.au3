If UBound(ProcessList("AutoIt3.exe")) > 2 Then
MsgBox(262144+16,"Error!",@ScriptName&" is already running!")
Exit 
Endif

Global $ipAdress
Global $ipPort

If $CmdLine[0] > 1 Then
    $ipAdress = $CmdLine[1]
    $ipPort = $CmdLine[2]
    
EndIf
;MsgBox(0, "", $ipAdress + $ipPort)

HotKeySet("{F5}", "NewDocument")

While 1
    Sleep(100)
WEnd


Func NewDocument()
	SendCommand("import DraftExtentions")
	SendCommand("DraftExtentions.PlaceOnDraftGrid().Activated('TS35')")
EndFunc

Func SendCommand($Fcmd)
	TCPStartup()
	$Socket = TCPConnect($ipAdress, $ipPort)
	TCPSend($Socket, $Fcmd)
	TCPCloseSocket($Socket)
	TCPShutdown()
EndFunc