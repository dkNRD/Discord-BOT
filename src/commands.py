import discord
import random
import time

flood_mod = False
user_message = {}


async def on_message(ctx, bot):
    """
    (Not a command but user a global variable)
    Répond à un message si celui-ci est égal à 'Salut tout le monde' par 'Salut tout seul' et le pseudo de l'auteur
    et gère le flood
    :param ctx: contexte du message
    :param bot: the discord
    :return: None
    """
    if flood_mod:
        if ctx.author.id != bot.user.id:
            if ctx.author.id in user_message:
                if len(user_message[ctx.author.id]) >= 5:
                    # check if the 5th message away is in less than 5 seconds
                    message_list = user_message[ctx.author.id]
                    if ctx.created_at.timestamp() - message_list[len(message_list) - 6].created_at.timestamp() < 5:
                        await ctx.channel.send(f"{ctx.author.mention} arrête de spammer !")
                    else:
                        user_message[ctx.author.id].append(ctx)
                        user_message[ctx.author.id].pop(0)
                else:
                    user_message[ctx.author.id].append(ctx)
            else:
                user_message[ctx.author.id] = [ctx]

    if 'Salut tout le monde'.__eq__(ctx.content):
        await ctx.channel.send(f"Salut tout seul {ctx.author.mention}")
    else:
        await bot.process_commands(ctx)


async def pong(ctx):
    """
    Envoie pong dans le channel où la commande a été envoyée
    :param ctx: contexte de la commande
    :return: None
    """
    await ctx.send('pong')


async def name(ctx):
    """
    Envoie le pseudo de l'auteur de la commande
    :param ctx: contexte de la commande
    :return: None
    """
    await ctx.send(ctx.author)


async def d6(ctx):
    """
    Envoie un nombre aléatoire entre 1 et 6
    :param ctx: contexte de la commande
    :return: None
    """
    await ctx.send(random.randint(1, 6))


async def admin(ctx, member):
    """
    Crée le rôle admin s'il n'existe pas et l'ajoute à l'utilisateur s'il ne l'a pas déjà
    :param ctx: contexte de la commande
    :param member: utilisateur à promouvoir
    :return: None
    """
    role = discord.utils.get(ctx.guild.roles, name="admin")
    if role is None:
        await ctx.guild.create_role(name="admin", permissions=discord.Permissions(8))
        role = discord.utils.get(ctx.guild.roles, name="admin")
        await ctx.send("Le rôle admin a été créé.")
    else:
        await ctx.send("Le rôle admin existe déjà.")

    if role in member.roles:
        await ctx.send(f"{member.mention} est déjà admin.")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} est maintenant admin.")


async def ban(ctx, member, reason):
    """
    Bannit un utilisateur si l'autheur de la commande a la permission et que l'utilisateur n'est pas admin
    :param ctx: contexte de la commande
    :param member: utilisateur à bannir
    :param reason: raison du bannissement
    :return: None
    """
    if member is None:
        await ctx.send("Vous devez spécifier un utilisateur.")
    elif member.id == ctx.author.id:
        await ctx.send("Vous ne pouvez pas vous bannir vous-même.")
    elif ctx.author.guild_permissions.ban_members is False:
        await ctx.send("Vous n'avez pas le droit de faire ça.")
    else:
        if discord.utils.get(ctx.guild.roles, name="admin") in member.roles:
            await ctx.send("Vous ne pouvez pas bannir un admin.")
        else:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} a été banni pour la raison suivante : {reason}.")


async def flood(ctx, message):
    """
    Active ou désactive la modération du flood si l'user est admin
    :param ctx: contexte de la commande
    :param message: le message pour activer ou désactiver le flood mod
    :return:
    """
    if discord.utils.get(ctx.guild.roles, name="admin") in ctx.author.roles:
        global flood_mod
        if message == "on":
            flood_mod = True
            await ctx.send("La modération du flood est activée.")
        elif message == "off":
            flood_mod = False
            await ctx.send("La modération du flood est désactivée.")
        else:
            await ctx.send("Vous devez spécifier on ou off.")


async def xkcd(ctx):
    """
    Envoie un lien vers un comic xkcd aléatoire
    :param ctx: contexte de la commande
    :return: None
    """
    await ctx.send(f"https://xkcd.com/{random.randint(1, 2500)}")


async def poll(ctx, content):
    """
    Envoie un sondage dans le channel où la commande a été envoyée, supprime le message après 20 secondes et envoie le
    résultat
    :param ctx: contexte de la commande
    :param content: contenu du sondage
    :return: None
    """
    poll_message = await ctx.send(f"@here {content}")
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    time.sleep(20)
    poll_message = await ctx.channel.fetch_message(poll_message.id)
    if poll_message.reactions[0].count > poll_message.reactions[1].count:
        await ctx.send(f"Le résultat du sondage \"{content}\" est : 👍")
    elif poll_message.reactions[0].count < poll_message.reactions[1].count:
        await ctx.send(f"Le résultat du sondage \"{content}\" est : 👎")
    else:
        await ctx.send(f"Le résultat du sondage \"{content}\" est : 🟰")
    await poll_message.delete()
