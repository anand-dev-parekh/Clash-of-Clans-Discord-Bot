# Clash-of-Clans-Discord-Bot
This Bot displays a users Clash of Clans stats with some basic commands.


This is different to the popular ClashofStats bot as it allows the user to set their player tag and clan tag. In the ClashofStats discord bot, one annoying problem is always having to type out your player tag (which is random characters and numbers) to view your stats. This program stores the discord user's player tag and clan tag using mongoDB that way the user can just type out the command and get stats from the Clash of Clans API. The user can set their player tag and clan tag once and never have to worry about it again!





Commands:

    Bot setup:
      Command = .setplayertag {tag}
      Description = This sets the discord user's player tag to whatever they specify and stores it (mongoDB).
      
      Command = .setclantag {tag}
      Description = This sets the discord user's clan tag to whatever they specify and stores it (mongoDB).
      
      Command = .mytags
      Description = This displays the discord user's tags they have (if) set.
   
   Player Commands:
      IMPORTANT: The optionalTag will only be optional if they have set their player tag in the Bot Setup above. Or if the user would like to check the stats of                   a different user they will have to write in the other user's tag.
   
   
      Command = .homeprofile {optionalTag}
      Description = Displays statistics about the discord user's home profile.
      
      Command = .builderprofile {optionalTag}
      Description = Displays statistics about the discord user's builder profile.
      
      Command = .hometroops {optionalTag}
      Description = Displays statistics about the discord user's home troops
      
      Command = .buildertroops {optionalTag}
      Description = Displays statistics about the discord user's builder troops
      
  Clan Commands: 
      IMPORTANT: The optionalTag will only be optional if they have set their clan tag in the Bot Setup above. Or if the user would like to check the stats of                   a different clan they will have to write in the other clan's tag.
      
      Command = .clanprofile {optionalTag}
      Description = Displays statistics about the clan's profile
      
      Command = .clanwar {optionalTag}
      IMPORTANT: Only will work if clan's war log is public
      Description = Displays stats about the clan war. If the clan is in preparation, war, or not in war. If the clan is in war, it will display the score, and                       the attacks left for each member in the clan.
  
  
