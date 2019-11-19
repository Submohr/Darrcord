Simple discord bot for Sonarr/Radarr integration.

#### Setup:

Config.py is looking for env variables to define things for the program.  Set them up in a .env file in the base
directory, or establish them in the environment before starting the program.

To get your discord token:  https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token 

#### Commands:

Only implemented command so far is "r {id}".

This works for both TV shows and movies.  For TV shows, it's the tvdb ID of a show - to find it, go to https://www.thetvdb.com/ and search for your show.  (For example: https://www.thetvdb.com/series/lost ).  On this page you'll find "The TVDB.com Series ID" with a value of 73739.  To request, Lost, you'll type:

`r 73739`

in a channel defined by SONARR_CHANNELS in the config.

Similarly for movies:  it uses the tmdb ID of a show.  To find it, go to https://www.themoviedb.org/ and  search for your movie.  (For example: https://www.themoviedb.org/movie/503919-the-lighthouse ).  In the URL of the movie, you'll see a number - in this case, 503919.  This is the tmdb ID.  To request The Lighthouse, you'll type:

`r 503919`

in a channel defined by RADARR_CHANNELS in the config.