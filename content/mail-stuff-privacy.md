+++
title = "mail-stuff privacy policy"
description = "How mail-stuff handles Gmail data."
+++
mail-stuff is a single-user tool. The only Google account it is authorized
for is mine, and this policy describes what it does with that account's data.

## What it accesses

Messages in my own Gmail account, through the read-only scope
`https://www.googleapis.com/auth/gmail.readonly`. It requests no other scope
and has no code that sends, drafts, deletes, labels or archives mail.

## How the data is used

- Recent threads are stored on my own server so I can review them.
- The text of those threads is sent to a third-party language model API,
  currently xAI's Grok, to sort them into the lists described on the
  [project page](@/mail-stuff.md). Its output stays on my server.
- A short summary of open items, with subjects and Gmail links, is posted to
  my own private Discord channel twice a week.

The data is not sold, used for advertising, or shared with anyone else. Use
of information received from Google APIs adheres to the
[Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy),
including the Limited Use requirements.

## Retention and removal

Stored threads and lists stay on my server until I delete them. Access can be
revoked at any time at
[myaccount.google.com/permissions](https://myaccount.google.com/permissions).

## Contact

Szymon Głuch, szymongluch100@gmail.com
