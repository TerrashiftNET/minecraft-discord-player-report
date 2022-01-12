## Minecraft activity-check

`activity-check.py` is a script written in python that can be used to gather last player login dates on a specific Minecraft world and send a formatted report to Discord.

----------
### Installation
1. Clone the repository
2. Install required modules with: `pip3 install -r requirements.txt`
3. Add required values to `config.json`
```
whitelist - path to the whitelist file
stat_location - path to the stat directory of the Minecraft world
webhook_url - your Discord webhook
```
