$Adapters = Get-WmiObject Win32_NetworkAdapterConfiguration | ? {$_.IPEnabled}
$PrimaryDns = $Adapters[0].DNSServerSearchOrder[0]
netsh interface ip set dns name="Local Area Connection" static 127.0.0.1
Invoke-Expression "netsh interface ip add dns name='Local Area Connection' $PrimaryDns index=2"
Clear-Host
If ($LASTEXITCODE -Eq 0) {
	"Successfully updated your system!"
} else {
	"Failed to update your system :("
	"You can revert and try again.."
}
