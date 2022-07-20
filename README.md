# iCODE
A Discord Bot coded in Python.
<br>
<br>

- [iCODE](#icode)
- [Features](#features)
  - [Animated Emojis Without Nitro](#animated-emojis-without-nitro)
    - [How this works?](#how-this-works)
  - [Reaction Roles](#reaction-roles)
  - [YouTube Search](#youtube-search)
  - [Text Filter](#text-filter)
- [Commands](#commands)
  - [General Commands](#general-commands)
    - [`/avatar`](#avatar)
        - [Command Syntax:](#command-syntax)
    - [`/embed`](#embed)
        - [Command Syntax:](#command-syntax-1)
    - [`/icon`](#icon)
        - [Command Syntax:](#command-syntax-2)
    - [`/membercount`](#membercount)
        - [Command Syntax:](#command-syntax-3)
    - [`/serverinfo`](#serverinfo)
        - [Command Syntax:](#command-syntax-4)
    - [`/suggest`](#suggest)
        - [Command Syntax:](#command-syntax-5)
    - [`/userinfo`](#userinfo)
        - [Command Syntax:](#command-syntax-6)
    - [`/update-emojis`](#update-emojis)
        - [Command Syntax:](#command-syntax-7)
    - [`/help`](#help)
        - [Command Syntax:](#command-syntax-8)
  - [Moderation Commands](#moderation-commands)
    - [`/ban`](#ban)
        - [Command Syntax:](#command-syntax-9)
    - [`/kick`](#kick)
        - [Command Syntax:](#command-syntax-10)
    - [`/lock`](#lock)
        - [Command Syntax:](#command-syntax-11)
    - [`/unlock`](#unlock)
        - [Command Syntax:](#command-syntax-12)
    - [`/purge`](#purge)
        - [Command Syntax:](#command-syntax-13)
    - [`/timeout`](#timeout)
        - [Command Syntax:](#command-syntax-14)
  - [Reaction Role Commands](#reaction-role-commands)
    - [`/reaction roles add`](#reaction-roles-add)
        - [Command Syntax:](#command-syntax-15)
    - [`/reaction roles remove`](#reaction-roles-remove)
        - [Command Syntax:](#command-syntax-16)
  - [YouTube Commands](#youtube-commands)
    - [`/youtube search`](#youtube-search-1)
        - [Command Syntax:](#command-syntax-17)
  - [Setup Commands](#setup-commands)
    - [`/setup modlogs`](#setup-modlogs)
        - [Command Syntax:](#command-syntax-18)
    - [`/setup console`](#setup-console)
        - [Command Syntax:](#command-syntax-19)
    - [`/setup suggestions`](#setup-suggestions)
        - [Command Syntax:](#command-syntax-20)
    - [`/setup bump-reminder`](#setup-bump-reminder)
        - [Command Syntax:](#command-syntax-21)
    - [`/setup bumper-role`](#setup-bumper-role)
        - [Command Syntax:](#command-syntax-22)
    - [`/setup reaction-roles`](#setup-reaction-roles)
        - [Command Syntax:](#command-syntax-23)
  - [Miscellaneous Commands](#miscellaneous-commands)
    - [`/exec`](#exec)
        - [Command Syntax:](#command-syntax-24)
    - [`/toggle-maintenance-mode`](#toggle-maintenance-mode)
        - [Command Syntax:](#command-syntax-25)


# Features
iCODE has many features. Here are some I love:
<br>
- Animated Emojis Without Nitro
- Reaction Roles
- YouTube Search
- Text Filter
<br>
<br>

## Animated Emojis Without Nitro
This one is my favourite. It lets anyone use animated emojis, whether
or not they have discord nitro subscription (a premium plan which lets
users use animated emojis and some more premium features). This one is
implemented in `src/bot.py`.
<br>

### How this works?
Whenever someone tries to use an animated emoji, the bot catches the msg,
reads every emoji and deletes the message. Then it processes the emojis
and sends a webhook back to the same channel which shows those emojis!
<br>
<br>

## Reaction Roles
Discord servers have **Roles**. These are like ranks in a forum or on a
subreddit. They give users different privileges within a server or make
them stand out from other users by adding a color to their name or placing
them higher than other users on the sidebar. On Discord, `reaction roles`
are roles users can assign and unassign to themselves by simply reacting to
a message with an emoji. iCODE has commands to set up messages for reaction
roles. The commands for this are defined in `/src/commands/reaction_roles.py`.
<br>
<br>

## YouTube Search
This one lets users stream (search for) YouTube videos right from Discord!
For this I integrated the `YouTube Data API` in `/src/utils/youtube.py`.
<br>
<br>

## Text Filter
This one keeps the chat clean and community friendly. It basically censors
bad words that come in chat. For this, I used `/data/badwords.txt` (from 
Google archives), implemented in `/src/utils/filter.py`.
<br>
<br>
<br>
<br>

# Commands
iCODE has a lot of commands to work with. I've divided them into different
groups (Command groups or `Cogs`). 
<br>
1. [General Commands](#general-commands)
2. [Moderation Commands](#moderation-commands)
3. [ReactionRole Commands](#reaction-role-commands)
4. [YouTube Commands](#youtube-commands)
5. [Setup Commands](#setup-commands)
6. [Miscellaneous Commands](#miscellaneous-commands)
<br>
<br>
<br>

## General Commands
These commands are defined in `/src/commands/general.py`.
Anyone can use these commands.
<br>
<br>

### `/avatar`
This command gets the avatar (profile picture) of a member in a server.
<br>

##### Command Syntax:
```html
/avatar [member]
```
`member` *`[OPTIONAL]`*: A server member
<br>
<br>

### `/embed`
This is used to create an embedded message.
<br>

##### Command Syntax:
```html
/embed
```

<br>

### `/icon`
It is used to get the icon of a server.
<br>

##### Command Syntax:
```
/icon
```

<br>

### `/membercount`
Get the number of members (humans and bots) in the server.
<br>

##### Command Syntax:
```html
/membercount
```

<br>

### `/serverinfo`
Get server information.
<br>

##### Command Syntax:
```html
/serverinfo
```

<br>

### `/suggest`
Make a suggestion.
<br>

##### Command Syntax:
```html
/suggest <suggestion>
```
`suggestion` *`REQUIRED`*: The suggestion to be suggested.
<br>
<br>

### `/userinfo`
Get information about a member.
<br>

##### Command Syntax:
```html
/userinfo <member>
```
`member` *`<REQUIRED>`*: A discord member
<br>
<br>

### `/update-emojis`
Update server emojis. Should be run after adding emojis.
<br>

##### Command Syntax:
```html
/update-emojis
```

<br>

### `/help`
Get help menu for commands
<br>

##### Command Syntax:
```html
/help
```

<br>
<br>

## Moderation Commands
These commands are defined in `/src/commands/moderation.py`
These can be used by server moderators/admins. The usage of these commands
gets logged in the server modlogs channel.
<br>
<br>

### `/ban`
Ban a member from a server.
<br>

##### Command Syntax:
```html
/ban <member> [reason]
```
`member` *`<REQUIRED>`*: Member to be banned<br>
`reason` *`[OPTIONAL]`*: Reason for this action
<br>
<br>

### `/kick`
Kick a member from a server.
<br>

##### Command Syntax:
```html
/kick <member> [reason]
```
`member` *`<REQUIRED>`*: Member to be kicked<br>
`reason` *`[OPTIONAL]`*: Reason for this action
<br>
<br>

### `/lock`
Lock current channel.
<br>

##### Command Syntax:
```html
/lock
```

<br>

### `/unlock`
Unlock current channel if locked.
<br>

##### Command Syntax:
```html
/unlock
```

<br>

### `/purge`
Delete a number of messages.
<br>

##### Command Syntax:
```html
/purge <count> [from_user]
```
`count` *`<REQUIRED>`*: Number of messages to delete. Use `all` for all messages.<br>
`from_user` *`[OPTIONAL]`*: Delete messages from one member.
<br>
<br>

### `/timeout`
Timeout a server member for some time.
<br>

##### Command Syntax:
```html
/timeout <member> <duration> [reason]
```
`member` *`<REQUIRED>`*: Member to be timed out<br>
`duration` *`<REQUIRED>`*: Time in minutes<br>
`reason` *`[OPTIONAL]`*: Reason for this action
<br>
<br>
<br>

## Reaction Role Commands
These commands are defined in `/src/commands/reaction_roles.py`.
These can be used by server moderators/admins. Use these to set messages
for reaction roles.
<br>
<br>

### `/reaction roles add`
Set a message for reaction roles. Add reactions to the message before
using this command.
<br>

##### Command Syntax:
```html
/reaction roles add <message_id> <roles>
```
`message_id` *`<REQUIRED>`*: ID of the message<br>
`roles` *`<REQUIRED>`*: A string of role names separated by `-`. This must be in the
same order as of the reactions on the message.
<br>
<br>

### `/reaction roles remove`
Remove reaction roles from a message.
<br>

##### Command Syntax:
```html
/reaction roles remove <message_id>
```
`message_id` *`<REQUIRED>`*: ID of the message
<br>
<br>
<br>

## YouTube Commands
These commands are defined in `src/commands/youtube.py`.
Anyone can use these commands.
<br>
<br>

### `/youtube search`
Search for a YouTube video.
<br>

##### Command Syntax:
```html
/youtube search <query> [single]
```
`query` *`<REQUIRED>`*: Search query<br>
`single` *`[OPTIONAL, Default: False]`*: Whether a single result is wanted.
<br>
<br>
<br>

## Setup Commands
These commands are defined in `/src/commands/setup.py`<br>
Commands for setting up iCODE. Only members with Admin perms can use
these commands.
<br>
<br>

### `/setup modlogs`
Set up a channel for moderation logs.
<br>

##### Command Syntax:
```html
/setup modlogs [channel]
```
`channel` *`[OPTIONAL, Default: Current Channel]`*: The channel
to be set for moderation logs
<br>
<br>

### `/setup console`
Set up a channel for greeting members.
<br>

##### Command Syntax:
```html
/setup console [channel]
```
`channel` *`[OPTIONAL, Default: Current Channel]`*: The channel
to be set for greeting members.
<br>
<br>

### `/setup suggestions`
Set up a channel for suggestions.
<br>

##### Command Syntax:
```html
/setup suggestions [channel]
```
`channel` *`[OPTIONAL, Default: Current Channel]`*: The channel
to be set for suggestions.
<br>
<br>

### `/setup bump-reminder`
Set up a channel for bump reminders logs.
<br>

##### Command Syntax:
```html
/setup bump-reminder [channel]
```
`channel` *`[OPTIONAL, Default: Current Channel]`*: The channel
to be set for bump reminders.
<br>
<br>

### `/setup bumper-role`
Set up a role for bump reminder mentions.
<br>

##### Command Syntax:
```html
/setup bumper-role <role>
```
`role` *`<REQUIRED>`*: The role to mention in bump reminders.
<br>
<br>

### `/setup reaction-roles`
Configure iCODE for reaction roles in the server.
<br>

##### Command Syntax:
```html
/setup reaction-roles
```

<br>
<br>

## Miscellaneous Commands
These commands are defined in `/src/commands/miscellaneous.py`
These commands can only be run by the owner of iCODE (Me).
<br>
<br>

### `/exec`
Run Python code.
<br>

##### Command Syntax:
```html
/exec
```

<br>

### `/toggle-maintenance-mode`
Activate maintenance mode.
<br>

##### Command Syntax:
```html
/toggle-maintenance-mode
```
<br>