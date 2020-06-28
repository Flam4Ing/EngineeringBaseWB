'Get Arguments
	scriptArg = WScript.Arguments.Count
	If scriptArg = 0 Then
		Msgbox ReadEBdeviceProperties()
	ElseIf scriptArg = 1 Then
		Folder = WScript.Arguments(0)
		deviceProperties = ReadEBdeviceProperties()
		'Call WriteToFile(Folder , deviceProperties)
		Call WriteToUTF8(Folder , deviceProperties)
'Test ohne EB installation
    ElseIf scriptArg = 2 Then
		'MsgBox "Test ohne EB installation"
		Folder = WScript.Arguments(0)
		deviceProperties = TestOhneEB()
		Call WriteToUTF8(Folder , deviceProperties)
	End If



Function ReadEBdeviceProperties ()
	On Error Resume Next
	'Create EB Object
		Set FSO = CreateObject("Scripting.FileSystemObject")
		Set oEb = CreateObject("AucEasylectric.AucApplication")	'EB Instantzieren
		Set ebShape = oEb.Selection(1)
	
	'Pruefen ob ein Gereat ist
		If ebShape.Kind <>113 Then
			MsgBox "Kein Gereat ausgewaelt!"
			ReadEBdeviceProperties = TestOhneEB()
			Exit Function
		End If
		
	'Pruefen ob eine Klemmleiste ist
		If ebShape.Attributes.ItemByID(7).Value = 137 Then
			terminalFullName = ebShape.FullName
			terminalName = ebShape.Name
			terminalID = ebShape.ID
			terminalDiscription = ebShape.Attributes.ItemByID(25)
			terminalCount = ebShape.Children.Count
			ReadEBdeviceProperties = terminalFullName & vbCrLf &_
						terminalName & vbCrLf &_
						"none" & vbCrLf &_
						"0" & vbCrLf &_
						"0" & vbCrLf &_
						"0" & vbCrLf &_
						terminalID & vbCrLf &_
						terminalDiscription & vbCrLf &_
						terminalCount & vbCrLf
			Exit Function
		End If
	'EBdevice Name
		deviceFullName = ebShape.FullName
		'deviceFullName = Replace(shapeName, "Geräte", "")
		deviceName = ebShape.Name
		deviceID = ebShape.ID
	'EBdevice description in germany
		deviceDiscription = ebShape.Attributes.ItemByID(100006)
	'Shape Dimension
		Breite = ebShape.Attributes.ItemByID(245)
		if Len(Breite) > 1 then
			Breite = Left(Breite, Len(Breite) - 6)
		else
			Breite = 0
		end if

		Hoehe = ebShape.Attributes.ItemByID(246)
		if Len(Hoehe) > 1 then
			Hoehe = Left(Hoehe, Len(Hoehe) - 6)
		else
			Hoehe = 0
		end if

		Tiefe = ebShape.Attributes.ItemByID(247)
		if Len(Tiefe) > 1 then
			Tiefe = Left(Tiefe, Len(Tiefe) - 6)
		else
			Tiefe = 0
		end if

	'Shape STEP File (Filepath is in Attribut -Bauform-)
		StepFile = ebShape.Attributes.ItemByID(10296)
		if Len(StepFile) < 1 then
			StepFile = "None"
		end if
	ReadEBdeviceProperties = deviceFullName & vbCrLf &_
						deviceName & vbCrLf &_
						StepFile & vbCrLf &_
						Breite & vbCrLf &_
						Hoehe & vbCrLf &_
						Tiefe & vbCrLf &_
						deviceID & vbCrLf &_
						deviceDiscription& vbCrLf &_
						"1"
	'Fehlerauswertung
	if err.number <> 0 then 
		ReadEBdeviceProperties = TestOhneEB()

        MsgBox "Connect to EB Failure: " & err.number & "- " & err.description
		err.Clear
	end if
End Function


Function WriteToFile(pathToFolder , txtString)
	txtFile = pathToFolder & "\ExportedDeviceEBANSI.txt"
	Set FSO = CreateObject("Scripting.FileSystemObject")
	Set File = FSO.CreateTextFile(txtFile,True)
	File.Write txtString
	File.Close
	WriteToFile = True
End Function

Function WriteToUTF8(pathToFolder , txtString)
	txtFile = pathToFolder & "\ExportedDeviceEB.txt"
	Set objStream = CreateObject("ADODB.Stream")
	objStream.CharSet = "utf-8"
	objStream.Open
	objStream.WriteText txtString
	objStream.SaveToFile txtFile, 2
End Function



Function TestOhneEB()
	TestOhneEB = "+TEST DEVICE#-K31.00" & vbCrLf &_
				"-K31.00" & vbCrLf &_
				"C:\Users\heinrich\Desktop\FreeCAD18\Mod\!EngineeringBase\TerminalBlocks\S200.step" & vbCrLf &_
				"33" & vbCrLf &_
				"100" & vbCrLf &_
				"120" & vbCrLf &_
				"00000000-0000-0000-0000-000004A397A3" & vbCrLf &_
				"CPU340-20 Ethernet+CANopen" & vbCrLf &_
				"1"
End Function








