param(
    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]]$HtmlFiles
)

$Columns = @("Date", "Open", "High", "Low", "Close", "Adj Close", "Volume")
$SplitDate = "Aug 25, 2022"

function Convert-CellText {
    param([string]$Html)

    $text = [regex]::Replace($Html, "<[^>]+>", "")
    $text = [System.Net.WebUtility]::HtmlDecode($text)
    $text = [regex]::Replace($text, "\s+", " ").Trim()
    return $text
}

function Quote-CsvValue {
    param([string]$Value)

    return '"' + $Value.Replace('"', '""') + '"'
}

foreach ($HtmlFile in $HtmlFiles) {
    $InputPath = Resolve-Path -LiteralPath $HtmlFile
    $Html = Get-Content -LiteralPath $InputPath -Raw -Encoding UTF8
    $SplitPresent = $Html.Contains("3:1") -and $Html.Contains("Stock Splits") -and $Html.Contains($SplitDate)
    $Rows = New-Object System.Collections.Generic.List[string]

    $Rows.Add(($Columns -join ","))

    foreach ($RowMatch in [regex]::Matches($Html, "<tr\b[^>]*>(.*?)</tr>", "Singleline")) {
        $Cells = @()
        foreach ($CellMatch in [regex]::Matches($RowMatch.Groups[1].Value, "<t[dh]\b[^>]*>(.*?)</t[dh]>", "Singleline")) {
            $Cells += Convert-CellText $CellMatch.Groups[1].Value
        }

        if ($Cells.Count -ne $Columns.Count) {
            continue
        }
        if ($Cells[0] -eq "Date") {
            continue
        }
        if ($SplitPresent -and $Cells[0] -eq $SplitDate) {
            continue
        }

        $VolumeText = $Cells[6].Replace(",", "")
        $Volume = 0L
        if (-not [long]::TryParse($VolumeText, [ref]$Volume)) {
            continue
        }

        $Rows.Add((
            (Quote-CsvValue $Cells[0]),
            $Cells[1],
            $Cells[2],
            $Cells[3],
            $Cells[4],
            $Cells[5],
            $Volume
        ) -join ",")
    }

    $CsvPath = [System.IO.Path]::ChangeExtension($InputPath.Path, ".csv")
    [System.IO.File]::WriteAllLines($CsvPath, $Rows, [System.Text.UTF8Encoding]::new($false))
    Write-Output "$($InputPath.Path) -> $CsvPath"
}
