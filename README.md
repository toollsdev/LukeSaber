<div align="center">
  <img src="assets/branding/lukes-saber-banner.png" alt="Luke's Saber — Music, Community and Support" width="100%">

  <br>

  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Discord](https://img.shields.io/badge/Discord-Music_Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)
  [![Lavalink](https://img.shields.io/badge/Audio-Lavalink-ED4245?style=for-the-badge)](https://github.com/lavalink-devs/Lavalink)
  [![License](https://img.shields.io/github/license/toollsdev/LukeSaber?style=for-the-badge&color=57F287)](LICENSE)

  **High-fidelity music for every Discord community.**<br>
  **Música em alta fidelidade para todas as comunidades do Discord.**

  [Português](#-português) · [English](#-english) · [Instalação](#-instalação) · [Installation](#-installation) · [Reportar problema](https://github.com/toollsdev/LukeSaber/issues)
</div>

---

## 🇧🇷 Português

**Luke's Saber** é um bot de música de alta fidelidade para Discord, projetado para trazer reprodução ágil, áudio cristalino e integração fluida com múltiplas plataformas diretamente para os seus canais de voz.

Criado para comunidades do mundo todo, o projeto combina uma experiência simples para os ouvintes com opções completas de personalização e hospedagem para administradores.

> **Continuação do projeto original:** Luke's Saber dá continuidade ao [MuseHeart-MusicBot](https://github.com/zRitsu/MuseHeart-MusicBot), criado originalmente por **Alex ([zRitsu](https://github.com/zRitsu))**. Esta versão é personalizada e mantida por **toollsdev**, preservando o crédito, o histórico e a licença do projeto de origem.

Mantido por **[toollsdev](https://github.com/toollsdev)** · [Repositório](https://github.com/toollsdev/LukeSaber) · [Relatar um problema](https://github.com/toollsdev/LukeSaber/issues)

### 🐾 A origem do nome

Luke é o cachorro salsichinha que inspirou o coração e o mascote do projeto. O nome **Luke's Saber** une essa homenagem à imagem de um sabre azul atravessando a galáxia — agora com música, comunidade e uma boa dose de personalidade.

### ✨ Recursos

- Player interativo com botões, comandos de barra e comandos por prefixo.
- Fila de músicas, playlists, pausa, retomada, volume e repetição.
- Reprodução de vídeos do YouTube pela fonte exata, sem trocar automaticamente por covers de outras plataformas.
- Integração com links e metadados do Spotify e suporte a fontes como SoundCloud.
- Player fixo em canal de pedidos, skins personalizáveis e suporte a múltiplos bots.
- Integração opcional com Last.fm e Rich Presence.
- Aviso no terminal quando a autorização do YouTube precisar ser renovada, quando o Lavalink for iniciado pelo bot.

O Spotify fornece os metadados das faixas; a reprodução depende de uma fonte de áudio compatível. A disponibilidade e a qualidade final também dependem da fonte e do servidor de música.

### 🧰 Tecnologias

Python · Disnake · Wavelink customizado · Lavalink · youtube-source · LavaSrc

### 🚀 Instalação

Tenha Python 3.11 ou superior, Git e um JDK compatível com a versão do Lavalink utilizada.

```bash
git clone https://github.com/toollsdev/lukesaber.git
cd lukesaber
python -m venv venv
```

Ative o ambiente no Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Ou no Linux:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### ⚙️ Configuração

Copie [`.example.env`](.example.env) para `.env` na raiz do projeto e preencha suas credenciais. O exemplo contém as opções comentadas, sem tokens ou senhas reais.

No PowerShell:

```powershell
Copy-Item .example.env .env
```

Se você já tem um `.env` configurado, mantenha-o e consulte o exemplo sem sobrescrevê-lo. Configuração inicial para um servidor Lavalink local iniciado pelo bot:

```dotenv
TOKEN_BOT_1=seu_token_do_discord
DEFAULT_PREFIX=!
SOURCE_REPO=https://github.com/toollsdev/lukesaber.git
RUN_LOCAL_LAVALINK=true
CONNECT_LOCAL_LAVALINK=true
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

Use o [Discord Developer Portal](https://discord.com/developers/applications) para criar a aplicação, obter o token e configurar as permissões e intents necessárias. Convide o bot com os escopos `bot` e `applications.commands`, permitindo acesso aos canais de texto e voz.

As opções disponíveis ficam em [`config_loader.py`](config_loader.py). Mantenha tokens e segredos apenas nos arquivos locais; não os publique no GitHub.

#### YouTube e Lavalink

O servidor utiliza o plugin `youtube-source`. No `application.yml`, a fonte interna antiga do YouTube deve ficar desativada e o plugin deve estar habilitado.

Se a configuração exigir autorização, conclua o fluxo do Google mostrado pelo Lavalink. Quando o login for aceito, Luke's Saber captura o novo `refreshToken` sem exibi-lo no console, salva-o automaticamente no `application.yml` e o reutiliza nas próximas inicializações. Use uma conta separada, sem dados pessoais importantes, conforme recomendado pelo próprio `youtube-source`.

Esta versão inclui uma [correção local de leitura por blocos](lavalink_patches/youtube-range-length/README.md), validada com youtube-source 1.18.2 e Lavaplayer 2.2.7. O JAR modificado é um arquivo local: siga o procedimento de reconstrução após uma instalação nova. Atualizações do plugin podem remover a correção.

#### Spotify

Obtenha o Client ID e o Client Secret no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). Preencha `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` no `.env`.

Para a integração via LavaSrc, configure também `plugins.lavasrc.spotify.clientId` e `plugins.lavasrc.spotify.clientSecret` no `application.yml`, com a fonte Spotify habilitada. Reinicie os processos correspondentes após alterar suas configurações. O acesso à API depende das regras e permissões vigentes do Spotify.

### ▶️ Executar

Com o ambiente ativado:

```bash
python main.py
```

No Windows, também é possível usar `source_start_windows.bat`.

#### Manter o bot self-hosted 24 horas com PM2

Depois de preparar o ambiente Python uma vez, use o PM2 para executar o bot em segundo plano e reiniciá-lo automaticamente caso o processo pare:

```console
pm2 start ecosystem.config.cjs --only lukes-saber
pm2 save
```

No Windows, você também pode executar `pm2_start_windows.bat`. Ele valida o ambiente, inicia o processo sem manter uma janela aberta, salva a lista do PM2 e mostra o estado do bot.

O `pm2 save` registra a lista atual de processos. Depois de reiniciar o computador, restaure essa lista com:

```console
pm2 resurrect
```

Para iniciar automaticamente após entrar no Windows, crie uma tarefa no **Agendador de Tarefas** que execute `pm2 resurrect` no logon do usuário. Marque a opção para executar a tarefa mesmo sem uma janela visível. Em Linux, use `pm2 startup`, execute o comando administrativo exibido pelo PM2 e finalize com `pm2 save`.

Para disponibilidade contínua, o computador ou servidor precisa permanecer ligado, conectado à internet e sem suspensão automática. Se o seu computador não fica ligado o tempo todo, hospede o projeto em uma VPS ou servidor dedicado. O PM2 recupera falhas do processo, mas não consegue manter o bot online enquanto a máquina estiver desligada ou sem rede.

Comandos de manutenção:

```console
pm2 status lukes-saber
pm2 logs lukes-saber
pm2 restart lukes-saber
pm2 stop lukes-saber
```

Os registros ficam em `.logs/pm2/`. Ao atualizar o código ou as dependências, execute a instalação necessária e depois `pm2 restart lukes-saber`.

Entre em um canal de voz e use os comandos de música do bot. Use `/setup` para configurar o player fixo e `/change_skin` para escolher sua aparência.

### 🩺 Diagnóstico

- Logs do servidor de música: `.logs/lavalink/spring.log`.
- **VOCÊ PRECISA RENOVAR O TOKEN**: conclua novamente a autorização do YouTube e atualize o token local.
- Erros de leitura ou decodificação de áudio não significam necessariamente que o token expirou.
- Ao abrir uma issue, informe o comando, a fonte, as versões e o erro, removendo tokens e dados privados.

### 📜 Manutenção e licença

**Luke's Saber** é uma continuação personalizada mantida por **toollsdev** a partir do [MuseHeart-MusicBot](https://github.com/zRitsu/MuseHeart-MusicBot), projeto original criado por **Alex ([zRitsu](https://github.com/zRitsu))**. A continuidade e as personalizações não alteram a autoria do código preexistente.

Os avisos originais permanecem em [`LICENSE`](LICENSE). O projeto mantém a licença GNU GPL indicada nesse arquivo; bibliotecas e componentes externos conservam suas próprias licenças.

### 🤖 Uso de inteligência artificial

O **ChatGPT, da OpenAI**, foi utilizado como ferramenta de apoio durante a personalização do Luke's Saber. Ele auxiliou na análise e reconstrução de alguns trechos de código que estavam quebrados, na investigação de erros e na preparação de correções. O conteúdo, a estrutura e a apresentação deste `README.md` foram produzidos principalmente com o auxílio do ChatGPT e revisados pelo mantenedor do projeto.

O uso dessa ferramenta não substitui a autoria e as licenças do código original. **toollsdev** permanece responsável por revisar, testar, manter e publicar as alterações aplicadas ao repositório.

---

## 🌎 English

**Luke's Saber** is a high-fidelity Discord music bot built to deliver responsive playback, crystal-clear audio, and smooth multi-platform integration directly to your voice channels.

Designed for communities around the world, the project combines a simple listening experience with extensive customization and self-hosting options for administrators.

> **Continuation of the original project:** Luke's Saber continues the work of [MuseHeart-MusicBot](https://github.com/zRitsu/MuseHeart-MusicBot), originally created by **Alex ([zRitsu](https://github.com/zRitsu))**. This version is customized and maintained by **toollsdev** while preserving the credit, history, and license of the original project.

Maintained by **[toollsdev](https://github.com/toollsdev)** · [Repository](https://github.com/toollsdev/LukeSaber) · [Report an issue](https://github.com/toollsdev/LukeSaber/issues)

### 🐾 Behind the name

Luke is the dachshund who inspired the heart and mascot of this project. The name **Luke's Saber** combines that tribute with the image of a blue energy saber crossing the galaxy — now powered by music, community, and plenty of personality.

### ✨ Features

- Interactive player with buttons, slash commands, and prefix commands.
- Music queues, playlists, pause, resume, volume, and repeat controls.
- Direct playback of exact YouTube videos without automatically replacing them with unrelated covers from other platforms.
- Spotify link and metadata integration, with support for sources such as SoundCloud.
- Dedicated song-request channel, customizable player skins, and multiple bot instances.
- Optional Last.fm and Rich Presence integrations.
- Terminal warning when YouTube authorization must be renewed, when Lavalink is started by the bot.

Spotify provides track metadata; playback still requires a compatible audio source. Final availability and quality also depend on the selected source and music server.

### 🧰 Technology

Python · Disnake · Customized Wavelink · Lavalink · youtube-source · LavaSrc

### 🚀 Installation

Install Python 3.11 or newer, Git, and a JDK compatible with the Lavalink version used by the project.

```bash
git clone https://github.com/toollsdev/lukesaber.git
cd lukesaber
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Or on Linux:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### ⚙️ Configuration

Copy [`.example.env`](.example.env) to `.env` in the project root and enter your credentials. The example contains documented options without real tokens or passwords.

In PowerShell:

```powershell
Copy-Item .example.env .env
```

If you already have a configured `.env`, keep it and consult the example without overwriting your file. Minimal configuration for a local Lavalink server started by the bot:

```dotenv
TOKEN_BOT_1=your_discord_token
DEFAULT_PREFIX=!
SOURCE_REPO=https://github.com/toollsdev/lukesaber.git
RUN_LOCAL_LAVALINK=true
CONNECT_LOCAL_LAVALINK=true
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

Use the [Discord Developer Portal](https://discord.com/developers/applications) to create the application, obtain its token, and configure the required permissions and intents. Invite the bot with the `bot` and `applications.commands` scopes and grant access to the required text and voice channels.

All available settings are documented in [`config_loader.py`](config_loader.py). Keep tokens and secrets in local files only; never publish them on GitHub.

#### YouTube and Lavalink

The server uses the `youtube-source` plugin. Disable Lavalink's legacy built-in YouTube source in `application.yml` and keep the plugin enabled.

When authorization is required, complete the Google flow displayed by Lavalink. Once the login is accepted, Luke's Saber captures the new `refreshToken` without printing it to the console, saves it automatically to `application.yml`, and reuses it on future starts. Use a separate account without important personal data, as recommended by `youtube-source` itself.

This version includes a [local chunked-reading fix](lavalink_patches/youtube-range-length/README.md), validated with youtube-source 1.18.2 and Lavaplayer 2.2.7. The modified JAR is a local artifact: follow the rebuild procedure after a fresh installation. Plugin updates may remove the patch.

#### Spotify

Create a Client ID and Client Secret in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), then set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in `.env`.

For LavaSrc integration, also set `plugins.lavasrc.spotify.clientId` and `plugins.lavasrc.spotify.clientSecret` in `application.yml` and enable the Spotify source. Restart the related processes after changing the configuration. API access depends on Spotify's current rules and account permissions.

### ▶️ Running the bot

With the virtual environment active:

```bash
python main.py
```

On Windows, you can also run `source_start_windows.bat`.

### Keep the self-hosted bot online 24/7 with PM2

After preparing the Python environment once, use PM2 to run the bot in the background and restart it automatically if the process stops:

```console
pm2 start ecosystem.config.cjs --only lukes-saber
pm2 save
```

On Windows, you can also run `pm2_start_windows.bat`. It validates the environment, starts the process without keeping a window open, saves the PM2 process list, and shows its status.

`pm2 save` records the current process list. After restarting the computer, restore it with:

```console
pm2 resurrect
```

To restore it automatically after signing in to Windows, create a **Task Scheduler** task that runs `pm2 resurrect` when the user logs on, with the task configured to run without a visible window. On Linux, run `pm2 startup`, execute the administrative command printed by PM2, and finish with `pm2 save`.

For continuous availability, the computer or server must remain powered on, connected to the internet, and configured not to sleep. If your computer is not always running, deploy the project to a VPS or dedicated server. PM2 recovers a stopped process, but it cannot keep the bot online while its host is powered off or disconnected.

Maintenance commands:

```console
pm2 status lukes-saber
pm2 logs lukes-saber
pm2 restart lukes-saber
pm2 stop lukes-saber
```

Logs are written to `.logs/pm2/`. After updating the code or dependencies, install what changed and run `pm2 restart lukes-saber`.

Join a voice channel and use the music commands. Run `/setup` to configure the dedicated player and `/change_skin` to select its appearance.

### 🩺 Troubleshooting

- Music server logs: `.logs/lavalink/spring.log`.
- **VOCÊ PRECISA RENOVAR O TOKEN / YOU NEED TO RENEW THE TOKEN**: repeat the YouTube authorization flow and update the local token.
- Audio reading or decoding errors do not necessarily mean that the token has expired.
- When opening an issue, include the command, source, component versions, and sanitized error output. Remove all tokens and private data first.

### 📜 Maintenance and license

**Luke's Saber** is a customized continuation maintained by **toollsdev** from [MuseHeart-MusicBot](https://github.com/zRitsu/MuseHeart-MusicBot), the original project created by **Alex ([zRitsu](https://github.com/zRitsu))**. This continuation and its customizations do not change the authorship of pre-existing code.

The original notices remain in [`LICENSE`](LICENSE). The project follows the GNU GPL license stated in that file; external libraries and components retain their respective licenses.

### 🤖 Use of artificial intelligence

**ChatGPT by OpenAI** was used as a supporting tool during the customization of Luke's Saber. It assisted with analyzing and reconstructing parts of the code that were broken, investigating errors, and preparing fixes. The content, structure, and presentation of this `README.md` were produced primarily with ChatGPT's assistance and reviewed by the project maintainer.

This assistance does not replace the authorship or licenses of the original code. **toollsdev** remains responsible for reviewing, testing, maintaining, and publishing the changes applied to the repository.

---

<div align="center">
  <img src="assets/branding/lukes-saber-avatar.png" alt="Luke, the Luke's Saber mascot" width="140">

  Made with 💙 for Luke and Discord music communities around the world.
</div>
