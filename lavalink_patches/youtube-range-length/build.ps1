param([Parameter(Mandatory=$true)][string]$JdkDirectory)
$ErrorActionPreference = 'Stop'
$project = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$build = Join-Path $project '.tmp/youtube-range-build'
$lib = Join-Path $build 'lib'
$classes = Join-Path $build 'classes'
New-Item -ItemType Directory -Force $lib,$classes | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead((Join-Path $project 'Lavalink.jar'))
try {
    foreach($entry in $archive.Entries) {
        if($entry.FullName -like 'BOOT-INF/lib/*.jar') {
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry,(Join-Path $lib $entry.Name),$true)
        }
    }
} finally { $archive.Dispose() }
$plugin = Join-Path $project 'plugins/youtube-plugin-1.18.2.jar'
Copy-Item -LiteralPath $plugin -Destination $lib -Force
$classpath = Join-Path $lib '*'
& (Join-Path $JdkDirectory 'bin/javac.exe') --release 11 -cp $classpath -d $classes (Join-Path $PSScriptRoot 'YoutubePersistentHttpStream.java')
if($LASTEXITCODE -ne 0) { throw 'Falha na compilação.' }
& (Join-Path $JdkDirectory 'bin/java.exe') -cp "$classes;$classpath" (Join-Path $PSScriptRoot 'RangeLengthTest.java')
if($LASTEXITCODE -ne 0) { throw 'Falha nos testes.' }
$result = Join-Path $build 'youtube-plugin-1.18.2.jar'
Copy-Item -LiteralPath $plugin -Destination $result -Force
& (Join-Path $JdkDirectory 'bin/jar.exe') --update --file $result -C $classes 'dev/lavalink/youtube/track/YoutubePersistentHttpStream.class'
if($LASTEXITCODE -ne 0) { throw 'Falha ao gerar o plugin.' }
Write-Output "Plugin corrigido: $result"
