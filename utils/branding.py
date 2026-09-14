"""Identidade visual central do Luke's Saber."""

import disnake


class LukeTheme:
    PRIMARY = 0x2F81F7
    SECONDARY = 0x56D6FF
    GOLD = 0xF2B84B
    SUCCESS = 0x3DDC97
    WARNING = 0xF2B84B
    ERROR = 0xED5E68
    BACKGROUND = 0x0B1220

    BRAND = "Luke's Saber"
    TAGLINE = "Som além das estrelas · Sound beyond the stars"
    FOOTER = "Luke's Saber  •  Música em alta fidelidade"

    NOW_PLAYING = "⚔️  TOCANDO AGORA"
    PAUSED = "⏸️  REPRODUÇÃO PAUSADA"
    QUEUE = "✦  PRÓXIMAS NA FILA"


def brand_embed(
    *,
    title: str | None = None,
    description: str | None = None,
    color: int | disnake.Color = LukeTheme.PRIMARY,
    bot=None,
    footer: str | None = None,
) -> disnake.Embed:
    """Cria um embed novo com o acabamento padrão da marca."""
    embed = disnake.Embed(title=title, description=description, color=color)
    if bot and getattr(bot, "user", None):
        embed.set_author(name=LukeTheme.BRAND, icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=footer or LukeTheme.FOOTER)
    return embed


def finish_embed(embed: disnake.Embed, *, bot=None, footer: str | None = None) -> disnake.Embed:
    """Aplica autoria e rodapé da marca a um embed existente."""
    if bot and getattr(bot, "user", None) and not embed.author:
        embed.set_author(name=LukeTheme.BRAND, icon_url=bot.user.display_avatar.url)
    if not embed.footer:
        embed.set_footer(text=footer or LukeTheme.FOOTER)
    return embed
