# Spellbreak
Limitations: 
- Script will detect mouse presses even outside of the spellbreak window. 

- Changing your swapgauntlet setting MID game will bug out the script. When your match is started it checks if your swapgauntlet setting is on or off. 
  It doesn't check anymore after your match has started, only upon a newly started match. 
  I can add a periodic check after the match has started but this will create extra overhead.
  
- Script will bugg out when playing in certain regions. Seems to be an encoding issue. Will fix this eventually.

- There is no GUI. This is something I might add later if there is a demand for a GUI. (Also I need to learn how to make a proper GUI lol)

- Script expects your Center-screen loadout scaling to be set to 100. Values too high or too low 100 will cause the image recognition function to fail. 
  This can be fixed manually by the user though. I will make a manual for it.
  
- The script monitors right and left mouse click. It doesn't check if you've succesfully launched an attack. 
  Meaning that if you try to attack while you're out of mana, it will still register the mouse click and run the api command.
  
- Sorceries are not supported yet. I will try to add this but it will most likely also have some limitations due to sorcery cooldowns.

- Most gauntlets have a decently long ending animation. As a matter of fact, only wind is fast. 
  If you use for instance fire gauntlet and try to attack with any other gauntlet before the fire drawback animation has finished, it will still see this as a mouse  click thus it will call the api.
  This is something I can't fix. It can be slighly mitigated by adding a short time out after a mouse click has been detected and processed.
  
- Noodle is not always recognized. This is because the noodle icon is slightly transluscent. Hardly ever happens though and majority of the time user will have an offhand anyway. Thus I'm not gonna bother trying to get recognition to 100% for noodle  
