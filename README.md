# simple-local-gallery
Simple local photo gallery

This is a very simple project to add gps information into photos.

The problem I'm facing is that there isn't a reliable for Nikon Z6 III
to get gps information without an external gps device to connect.
The SnapBridge do work but takes a little to connect the smartphone and the camera
and the coordinate isn't always good.
I think sometimes it's get proximate from the phone network antenna.
With bluetooth always active (when camera is ON) the battery last significantly less.

WikiLoc app used in track mode collect reliable gps points compared to values from the photos taken,
for this reason it's better to use it and extract the gpx and inject information into photos.

Nikon NxStudio and other photo apps can do the same job
but I don't want to alter originals and I'd like to post them Flickr.

# TODO

* [ ] Persist all interpolated
* [ ] Select photos for Flickr
* [ ] Convert gps point into Location for tags and groups
* [ ] Use Gemini to create description and additional tags