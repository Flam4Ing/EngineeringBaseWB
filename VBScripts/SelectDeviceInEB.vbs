'Get Arguments
	On Error Resume Next
	scriptArg = WScript.Arguments.Count

	If scriptArg = 0 Then
		Msgbox "Test"
'Select EB device
	ElseIf scriptArg = 1 Then
		OID = WScript.Arguments(0)
'Create EB Object
		Set oEb = CreateObject("AucEasylectric.AucApplication")	'EB Instantzieren
		Set device = oEb.Utils.GetSnglObjectByID(OID)
		Call oEb.Utils.ExecuteCommand(57092, device)
'Test ohne EB installation	
	ElseIf scriptArg = 2 Then
		OID = WScript.Arguments(0)
        Msgbox OID
	End If

	if err.number <> 0 then 
		ReadEBdeviceProperties = err.number & ": " & err.description
		err.Clear
	end if