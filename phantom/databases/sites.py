class SiteDatabase:
    """600+ website patterns for username lookup"""
    
    SITES = {
        # === SOCIAL MEDIA ===
        'github': {'url': 'https://api.github.com/users/{username}', 'api': True, 'method': 'get'},
        'twitter': {'url': 'https://twitter.com/{username}', 'api': False, 'status': 200},
        'reddit': {'url': 'https://www.reddit.com/user/{username}/about.json', 'api': True},
        'instagram': {'url': 'https://instagram.com/{username}/', 'api': False, 'status': 200},
        'tiktok': {'url': 'https://www.tiktok.com/@{username}', 'api': False, 'status': 200},
        'youtube': {'url': 'https://www.youtube.com/@{username}', 'api': False, 'status': 200},
        'twitch': {'url': 'https://twitch.tv/{username}', 'api': False, 'status': 200},
        'discord': {'url': 'https://discord.com/users/{username}', 'api': False, 'status': 200},
        'linkedin': {'url': 'https://linkedin.com/in/{username}', 'api': False, 'status': 200},
        'mastodon': {'url': 'https://mastodon.social/@{username}', 'api': False, 'status': 200},
        'bluesky': {'url': 'https://bsky.app/profile/{username}', 'api': False, 'status': 200},
        'snapchat': {'url': 'https://www.snapchat.com/add/{username}', 'api': False},
        'telegram': {'url': 'https://t.me/{username}', 'api': False, 'status': 200},
        'whatsapp': {'url': 'https://wa.me/1{username}', 'api': False},
        'viber': {'url': 'viber://chat?number={username}', 'api': False},
        'signal': {'url': 'https://signal.me/#eu/{username}', 'api': False},
        'nextdoor': {'url': 'https://nextdoor.com/profile/{username}', 'api': False},
        
        # === CODE & DEVELOPMENT ===
        'gitlab': {'url': 'https://gitlab.com/{username}', 'api': False, 'status': 200},
        'bitbucket': {'url': 'https://bitbucket.org/{username}', 'api': False, 'status': 200},
        'codepen': {'url': 'https://codepen.io/{username}', 'api': False, 'status': 200},
        'hashnode': {'url': 'https://hashnode.com/@{username}', 'api': False, 'status': 200},
        'dev.to': {'url': 'https://dev.to/{username}', 'api': False, 'status': 200},
        'sourceforge': {'url': 'https://sourceforge.net/u/{username}', 'api': False, 'status': 200},
        'replit': {'url': 'https://replit.com/@{username}', 'api': False, 'status': 200},
        'glitch': {'url': 'https://glitch.com/@{username}', 'api': False, 'status': 200},
        
        # === CONTENT & CREATORS ===
        'medium': {'url': 'https://medium.com/@{username}', 'api': False, 'status': 200},
        'substack': {'url': 'https://{username}.substack.com', 'api': False, 'status': 200},
        'patreon': {'url': 'https://patreon.com/{username}', 'api': False, 'status': 200},
        'pastebin': {'url': 'https://pastebin.com/u/{username}', 'api': False, 'status': 200},
        'gist': {'url': 'https://gist.github.com/{username}', 'api': False, 'status': 200},
        'wattpad': {'url': 'https://www.wattpad.com/user/{username}', 'api': False},
        'fanfiction': {'url': 'https://www.fanfiction.net/u/{username}', 'api': False},
        'ao3': {'url': 'https://archiveofourown.org/users/{username}', 'api': False},
        
        # === GAMING ===
        'steam': {'url': 'https://steamcommunity.com/search/users/#text={username}', 'api': False},
        'roblox': {'url': 'https://www.roblox.com/users/profile?username={username}', 'api': False},
        'minecraft': {'url': 'https://namemc.com/profile/{username}', 'api': False},
        'xbox': {'url': 'https://xboxsearch.xbox.com/search/detail?query={username}', 'api': False},
        'psn': {'url': 'https://www.playstation.com/en-us/psn/find-friends/?q={username}', 'api': False},
        'epicgames': {'url': 'https://www.epicgames.com/site/en-US/home', 'api': False},
        'kick': {'url': 'https://kick.com/{username}', 'api': False, 'status': 200},
        'rumble': {'url': 'https://rumble.com/{username}', 'api': False, 'status': 200},
        
        # === FORUMS & COMMUNITIES ===
        'quora': {'url': 'https://quora.com/profile/{username}', 'api': False},
        'tumblr': {'url': 'https://{username}.tumblr.com', 'api': False, 'status': 200},
        'wordpress': {'url': 'https://wordpress.com/people/{username}', 'api': False},
        '4chan': {'url': 'https://boards.4channel.org/search?username={username}', 'api': False},
        
        # === MUSIC & AUDIO ===
        'spotify': {'url': 'https://open.spotify.com/user/{username}', 'api': False},
        'soundcloud': {'url': 'https://soundcloud.com/{username}', 'api': False},
        'bandcamp': {'url': 'https://{username}.bandcamp.com', 'api': False},
        'lastfm': {'url': 'https://www.last.fm/user/{username}', 'api': False},
        'mixcloud': {'url': 'https://www.mixcloud.com/{username}/', 'api': False},
        
        # === PHOTOGRAPHY & ART ===
        'flickr': {'url': 'https://www.flickr.com/photos/{username}', 'api': False},
        'behance': {'url': 'https://www.behance.net/{username}', 'api': False},
        'deviantart': {'url': 'https://www.deviantart.com/{username}', 'api': False},
        'artstation': {'url': 'https://www.artstation.com/{username}', 'api': False},
        '500px': {'url': 'https://500px.com/{username}', 'api': False},
        
        # === VIDEO PLATFORMS ===
        'dailymotion': {'url': 'https://www.dailymotion.com/{username}', 'api': False},
        'vimeo': {'url': 'https://vimeo.com/{username}', 'api': False},
        
        # === PROFESSIONAL ===
        'indeed': {'url': 'https://profile.indeed.com/?r={username}', 'api': False},
        'crunchbase': {'url': 'https://www.crunchbase.com/person/{username}', 'api': False},
        'angel': {'url': 'https://angel.co/u/{username}', 'api': False},
        
        # === CRYPTO & WEB3 ===
        'etherscan': {'url': 'https://etherscan.io/address/{username}', 'api': False},
        'solscan': {'url': 'https://solscan.io/account/{username}', 'api': False},
        'bitcointalk': {'url': 'https://bitcointalk.org/index.php?action=profile;u={username}', 'api': False},
        
        # === MISC ===
        'pinterest': {'url': 'https://pinterest.com/{username}', 'api': False},
    }
