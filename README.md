Consortium
==========

This was the webapp for the Assassins' Guild ten-day Consortium, which ran in March 2013.

You have permission to use it, or derivatives thereof, for your MIT Assassins' Guild game, subject to the following disclaimer: 

THIS CODE COMES WITH NO WARRANTY OR PROMISE OF FUNCTIONALITY WHATSOEVER. IT IS ALMOST CERTAINLY INSECURE. IT MAY BREAK ON DAY EIGHT, REVEAL SECRETS TO YOUR PLAYERS, COMPROMISE YOUR SERVER, AND KICK YOUR PUPPY. NEITHER THE AUTHORS NOR THE MIT ASSASSINS' GUILD ASSUME ANY LIABILITY WHATSOEVER FOR ANYTHING YOU DO WITH THIS CODE.

Things you might be looking for:

 * `app/`: the game's app.  This *might* stand on its own but probably needs some work.
 * `askgms/`: an interface for players to ask questions and the GMs to publish answers.
 * `consortium/`: a catchall location for global-ish stuff that didn't fit anywhere else.
 * `hexgrid/`: the black market as a Django app.  Much better than the original assassin-hexgrid system.
 * `keycards/`: integrating with gametex-django, this system would display keycards and allow them to be printed.
 * `messaging/`: an in-game mail system with SMS, email, and zephyr capabilities.
 * `security/`: the game's security-window system.  Pretty specific to Consortium.
 * `static/`: where the site's CSS, images, etc. lived.
 * `succession/`: the lines-of-succession system.  Tied into the character system in hexgrid/.
 * `templates/`: Global Django templates.  Individual apps have their own.
 * `territory/`: a sweet Diplomacyesque territory control mechanic with a full web interface.  NOTE: The Diplomacy decision algorithm makes correct decisions 95% of the time.  That last 5% is what kills you.  

Note that the architecture isn't nearly as neatly-separated as I'd have liked.  I originally intended each of these apps to be standalone and loosely-coupled, but under the pressure of ten-day writing, I often took the quick-and-dirty path; as a result, you'll have your work cut out for you if you want to reuse this code.

Good luck!

-ternus 4/13
