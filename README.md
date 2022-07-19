# iCODE
#### Video Demo:  <URL HERE>
#### Description: A Discord bot coded in Python
#### Author: `Tauseef Hilal Tantary`
<br>
<br>


# Features
iCODE has many features. Here are some I love:
<br>
- Animated Emojis Without Nitro
- YouTube Search
- Reaction Roles
- Text Filter
<br>
<br>

## Animated Emojis Without Nitro
This one is my favourite. It lets anyone use animated emojis, whether<br>
or not they have discord nitro subscription (a premium plan which lets<br>
users use animated emojis and some more premium features).
<br>

### How this works?
Whenever someone tries to use an animated emoji, the bot catches the msg<br>
reads every emoji and deletes the message. Then it processes the emojis<br>
and sends a webhook back to the same channel which shows that emoji!
<br>
<br>

## YouTube Search
This one lets users stream (search for) YouTube videos right from Discord!<br>
<br>
<br>

## Reaction Roles
Discord servers have **Roles**.These are like ranks in a forum or on a <br>
subreddit. They give users different privileges within a server or make<br>
them stand out from other users by adding a color to their name or placing<br>
them higher than other users on the sidebar. On Discord, **reaction roles**<br>
are roles users can assign and unassign to themselves by simply reacting to<br>
a message with an emoji. iCODE has commands to set up messages for<br>
reaction roles.
<br>
<br>

## Text Filter
This one keeps the chat clean and community friendly. It basically censors<br>
bad words that come in chat.
<br>
<br>
<br>
<br>

# Commands
iCODE has a lot of commands to work with. I've divided them into different<br>
groups (Command groups or **Cogs**). 
<br>
- General Commands
- Moderation Commands
- ReactionRole Commands
- YouTube Commands
- Setup Commands
- Miscellaneous Commands
<br>
<br>
<br>

## General Commands
These commands can be used by anyone in the a server.
<br>
<br>

### The `/avatar` command
This command gets the avatar (profile picture) of a member in a server.
<br>

#### Command Syntax:
> **`/avatar [member]`**<br>

**member** (optional): A server member
<br>
<br>

### The `/embed` command
This is used to create an embedded message.
<br>

#### Command Syntax:
> **`/embed`**<br>


<br>

### The `/icon` command
It is used to get the icon of a server.
<br>

#### Command Syntax:
> **`/icon`**<br>


<br>

### The `/membercount` command
Get the number of members (humans and bots) in the server.
<br>

#### Command Syntax:
> **`/membercount`**<br>


<br>

### The `/serverinfo` command
Get server information.
<br>

#### Command Syntax:
> **`/serverinfo`**<br>


<br>

### The `/suggest` command
Make a suggestion.
<br>

#### Command Syntax:
> **`/suggest <suggestion>`**<br>

**suggestion**: The suggestion to be suggested.
<br>
<br>

### The `/userinfo` command
Get information about a member.
<br>

#### Command Syntax:
> **`/userinfo <member>`**<br>

**member**: A discord member
<br>
<br>

### The `/update-emojis` command
Update server emojis. Should be run after adding emojis.
<br>

#### Command Syntax:
> **`/update-emojis`**<br>


<br>

### The `/help` command
Get help menu for commands
<br>

#### Command Syntax:
> **`/help`**<br>


<br>
<br>

## Moderation Commands
These can be used by server moderators/admins. The usage of these commands<br>
gets logged in the server modlogs channel.
<br>
<br>

### The `/ban` command
Ban a member from a server.
<br>

#### Command Syntax:
> **`/ban <member> [reason]`**<br>

**member**: Member to be banned<br>
**reason** (optional): Reason for this action
<br>
<br>

### The `/kick` command
Kick a member from a server.
<br>

#### Command Syntax:
> **`/kick <member> [reason]`**<br>

**member**: Member to be kicked<br>
**reason** (optional): Reason for this action
<br>
<br>

### The `/lock` command
Lock current channel.
<br>

#### Command Syntax:
> **`/lock`**<br>


<br>

### The `/unlock` command
Unlock current channel if locked.
<br>

#### Command Syntax:
> **`/unlock`**<br>


<br>

### The `/purge` command
Delete a number of messages.
<br>

#### Command Syntax:
> **`/purge <count> [from_user]`**<br>

**count**: Number of messages to delete. Use `all` for all messages.<br>
**from_user** (optional): Delete messages from one member.
<br>
<br>

### The `/timeout` command
Timeout a server member for some time.
<br>

#### Command Syntax:
> **`/timeout <member> <duration> [reason]`**<br>

**member**: Member to be timed out<br>
**duration**: Time in minutes<br>
**reason** (optional): Reason for this action
<br>
<br>
<br>

## Reaction Role Commands
These can be used by server moderators/admins. Use these to set messages<br>
for reaction roles.
<br>
<br>

### The `/reaction roles add` command
Set a message for reaction roles. Add reactions to the message before<br>
using this command.
<br>

#### Command Syntax:
> **`/reaction roles add <message_id> <roles>`**<br>

**message_id**: ID of the message<br>
**roles**: A string of role names separated by `-`. This must be in the<br>
same order as of the reactions on the message.
<br>
<br>

### The `/reaction roles remove` command
Remove reaction roles from a message.
<br>

#### Command Syntax:
> **`/reaction roles remove <message_id>`**<br>

**message_id**: ID of the message<br>
<br>
<br>
<br>

## YouTube Commands
Anyone can use these commands.
<br>
<br>

### The `/youtube search` command
Search for a YouTube video.
<br>

#### Command Syntax:
> **`/youtube search <query> [single=False]`**<br>

**query**: Search query<br>
**single** (optional, defaults to False): Whether a single result is wanted.
<br>
<br>
<br>

## Setup Commands
Commands for setting up iCODE. Only members with Admin perms can use<br>
these commands.
<br>
<br>

### The `/setup modlogs` command
Set up a channel for moderation logs.
<br>

#### Command Syntax:
> **`/setup modlogs [channel=#CURRENT_CHANNEL]`**<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for moderation logs
<br>
<br>

### The `/setup console` command
Set up a channel for greeting members.
<br>

#### Command Syntax:
> **`/setup console [channel=#CURRENT_CHANNEL]`**<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for greeting members.
<br>
<br>

### The `/setup suggestions` command
Set up a channel for suggestions.
<br>

#### Command Syntax:
> **`/setup suggestions [channel=#CURRENT_CHANNEL]`**<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for suggestions.
<br>
<br>

### The `/setup bump-reminder` command
Set up a channel for bump reminders logs.
<br>

#### Command Syntax:
> **`/setup bump-reminder [channel=#CURRENT_CHANNEL]`**<br>

**channel** (optional, defaults to the current channel): The channel<br>
to be set for bump reminders.
<br>
<br>

### The `/setup bumper-role` command
Set up a role for bump reminder mentions.
<br>

#### Command Syntax:
> **`/setup bumper-role <role>`**<br>

**role**: The role to mention in bump reminders.
<br>
<br>

### The `/setup reaction-roles` command
Configure iCODE for reaction roles in the server.
<br>

#### Command Syntax:
> **`/setup reaction-roles`**<br>


<br>
<br>

## Miscellaneous Commands
These commands can only be run by the owner of iCODE (Me).
<br>
<br>

### The `/exec` command
Run Python code.
<br>

#### Command Syntax:
> **`/exec`**<br>


<br>

### The `/toggle-maintenance-mode` command
Activate maintenance mode.
<br>

#### Command Syntax:
> **`/toggle-maintenance-mode`**<br>