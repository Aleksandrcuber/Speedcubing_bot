# Bot for Speedcubing

Hello! This is a simple telegram bot for keeping your speedcubing results.

## Where can I find it?

This bot can be found at `t.me/cubing_timer_bot`.
To see its code, go to [this repository](https://github.com/Aleksandrcuber/Speedcubing_bot).

## How do I use this bot?

To start it, click on a `start` button at the bottom of the screen. It will ask you to log in.

Logging in is necessary so bot can track results of several people. It is pretty simple: just
create a simple nickname for your account and set a password for it so nobody except you can 
add solves into it. Make sure to memorize your password, as there's no way to reset it.

If you did it, bot will ask you to choose an event you want to add time to. At this point 
there are 6 different disciplines available: normal and one-handed 3x3, 2x2, 4x4, 5x5 and 
megaminx. You can always change selected discipline with `/event` command.

Now you can enter your results, bot will save it. Format your times like this: 
`minutes:seconds:milliseconds`, for `seconds` and `milliseconds` always use 2 digits, adding 
`0` to the beginning if necessary. Instead of colons dots can be used. You can 
also add comments for your solves just by putting them after digits (use at least 
one `space` to separate it). You can skip `minutes` in your message, if your solve took 
less than a minute. For example, `12:00` means 12-second solve. 
`1:10:50 easy centers` - an example of proper input.

## What else can I do?

You can use `/help` command to see all options.

Briefly, you can see results of other users via `/global` command, see statistics on your own
solves using `/stats` and find your `n` very last solves by typing `/last n`. This options 
will not work unless you're logged in and have already chosen an event.

###### ***Hope you enjoyed!***