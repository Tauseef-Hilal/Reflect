# iCODE
#### Video Demo:  <URL HERE>
#### Description: A Discord bot coded in Python
#### Author: `Tauseef Hilal Tantary`




# Features
iCODE has many features. Here are some I love:

- Animated Emojis Without Nitro
- YouTube Search
- Reaction Roles
- Text Filter


## Animated Emojis Without Nitro
This one is my favourite. It lets anyone use animated emojis, whether<br>
or not they have discord nitro subscription (a premium plan which lets<br>
users use animated emojis and some more premium features).

### How this works?
Whenever someone tries to use an animated emoji, the bot catches the msg<br>
reads every emoji and deletes the message. Then it processes the emojis<br>
and sends a webhook back to the same channel which shows that emoji!


## YouTube Search
This one lets users stream (search for) YouTube videos right from Discord!<br>


## Reaction Roles
Discord servers have **Roles**.These are like ranks in a forum or on a <br>
subreddit. They give users different privileges within a server or make<br>
them stand out from other users by adding a color to their name or placing<br>
them higher than other users on the sidebar. On Discord, **reaction roles**<br>
are roles users can assign and unassign to themselves by simply reacting to<br>
a message with an emoji. iCODE has commands to set up messages for reaction roles.


## Text Filter
This one keeps the chat clean and community friendly. It basically censors<br>
bad words that come in chat.




# Commands
iCODE has a lot of commands to work with. I've divided them into different<br>
groups (Command groups or **Cogs**). 

- General Commands
- Moderation Commands
- ReactionRole Commands
- YouTube Commands
- Setup Commands
- Miscellaneous Commands



## General Commands
These commands can be used by anyone in the a server.


### The `/avatar` command
This command gets the avatar (profile picture) of a member in a server.

#### Command Syntax:
> `/avatar [member]`<br>

**member** (optional): A server member


### The `/embed` command
This is used to create an embedded message.

#### Command Syntax:
> `/embed`<br>


### The `/icon` command
It is used to get the icon of a server.

#### Command Syntax:
> `/icon`<br>


### The `/membercount` command
Get the number of members (humans and bots) in the server.

#### Command Syntax:
> `/membercount`<br>


### The `/serverinfo` command
Get server information.

#### Command Syntax:
> `/serverinfo`<br>


### The `/suggest` command
Make a suggestion.

#### Command Syntax:
> `/suggest <suggestion>`<br>

**suggestion**: The suggestion to be suggested.


### The `/userinfo` command
Get information about a member.

#### Command Syntax:
> `/userinfo <member>`<br>

**member**: A discord member


### The `/update-emojis` command
Update server emojis. Should be run after adding emojis.

#### Command Syntax:
> `/update-emojis`<br>


### The `/help` command
Get help menu for commands

#### Command Syntax:
> `/help`<br>



## Moderation Commands
These can be used by server moderators/admins. The usage of these commands<br>
gets logged in the server modlogs channel.


### The `/ban` command
Ban a member from a server.

#### Command Syntax:
> `/ban <member> [reason]`<br>

**member**: Member to be banned<br>
**reason** (optional): Reason for this action


### The `/kick` command
Kick a member from a server.

#### Command Syntax:
> `/kick <member> [reason]`<br>

**member**: Member to be kicked<br>
**reason** (optional): Reason for this action


### The `/lock` command
Lock current channel.

#### Command Syntax:
> `/lock`<br>


### The `/unlock` command
Unlock current channel if locked.

#### Command Syntax:
> `/unlock`<br>


### The `/purge` command
Delete a number of messages.

#### Command Syntax:
> `/purge <count> [from_user]`<br>

**count**: Number of messages to delete. Use `all` for all messages.<br>
**from_user** (optional): Delete messages from one member.


### The `/timeout` command
Timeout a server member for some time.

#### Command Syntax:
> `/timeout <member> <duration> [reason]`<br>

**member**: Member to be timed out<br>
**duration**: Time in minutes<br>
**reason** (optional): Reason for this action



## Reaction Role Commands
These can be used by server moderators/admins. Use these to set messages<br>
for reaction roles.


### The `/reaction roles add` command
Set a message for reaction roles. Add reactions to the message before<br>
using this command.

#### Command Syntax:
> `/reaction roles add <message_id> <roles>`<br>

**message_id**: ID of the message<br>
**roles**: A string of role names separated by `-`. This must be in the<br>
same order as of the reactions on the message.


### The `/reaction roles remove` command
Remove reaction roles from a message.

#### Command Syntax:
> `/reaction roles remove <message_id>`<br>

**message_id**: ID of the message<br>



## YouTube Commands
Anyone can use these commands.


### The `/youtube search` command
Search for a YouTube video.

#### Command Syntax:
> `/youtube search <query> [single=False]`<br>

**query**: Search query<br>
**single** (optional, defaults to False): Whether a single result is wanted.



## Setup Commands
Commands for setting up iCODE. Only members with Admin perms can use<br>
these commands.


### The `/setup modlogs` command
Set up a channel for moderation logs.

#### Command Syntax:
> `/setup modlogs [channel=#CURRENT_CHANNEL]`<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for moderation logs


### The `/setup console` command
Set up a channel for greeting members.

#### Command Syntax:
> `/setup console [channel=#CURRENT_CHANNEL]`<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for greeting members.


### The `/setup suggestions` command
Set up a channel for suggestions.

#### Command Syntax:
> `/setup suggestions [channel=#CURRENT_CHANNEL]`<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for suggestions.


### The `/setup bump-reminder` command
Set up a channel for bump reminders logs.

#### Command Syntax:
> `/setup bump-reminder [channel=#CURRENT_CHANNEL]`<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for bump reminders.


### The `/setup bumper-role` command
Set up a role for bump reminder mentions.

#### Command Syntax:
> `/setup bumper-role <role>`<br>

**role**: The role to mention in bump reminders.


### The `/setup reaction-roles` command
Configure iCODE for reaction roles in the server.

#### Command Syntax:
> `/setup reaction-roles`<br>



## Miscellaneous Commands
These commands can only be run by the owner of iCODE (Me).


### The `/exec` command
Run Python code.

#### Command Syntax:
> `/exec`<br>


### The `/toggle-maintenance-mode` command
Activate maintenance mode.

#### Command Syntax:
> `/toggle-maintenance-mode`<br>