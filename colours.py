from os import getenv
from typing import (
    Dict,
    Final,
    Literal,
    Optional,
    Union,
)

from disnake import (
    CustomActivity,
    GuildCommandInteraction,
    Member,
    Role,
    User,
)
from disnake.ext.commands import InteractionBot, Param, guild_only
from dotenv import load_dotenv


VALID_HEX_CHARS: Final[Literal["0123456789abcdef"]] = "0123456789abcdef"
LEN_OF_HEX_STR: Final[int] = 6


bot = InteractionBot(
    activity = CustomActivity(
        state="🌈 /colour-role",
        name="Custom Status",
    ),
)
member_roles: Dict[int, Role] = {}


def _get_user_role_name(member: Union[Member, User]) -> str:
    """Generates the users role name"""
    # Change this to whatever you want, just make sure that it's
    #   unique per user, consistent, and below 250 chars (role name max len).
    return str(member.id)


async def _fetch_users_role(member: Union[Member, User]) -> Optional[Role]:
    """Fetches the users colour role"""
    if not isinstance(member, Member):
        return None

    user_role_name = _get_user_role_name(member)
    role = member_roles.get(member.id, None)
    if role is not None:
        return role

    for role in member.guild.roles:
        if role.name == user_role_name:
            member_roles[member.id] = role
            return role
    return None


def _convert_str_hex_to_int_hex(str_hex: str) -> Optional[int]:
    """Converts a str representation of a hex int to an int representation of a hex int"""

    str_hex = str_hex.lower()
    colour = str_hex if (str_hex[0] != "#") else str_hex[1::]
    colour = colour if (str_hex[0:2] != "0x") else str_hex[2::]
    if not (all(c in VALID_HEX_CHARS for c in colour) or len(colour) != LEN_OF_HEX_STR):
        return None
    else:
        return int(colour, 16)


@guild_only()
@bot.slash_command(
    name="colour-role",
    description="🌈 Edit / create your custom colour role.",
)
async def colour_role(_: GuildCommandInteraction[InteractionBot]) -> None:
    pass

@colour_role.sub_command(
    name="set-colour",
    description="🌈 Set the colour of your colour role.",
)
async def colour_role_set_colour(
    inter: GuildCommandInteraction[InteractionBot],
    colour: str = Param(
        name="colour",
        description="The hex code of the colour."
    ),
) -> None:
    hex_int = _convert_str_hex_to_int_hex(colour)
    if hex_int is None:
        await inter.response.send_message(
            content="That colour was not a valid hex code D:",
            ephemeral=True,
        )
        return

    await inter.response.defer()

    role = await _fetch_users_role(inter.user)
    if role is None:
        user_role_name = _get_user_role_name(inter.user)
        role = await inter.guild.create_role(
            name=user_role_name,
            colour=hex_int,
            reason="User requested colour role."
        )
    else:
        if role.colour.value != hex_int:
            await role.edit(
                colour=hex_int,
                reason="User requested new colour.",
            )
    await inter.edit_original_response(
        content="Your colour role has been updated :D",
    )

@colour_role.sub_command(
    name="delete-role",
    description="🌈 Delete your colour role.",
)
async def colour_role_delete_colour(
    inter: GuildCommandInteraction[InteractionBot],
) -> None:
    await inter.response.defer()
    role = await _fetch_users_role(inter.user)
    if role is None:
        await inter.edit_original_response(
            content="You don't have a colour role!",
        )
        return

    await role.delete(reason="Requested by role owner.")
    await inter.edit_original_response(
        content="Your colour role has been deleted!",
    )


if __name__ == "__main__":
    load_dotenv()
    discord_bot_token: str | None = getenv("DISCORD_BOT_TOKEN")
    if discord_bot_token is None:
        raise EnvironmentError("`DISCORD_BOT_TOKEN` was not provided.")

    bot.run(discord_bot_token)
