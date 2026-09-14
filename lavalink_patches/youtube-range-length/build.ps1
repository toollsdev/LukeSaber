param([Parameter(Mandatory=$true)][string]$JdkDirectory)
$ErrorActionPreference = 'Stop'
$project = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$build = Join-Path $project '.tmp/youtube-range-build'
$lib = Join-Path $build 'lib'
$classes = Join-Path $build 'classes'
if(Test-Path -LiteralPath $lib) { Remove-Item -LiteralPath $lib -Recurse -Force }
if(Test-Path -LiteralPath $classes) { Remove-Item -LiteralPath $classes -Recurse -Force }
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
# Bibliotecas nativas específicas de Linux não participam da compilação e
# algumas versões do javac no Windows não conseguem inspecioná-las.
Get-ChildItem -LiteralPath $lib -Filter '*native*.jar' | Remove-Item -Force
$plugin = Join-Path $project 'plugins/youtube-plugin-1.18.2.jar'
Copy-Item -LiteralPath $plugin -Destination $lib -Force
$classpath = @(
    (Join-Path $lib 'youtube-plugin-1.18.2.jar'),
    (Join-Path $lib 'lavaplayer-2.2.7.jar'),
    (Join-Path $lib 'httpclient-4.5.14.jar'),
    (Join-Path $lib 'httpcore-4.4.16.jar'),
    (Join-Path $lib 'slf4j-api-2.0.17.jar')
) -join ';'
& (Join-Path $JdkDirectory 'bin/javac.exe') --release 11 -cp $classpath -d $classes (Join-Path $PSScriptRoot 'YoutubePersistentHttpStream.java')
if($LASTEXITCODE -ne 0) { throw 'Falha na compilação.' }
& (Join-Path $JdkDirectory 'bin/java.exe') -cp "$classes;$classpath" (Join-Path $PSScriptRoot 'RangeLengthTest.java')
if($LASTEXITCODE -ne 0) { throw 'Falha nos testes.' }
$result = Join-Path $PSScriptRoot 'youtube-plugin-1.18.2.jar'
Copy-Item -LiteralPath $plugin -Destination $result -Force
& (Join-Path $JdkDirectory 'bin/jar.exe') --update --file $result -C $classes 'dev/lavalink/youtube/track/YoutubePersistentHttpStream.class'
if($LASTEXITCODE -ne 0) { throw 'Falha ao gerar o plugin.' }
Copy-Item -LiteralPath $result -Destination $plugin -Force
Write-Output "Plugin corrigido: $result"
