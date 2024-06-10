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
    Intents,
    Member,
    Role,
    User,
)
from disnake.ext.commands import InteractionBot, Param, guild_only
from dotenv import load_dotenv
from fuzzy_search import FuzzyPhraseSearcher


VALID_HEX_CHARS: Final[Literal["0123456789abcdef"]] = "0123456789abcdef"
LEN_OF_HEX_STR: Final[int] = 6
INTENTS: Final[Intents] = Intents(guilds=True, members=True)
COLOUR_LOOKUP_TABLE: Final[Dict[str, int]] = {
    'silver': 12632256,
    'gray': 8421504,
    'white': 16777215,
    'maroon': 8388608,
    'red': 16711680,
    'purple': 8388736,
    'fuchsia': 16711935,
    'green': 32768,
    'lime': 65280,
    'olive': 8421376,
    'yellow': 16776960,
    'navy': 128,
    'blue': 255,
    'teal': 32896,
    'aqua': 65535,
    'aliceblue': 15792383,
    'antiquewhite': 16444375,
    'aquamarine': 8388564,
    'azure': 15794175,
    'beige': 16119260,
    'bisque': 16770244,
    'black': 0,
    'blanchedalmond': 16772045,
    'blueviolet': 9055202,
    'brown': 10824234,
    'burlywood': 14596231,
    'cadetblue': 6266528,
    'chartreuse': 8388352,
	'chocolate': 13789470,
	'coral': 16744272,
	'cornflowerblue': 6591981,
	'cornsilk': 16775388,
	'crimson': 14423100,
	'cyan': 65535,
	'darkblue': 139,
	'darkcyan': 35723,
	'darkgoldenrod': 12092939,
	'darkgray': 11119017,
	'darkgreen': 25600,
	'darkgrey': 11119017,
	'darkkhaki': 12433259,
	'darkmagenta': 9109643,
	'darkolivegreen': 5597999,
	'darkorange': 16747520,
	'darkorchid': 10040012,
	'darkred': 9109504,
	'darksalmon': 15308410,
	'darkseagreen': 9419919,
	'darkslateblue': 4734347,
	'darkslategray': 3100495,
	'darkslategrey': 3100495,
	'darkturquoise': 52945,
	'darkviolet': 9699539,
	'deeppink': 16716947,
	'deepskyblue': 49151,
	'dimgray': 6908265,
	'dimgrey': 6908265,
	'dodgerblue': 2003199,
	'firebrick': 11674146,
	'floralwhite': 16775920,
	'forestgreen': 2263842,
	'gainsboro': 14474460,
	'ghostwhite': 16316671,
	'gold': 16766720,
	'goldenrod': 14329120,
	'greenyellow': 11403055,
	'grey': 8421504,
	'honeydew': 15794160,
	'hotpink': 16738740,
	'indianred': 13458524,
	'indigo': 4915330,
	'ivory': 16777200,
	'khaki': 15787660,
	'lavender': 15132410,
	'lavenderblush': 16773365,
	'lawngreen': 8190976,
	'lemonchiffon': 16775885,
	'lightblue': 11393254,
	'lightcoral': 15761536,
	'lightcyan': 14745599,
	'lightgoldenrodyellow': 16448210,
	'lightgray': 13882323,
	'lightgreen': 9498256,
	'lightgrey': 13882323,
	'lightpink': 16758465,
	'lightsalmon': 16752762,
	'lightseagreen': 2142890,
	'lightskyblue': 8900346,
	'lightslategray': 7833753,
	'lightslategrey': 7833753,
	'lightsteelblue': 11584734,
	'lightyellow': 16777184,
	'limegreen': 3329330,
	'linen': 16445670,
	'magenta': 16711935,
	'mediumaquamarine': 6737322,
	'mediumblue': 205,
	'mediumorchid': 12211667,
	'mediumpurple': 9662683,
	'mediumseagreen': 3978097,
	'mediumslateblue': 8087790,
	'mediumspringgreen': 64154,
	'mediumturquoise': 4772300,
	'mediumvioletred': 13047173,
	'midnightblue': 1644912,
	'mintcream': 16121850,
	'mistyrose': 16770273,
	'moccasin': 16770229,
	'navajowhite': 16768685,
	'oldlace': 16643558,
	'olivedrab': 7048739,
	'orange': 16753920,
	'orangered': 16729344,
	'orchid': 14315734,
	'palegoldenrod': 15657130,
	'palegreen': 10025880,
	'paleturquoise': 11529966,
	'palevioletred': 14381203,
	'papayawhip': 16773077,
	'peachpuff': 16767673,
	'peru': 13468991,
	'pink': 16761035,
	'plum': 14524637,
	'powderblue': 11591910,
	'rosybrown': 12357519,
	'royalblue': 4286945,
	'saddlebrown': 9127187,
	'salmon': 16416882,
	'sandybrown': 16032864,
	'seagreen': 3050327,
	'seashell': 16774638,
	'sienna': 10506797,
	'skyblue': 8900331,
	'slateblue': 6970061,
	'slategray': 7372944,
	'slategrey': 7372944,
	'snow': 16775930,
	'springgreen': 65407,
	'steelblue': 4620980,
	'tan': 13808780,
	'thistle': 14204888,
	'tomato': 16737095,
	'turquoise': 4251856,
	'violet': 15631086,
	'wheat': 16113331,
	'whitesmoke': 16119285,
	'yellowgreen': 10145074,
}
FUZZY_SEARCH_CONFIG: Final[Dict[str, Union[int, float, bool]]] = {
    "char_match_threshold": 0.6,
    "ngram_threshold": 0.5,
    "levenshtein_threshold": 0.6,
    "ignorecase": True,
    "max_length_variance": 3,
    "ngram_size": 2,
    "skip_size": 2,
}
fuzzy_searcher = FuzzyPhraseSearcher(
    config=FUZZY_SEARCH_CONFIG,
    phrase_model=COLOUR_LOOKUP_TABLE,
)


bot = InteractionBot(
    activity = CustomActivity(
        state="🌈 /colour-role",
        name="Custom Status",
    ),
    intents=INTENTS,
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
        results = fuzzy_searcher.find_matches(str_hex)
        if len(results) == 0:
            return None
        return COLOUR_LOOKUP_TABLE[results[0].phrase.name]
    else:
        return int(colour, 16)


@guild_only()
@bot.slash_command(
    name="colour-role",
    description="🌈 Edit / create your custom colour role.",
)
async def colour_role(_: GuildCommandInteraction) -> None:
    pass

@colour_role.sub_command(
    name="set-colour",
    description="🌈 Set the colour of your colour role.",
)
async def colour_role_set_colour(
    inter: GuildCommandInteraction,
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
        assert isinstance(inter.user, Member)
        await inter.user.add_roles(role)
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
    inter: GuildCommandInteraction,
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
    discord_bot_token: Optional[str] = getenv("DISCORD_BOT_TOKEN")
    if discord_bot_token is None:
        raise EnvironmentError("`DISCORD_BOT_TOKEN` was not provided.")

    if getenv("PROXY_URL"):
        from disnake.http import Route
        Route.BASE = getenv("PROXY_URL")
	
    bot.run(discord_bot_token)
