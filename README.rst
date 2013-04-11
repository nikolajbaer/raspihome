RaspiHome
===========

This is an experiment in making a "Home Information System" that I can pluggably extend to give me a remote dashboard from a Raspberry Pi plugged into my home network and exposed via HTTP.

Status
------

Concept => no working code yet. Check back in 6 months!


General Architecture Idea
-------------------------

The basic idea is to have nginx serving HTML, and proxying to a cherrypy app server that manages the information and session handling/authentication. I want the page to be a static html page with a long expires, and then have most of the updating via ajax calls to JSON/REST feeds to minimize effort on the not-so-powerful raspi. Things that can be statically generated on a timer will be done.

I am going to be investigating general open source home information systems (e.g. freedomotic) for architectural clues, but am mostly going to be brewing this from scratch.

Goals
-----

- Runs easily on Raspi without taxing the little thing too much (still enough hp left over for file sharing, SSH jump server, etc).
- Responsive design for both tablet, mobile and desktop
- Leverage MozApps/WebApp emerging standards to minimize requests on raspberry pi (e.g. App Caching)
- Pluggable Pythonic architecture for easy addition of new items

Ideas for Plugins
-----------------

- Wifi monitor (what devices attached?)
- House Temperature graph
- webcam snapshot / secure proxy via nginx  
- Garage door status
- Current weather
- ZigBee / X10 and other stuff..



