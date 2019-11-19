import discord
from config import Config
from darrcord import sonarr
from darrcord import radarr
from darrcord import logger


client = discord.Client()


def get_client():
    return client


def parse_message(message):
    logger.info(f"parsing message: {message}")
    ret_obj = {}

    son_ret = None
    if Config.SONARR_ENABLED:
        if str(message.channel) in Config.SONARR_CHANNELS:
            son_ret = parse_sonarr(message)

    if son_ret:
        ret_obj["sonarr"] = True
        ret_obj["sonarr_obj"]=son_ret
    else:
        ret_obj["sonarr"] = False

    rad_ret = None
    if Config.RADARR_ENABLED:
        if str(message.channel) in Config.RADARR_CHANNELS:
            rad_ret = parse_radarr(message)

    if rad_ret:
        ret_obj["radarr"] = True
        ret_obj["radarr_obj"]=rad_ret
    else:
        ret_obj["radarr"]=False

    return ret_obj


def parse_sonarr(message):
    ret = None
    try:
        command = message.content[0].lower()
        func = sonarr_switch(command)
        ret = func(message.content[1:].strip())
    except:
        return None
    return ret


def sonarr_switch(command):
    switch={
        'r':request_sonarr_series
    }
    ret = switch.get(command,null_func)
    return ret


def request_sonarr_series(series):
    try:
        id = int(series)
        son_resp = sonarr.req_series_request(id)
        code = son_resp["code"]
        resp = son_resp["json"]
        if code>=200 and code < 400:
            if resp:
                ret = {'message': f"Successfully requested {resp[0]['title']}: https://www.thetvdb.com/?tab=series&id={id}",
                   'resp': resp}
            else:
                ret = {'message':"Unknown error.  No error message.  Sorry."}
        else:
            if resp:
                ret = {'message': f"Error adding series.  Error message is: {resp[0]['errorMessage']}.", 'resp':resp}
            else:
                ret = {'message':"Unknown error.  No error message.  Sorry."}
        return ret
    except ValueError as err:
        logger.error(err)
        return None
    except Exception as e:
        logger.exception(e)
        return None


def parse_radarr(message):
    ret = None
    try:
        command = message.content[0].lower()
        func = radarr_switch(command)
        ret = func(message.content[1:].strip())
    except:
        return None
    return ret


def radarr_switch(command):
    switch={
        'r':request_radarr_movie
    }
    ret = switch.get(command,null_func)
    return ret


def request_radarr_movie(movie):
    try:
        id = int(movie)
        son_resp = radarr.req_movie_request(id)
        code = son_resp["code"]
        resp = son_resp["json"]
        if code>=200 and code < 400:
            if resp:
                ret = {'message': f"Successfully requested {resp[0]['title']}: https://www.themoviedb.org/movie/{id}",
                   'resp': resp}
            else:
                ret = {'message':"Unknown error.  No error message.  Sorry."}
        else:
            if resp:
                ret = {'message': f"Error adding series.  Error message is: {resp[0]['errorMessage']}.", 'resp':resp}
            else:
                ret = {'message':"Unknown error.  No error message.  Sorry."}
        return ret
    except ValueError as err:
        logger.error(err)
        return None
    except Exception as e:
        logger.exception(e)
        return None


def null_func(args):
    return {}


@client.event
async def on_message(message):
    # we do not want the bot to look at its own messages
    if message.author == client.user:
        return
    logger.debug(f"Received message: {message.content}")
    if str(message.channel) not in Config.SONARR_CHANNELS and str(message.channel) not in Config.RADARR_CHANNELS:
        return

    msg = None

    message_data = parse_message(message)
    if not message_data["sonarr"] and not message_data["radarr"]:
        if (Config.SONARR_ENABLED and str(message.channel) in Config.SONARR_CHANNELS) or (Config.RADARR_ENABLED and str(message.channel) in  Config.RADARR_CHANNELS):
            msg=f"Sorry, {message.author.mention}, I didn't understand that request."
        else:
            return
    if message_data["sonarr"]:
        msg=f"{message.author.mention}: {message_data['sonarr_obj']['message']}"
        await message.channel.send(msg)
        msg = None
    if message_data["radarr"]:
        msg=f"{message.author.mention}: {message_data['radarr_obj']['message']}"
        await message.channel.send(msg)
        msg = None

    if msg:
        await message.channel.send(msg)